"""This is an example flows module"""
from prefect import flow

from prefect_great_expectations.tasks import (
    goodbye_prefect_great_expectations,
    hello_prefect_great_expectations,
)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    print(hello_prefect_great_expectations)
    print(goodbye_prefect_great_expectations)
