import shutil
from pathlib import Path

import great_expectations as ge
import pandas as pd
import pytest
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.exceptions.exceptions import CheckpointNotFoundError
from prefect import flow

from prefect_great_expectations.validation import (
    GreatExpectationValidationError,
    run_checkpoint_validation,
)

CURRENT_DIR = Path(__file__).parent.resolve()
CONTEXT_ROOT_DIR = CURRENT_DIR / "great_expectations"
DATA_PATH = CURRENT_DIR / "data"


@pytest.fixture(autouse=True)
def disable_usage_stats(monkeypatch):
    monkeypatch.setenv("GE_USAGE_STATS", "FALSE")


class TestRunCheckpointValidation:
    def test_validation_wth_checkpoint_name(self):
        @flow
        def test_flow():
            return run_checkpoint_validation(
                checkpoint_name="my_checkpoint_pass",
                data_context_root_dir=CONTEXT_ROOT_DIR,
            )

        result = test_flow()
        assert result.success, "Checkpoint validation should pass"

    def test_validation_with_checkpoint(self):
        @flow
        def test_flow():
            checkpoint = ge.DataContext(
                context_root_dir=str(CONTEXT_ROOT_DIR)
            ).get_checkpoint("my_checkpoint_pass")
            return run_checkpoint_validation(
                checkpoint=checkpoint, data_context_root_dir=CONTEXT_ROOT_DIR
            )

        result = test_flow()
        assert result.success, "Checkpoint validation should pass"

    def test_checkpoint_supercedes_checkpoint_name(self):
        @flow
        def test_flow():
            checkpoint = ge.DataContext(
                context_root_dir=str(CONTEXT_ROOT_DIR)
            ).get_checkpoint("my_checkpoint_pass")
            return run_checkpoint_validation(
                checkpoint=checkpoint,
                checkpoint_name="my_checkpoint_fail",
                data_context_root_dir=CONTEXT_ROOT_DIR,
            )

        result = test_flow()
        assert result.success, "Checkpoint validation should pass"

    def test_validation_with_data_context(self):
        @flow
        def test_flow():
            data_context = ge.DataContext(context_root_dir=str(CONTEXT_ROOT_DIR))
            return run_checkpoint_validation(
                checkpoint_name="my_checkpoint_pass", data_context=data_context
            )

        result = test_flow()
        assert result.success, "Checkpoint validation should pass"

    def test_data_context_supercedes_data_context_root_dir(self, tmp_path):
        tmp_data_context_root_dir = tmp_path / "great_expectations"
        # Recreate current data context in tmp directory
        shutil.copytree(CONTEXT_ROOT_DIR, tmp_data_context_root_dir)

        @flow
        def test_flow():
            data_context = ge.DataContext(
                context_root_dir=str(tmp_data_context_root_dir)
            )
            # Delete the checkpoint in the tmp data context
            data_context.delete_checkpoint("my_checkpoint_pass")
            return run_checkpoint_validation(
                checkpoint_name="my_checkpoint_pass",
                data_context=data_context,
                data_context_root_dir=CONTEXT_ROOT_DIR,
            )

        # Running the flow should raise if the tmp data context is used
        with pytest.raises(CheckpointNotFoundError, match="my_checkpoint_pass.yml"):
            test_flow()

    def test_failed_validation_raises_by_default(self):
        @flow
        def test_flow():
            return run_checkpoint_validation(
                checkpoint_name="my_checkpoint_fail",
                data_context_root_dir=CONTEXT_ROOT_DIR,
            )

        with pytest.raises(GreatExpectationValidationError) as ex_info:
            test_flow()

        assert (
            not ex_info.value.result.success
        ), "Validation result should be accessible on raised exception"

    def test_failed_validation_with_no_raise(self):
        @flow
        def test_flow():
            return run_checkpoint_validation(
                checkpoint_name="my_checkpoint_fail",
                data_context_root_dir=CONTEXT_ROOT_DIR,
                raise_on_validation_failure=False,
            )

        result = test_flow()
        assert (
            not result.success
        ), "Checkpoint validation should fail without raising an exception"

    def test_run_name_properly_set(self):
        @flow
        def test_flow():
            return run_checkpoint_validation(
                checkpoint_name="my_checkpoint_pass",
                data_context_root_dir=CONTEXT_ROOT_DIR,
                run_name="THIS IS A CUSTOM RUN NAME",
            )

        result = test_flow()
        assert (
            result.run_id.run_name == "THIS IS A CUSTOM RUN NAME"
        ), "run_name does not match expected value"

    def test_validate_dataframe(self):
        @flow
        def test_flow():
            df = pd.read_csv(DATA_PATH / "yellow_tripdata_sample_2019-02.csv")
            runtime_batch_request = RuntimeBatchRequest(
                datasource_name="data__dir",
                data_connector_name="default_runtime_data_connector_name",
                data_asset_name="yellow_tripdata_sample_2019-02_df",
                runtime_parameters={"batch_data": df},
                batch_identifiers={
                    "default_identifier_name": "ingestion step 1",
                },
            )
            return run_checkpoint_validation(
                checkpoint_name="my_checkpoint_pass",
                data_context_root_dir=CONTEXT_ROOT_DIR,
                checkpoint_kwargs={
                    "validations": [
                        {
                            "batch_request": runtime_batch_request,
                            "expectation_suite_name": "taxi.demo_pass",
                        }
                    ]
                },
            )

        result = test_flow()
        assert result.success, "Checkpoint validation should be successful"
