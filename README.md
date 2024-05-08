# itksn v0.1.1

Helper utility for parsing ITk Serial Numbers

---

<!-- sync the following div with docs/index.md -->
<div align="center">

<img src="https://raw.githubusercontent.com/kratsg/itksn/main/docs/assets/images/logo.svg" alt="itksn logo" width="500" role="img">

<!-- --8<-- [start:badges] -->

<!-- prettier-ignore-start -->

| | |
| --- | --- |
| CI/CD | [![CI - Test][actions-badge]][actions-link] [![CI - Coverage][coverage-badge]][coverage-link] |
| Docs | [![Docs][actions-badge-docs]][actions-link-docs] [![Zenodo][zenodo-badge]][zenodo-link] |
| Package | [![PyPI - Downloads][pypi-downloads]][pypi-link] [![PyPI - Version][pypi-version]][pypi-link] [![PyPI platforms][pypi-platforms]][pypi-link] [![Conda-Forge][conda-badge]][conda-link] |
| Meta | [![GitHub - Discussion][github-discussions-badge]][github-discussions-link] [![GitHub - Issue][github-issues-badge]][github-issues-link] [![License - BSD 3.0][license-badge]][license-link] |

[actions-badge]:            https://github.com/kratsg/itksn/workflows/CI/badge.svg
[actions-link]:             https://github.com/kratsg/itksn/actions
[actions-badge-docs]:       https://github.com/kratsg/itksn/actions/workflows/docs.yml/badge.svg?branch=main
[actions-link-docs]:        https://github.com/kratsg/itksn/actions/workflows/docs.yml?query=branch:main
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/itksn
[conda-link]:               https://github.com/conda-forge/itksn-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/kratsg/itksn/discussions
[github-issues-badge]:      https://img.shields.io/static/v1?label=Issues&message=File&color=blue&logo=github
[github-issues-link]:       https://github.com/kratsg/itksn/issues
[pypi-link]:                https://pypi.org/project/itksn/
[pypi-downloads]:           https://img.shields.io/pypi/dm/itksn.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/itksn
[pypi-version]:             https://img.shields.io/pypi/v/itksn
[rtd-badge]:                https://readthedocs.org/projects/itksn/badge/?version=latest
[rtd-link]:                 https://itksn.readthedocs.io/en/latest/?badge=latest
[coverage-badge]:           https://codecov.io/gh/kratsg/itksn/graph/badge.svg?branch=main
[coverage-link]:            https://codecov.io/gh/kratsg/itksn?branch=main
[license-badge]:            https://img.shields.io/badge/License-BSD_3.0-blue.svg
[license-link]:             https://spdx.org/licenses/BSD-3-Clause.html
[zenodo-badge]:             https://zenodo.org/badge/290293623.svg
[zenodo-link]:              https://zenodo.org/badge/latestdoi/290293623

<!-- prettier-ignore-end -->

<!-- --8<-- [end:badges] -->

</div>

## Using

From the command line, you can parse serial numbers. If there is an error in
parsing, it will loudly complain (sometimes).

```
$ itksn parse 20UPGMC2291234
Container:
    atlas_project = (enum) atlas_detector b'20'
    system_code = (enum) phaseII_upgrade b'U'
    project_code = (enum) pixel_general b'PG'
    subproject_code = (enum) Module_carrier b'MC'
    identifier = Container:
        module_type = (enum) Linear_triplet_module_carrier b'2'
        module_version = (enum) Quad_v2p1 b'2'
        manufacturer = b'9' (total 1)
        number = b'1234' (total 4)

$ itksn parse 20UPGR40012345
Container:
    atlas_project = (enum) atlas_detector b'20'
    system_code = (enum) phaseII_upgrade b'U'
    project_code = (enum) pixel_general b'PG'
    subproject_code = (enum) Digital_quad_module b'R4'
    identifier = Container:
        FE_chip_version = (enum) RD53A b'0'
        reserved = b'0' (total 1)
        number = b'12345' (total 5)

$ itksn parse 20UPGPD0012345
Container:
    atlas_project = (enum) atlas_detector b'20'
    system_code = (enum) phaseII_upgrade b'U'
    project_code = (enum) pixel_general b'PG'
    subproject_code = (enum) Dual_PCB b'PD'
    identifier = Container:
        FE_chip_version = (enum) RD53A b'0'
        reserved = b'0' (total 1)
        number = b'12345' (total 5)

$ itksn parse 20UPGFW2123456
Container:
    atlas_project = (enum) atlas_detector b'20'
    system_code = (enum) phaseII_upgrade b'U'
    project_code = (enum) pixel_general b'PG'
    subproject_code = (enum) FE_chip_wafer b'FW'
    identifier = Container:
        batch_number = (enum) CROC b'2'
        number = b'123456' (total 6)
```

## Installation

In a fresh virtual environment, you can install from `PyPI`:

```
$ python -m pip install itksn
```

or from the main branch of the GitHub repository:

```
$ python -m pip install "git+https://github.com/kratsg/itksn.git"
```

The above is actually cloning and installing directly from the Git repository.

However, if you want to, you can of course also install it directly from the Git
repository "locally" by first cloning the repo and then from the top level of it
running

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

and you can use hatch for running tests/development, e.g.

```
hatch run +py=3.7 dev:test
```

(Optional) Then setup the Git pre-commit hooks by running

```
pre-commit install
```

## Acknowledgements

- [@matthefeickert](https://github.com/matthewfeickert)'s
  [heputilities](https://github.com/matthewfeickert/heputils) repository for a
  quick start

## References

- [Serial Number Specification for ITk pixel modules](https://cds.cern.ch/record/2728364)
- [Proposal for numbering scheme in the ITk, ATU-SYS-AM-0001](https://edms.cern.ch/document/1773411/1)
