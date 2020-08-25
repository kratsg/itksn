# itksn

[![GitHub Project](https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub)](https://github.com/kratsg/itksn)
[![GitHub Actions Status: CI](https://github.com/kratsg/itksn/workflows/CI/badge.svg?branch=master)](https://github.com/kratsg/itksn/actions?query=workflow%3ACI+branch%3Amaster)
[![Code Coverage](https://codecov.io/gh/kratsg/itksn/graph/badge.svg?branch=master)](https://codecov.io/gh/kratsg/itksn?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Helper utility for parsing ITk Serial Numbers

## Installation

In a fresh virtual environment, you can install from `PyPI`:

```
$ python -m pip install itksn
```

or from the master branch of the GitHub repository:

```
$ python -m pip install "git+https://github.com/kratsg/itksn.git"
```

The above is actually cloning and installing directly from the Git repository.

However, if you want to, you can of course also install it directly from the Git repository "locally" by first cloning the repo and then from the top level of it running

```
$ python -m pip install .
```

## Contributing

As this library is experimental contributions of all forms are welcome.

If you have ideas on how to improve the API or fix a bug please open an Issue.

You are of course also most welcome and encouraged to open PRs.

### Developing

To develop, use a virtual environment.

Once the environment is activated, clone the repo from GitHub

```
git clone git@github.com:kratsg/itksn.git
```

and install all necessary packages for development

```
python -m pip install --ignore-installed --upgrade -e .[complete]
```

(Optional) Then setup the Git pre-commit hooks by running

```
pre-commit install
```

## Acknowledgements

- [@matthefeickert](https://github.com/matthewfeickert)'s [heputilities](https://github.com/matthewfeickert/heputils) repository for a quick start
