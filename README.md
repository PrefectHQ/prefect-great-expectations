# prefect-great-expectations

## Welcome!

Prefect Collection containing integrations for interacting with Great Expectations

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).

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

## Resources

If you encounter any bugs while using `prefect-great-expectations`, feel free to open an issue in the [prefect-great-expectations](https://github.com/PrefectHQ/prefect-great-expectations) repository.

If you have any questions or issues while using `prefect-great-expectations`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

## Development

If you'd like to install a version of `prefect-great-expectations` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/PrefectHQ/prefect-great-expectations.git

cd prefect-great-expectations/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
