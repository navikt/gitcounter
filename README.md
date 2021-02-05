# gitcounter

This code runs as an action in https://github.com/navikt/vault-iac

## Local requirements
 - Python3.8+
 - [poetry](https://python-poetry.org/)

### How to install/set-up locally
1. `poetry install`
2. `cd "<repo with yaml files>" && poetry run python gitcounter.py`

Done.

### How to test locally
`poetry run pytest`
