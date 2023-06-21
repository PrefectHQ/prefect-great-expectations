# prefect-great-expectations

<p align="center">
    <a href="https://pypi.python.org/pypi/prefect-great-expectations/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-great-expectations?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/PrefectHQ/prefect-great-expectations/" alt="Stars">
        <img src="https://img.shields.io/github/stars/PrefectHQ/prefect-great-expectations?color=0052FF&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/prefect-great-expectations/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/prefect-great-expectations?color=0052FF&labelColor=090422" /></a>
    <a href="https://github.com/PrefectHQ/prefect-great-expectations/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/PrefectHQ/prefect-great-expectations?color=0052FF&labelColor=090422" /></a>
    <br>
    <a href="https://prefect-great-expectations-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>
    <a href="https://discourse.prefect-great-expectations.io/" alt="Discourse">
        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>
</p>

## Welcome!

Prefect integration for interacting with Great Expectations.

[Great Expectations](https://greatexpectations.io/gx-oss) is a Python library for data quality. It provides a framework to validate your state of data.

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda, or virtualenv.

These tasks are designed to work with Prefect 2. For more information about how to use Prefect, please refer to the [Prefect documentation](https://docs.prefect.io/).

### Installation

Install `prefect-great-expectations` with `pip`:

```bash
pip install prefect-great-expectations
```

### Write and run a flow

```python
from prefect import flow
from prefect_great_expectations import run_checkpoint_validation

@flow
def example_flow():
   run_checkpoint_validation(checkpoint_name="my_checkpoint")

example_flow()
```

## Tutorial

For a larger example, check out the [tutorial](tutorial.md).

## Resources

If you encounter any bugs while using `prefect-great-expectations`, feel free to open an issue in the [prefect-great-expectations](https://github.com/PrefectHQ/prefect-great-expectations) repository.

If you have any questions or issues while using `prefect-great-expectations`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

Feel free to ⭐️ or watch [`prefect-great-expectations`](https://github.com/PrefectHQ/prefect-great-expectations) for updates too!

## Development

If you'd like to install a version of `prefect-great-expectations` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/PrefectHQ/prefect-great-expectations.git

cd prefect-great-expectations/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
