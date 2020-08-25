# itksn

[![GitHub Project](https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub)](https://github.com/kratsg/itksn)
[![GitHub Actions Status: CI](https://github.com/kratsg/itksn/workflows/CI/badge.svg?branch=master)](https://github.com/kratsg/itksn/actions?query=workflow%3ACI+branch%3Amaster)
[![Code Coverage](https://codecov.io/gh/kratsg/itksn/graph/badge.svg?branch=master)](https://codecov.io/gh/kratsg/itksn?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Helper utilities around the Scikit-HEP ecosystem for common tasks in HEP

**This library is not meant for wide use and will probably be deprecated in favor of [`scikit-hep`](https://github.com/scikit-hep/scikit-hep) soon.**
This library should be viewed as a testing grounds for API design decisions, hence it will not be put up on PyPI.

## Installation

In a fresh virtual environment

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
If you have ideas on how to improve the API or conceptually how a library meant to introduce people to the Scikit-HEP ecosystem should be structured please open an Issue.
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

Then setup the Git pre-commit hooks by running

```
pre-commit install
```

## Acknowledgements

This library is built upon the hard work of many people in the [Scikit-HEP ecosystem](https://scikit-hep.org/) and is only possible because of the exchange of ideas and contributions of people working together, across experiments and fields to improve science.
This is not an inevitability, but rather the result of directed thought, time, and effort, to which I am most thankful to have benefited from and have been involved in.

## Requests

Cite the software you use in your papers.
