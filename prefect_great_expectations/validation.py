"""Tasks for performing Great Expectations validations"""

from pathlib import Path
from typing import Dict, Optional, Union

from great_expectations import DataContext
from great_expectations.checkpoint import Checkpoint
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from prefect import get_run_logger, task


class GreatExpectationValidationError(Exception):
    """
    Signals that a task failed due to a failed Great
    Expectations validation.

    Args:
        result: A CheckpointResult containing details
            of the failed validation.
    """

    def __init__(self, result: CheckpointResult):
        self.result = result
        super().__init__(
            "Great Expectations Validation failed. "
            "Check result on this exception for more details."
        )


@task
def run_checkpoint_validation(
    run_name: Optional[str] = None,
    checkpoint_name: Optional[str] = None,
    checkpoint: Optional[Checkpoint] = None,
    checkpoint_kwargs: Optional[Dict] = None,
    data_context_root_dir: Optional[Union[str, Path]] = None,
    data_context: Optional[DataContext] = None,
    runtime_environment: Optional[Dict] = None,
    raise_on_validation_failure: bool = True,
):
    """
    Task that performs a Great Expectations validation based on the provided checkpoint
        and data context.

    Args:
        run_name: The name of the Great Expectations validation run. Defaults to
            timestamp if not provided.
        checkpoint_name: The name of the Checkpoint to use for validation.
        checkpoint: A Checkpoint object to use for validation. Overrides
            `checkpoint_name` if both are provided.
        checkpoint_kwargs: A dictionary with values used to provide configuration to
            the task's Checkpint at runtime. Keys should match the parameters of
            `CheckpointConfig`.
        data_context_root_dir: Path to the great_expectations directory.
        data_context: A DataContext object to use during validation. Overrides
            `data_context_root_dir` if both are provided.
        runtime_environment: A dictionary with values to overwrite config in
            `great_expectations.yml` at run time.
        raise_on_validation_failure: If `True`, the task will raise a
            GreatExpectationValidationError when validation fails. If `False`,
            the task will return the result of the validation.

    Raises:
        GreatExpectationValidationError: Signals that a GE validation failed.
            Details of the failure can be found by inspecting the `result`
            attribute of the exception.

    Returns:
        CheckpointResult: Detailed result of the validation run in the task.

    Examples:
        Run a validation with a checkpoint named 'my_checkpoint':

        ```python
        from prefect import flow
        from prefect_great_expectations import run_checkpoint_validation


        @flow
        def example_flow():
            run_checkpoint_validation(checkpoint_name="my_checkpoint")

        example_flow()
        ```

        Run a validation with a custom path to the data context:

        ```python
        from prefect import flow
        from prefect_great_expectations import run_checkpoint_validation


        @flow
        def example_flow():
            run_checkpoint_validation(
                checkpoint_name="my_checkpoint",
                data_context_root_dir="my_data_context/"
            )

        example_flow()
        ```
    """
    logger = get_run_logger()

    logger.info("Running Great Expectations validation...")

    runtime_environment = runtime_environment or {}
    checkpoint_kwargs = checkpoint_kwargs or {}

    data_context_root_dir = (
        str(data_context_root_dir) if data_context_root_dir else None
    )

    if data_context:
        logger.debug("Using provided GE Data Context")
    else:
        logger.debug("Loading GE Data Context from %s", data_context_root_dir)
        data_context = DataContext(
            context_root_dir=data_context_root_dir,
            runtime_environment=runtime_environment,
        )

    if checkpoint:
        logger.debug("Using provided GE Checkpoint")
    else:
        logger.debug("Loading GE Checkpoint with name %s", checkpoint_name)
        checkpoint = data_context.get_checkpoint(checkpoint_name)

    result = checkpoint.run(run_name=run_name, **checkpoint_kwargs)

    if not result.success:
        logger.warn(
            "Great Expectations validation run %s failed", result.run_id.run_name
        )
        if raise_on_validation_failure:
            raise GreatExpectationValidationError(result)
    else:
        logger.info(
            "Great Expectations validation run %s succeeded", result.run_id.run_name
        )

    return result
