from prefect import flow

from prefect_great_expectations.tasks import (
    goodbye_prefect_great_expectations,
    hello_prefect_great_expectations,
)


def test_hello_prefect_great_expectations():
    @flow
    def test_flow():
        return hello_prefect_great_expectations()

    flow_state = test_flow()
    task_state = flow_state.result()
    assert task_state.result() == "Hello, prefect-great-expectations!"


def goodbye_hello_prefect_great_expectations():
    @flow
    def test_flow():
        return goodbye_prefect_great_expectations()

    flow_state = test_flow()
    task_state = flow_state.result()
    assert task_state.result() == "Goodbye, prefect-great-expectations!"
