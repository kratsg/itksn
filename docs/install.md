# Installation

---

## pip

itksn is available on PyPI and can be installed with [pip](https://pip.pypa.io).

```bash
pip install itksn
```

<!-- prettier-ignore -->
!!! warning
    This method modifies the Python environment in which you choose to install. Consider instead using [pipx](#pipx) or virtual environments to avoid dependency conflicts.

## pipx

[pipx](https://github.com/pypa/pipx) allows for the global installation of
Python applications in isolated environments.

```bash
pipx install itksn
```

## virtual environment

```bash
python -m venv venv
source venv/bin/activate
python -m pip install itksn
```

## Conda

See the [feedstock](https://github.com/conda-forge/itksn-feedstock) for more
details.

```bash
conda install -c conda-forge itksn
```

or with [mamba](https://github.com/mamba-org/mamba):

```bash
mamba install itksn
```

<!-- prettier-ignore -->
!!! warning
    This method modifies the Conda environment in which you choose to install. Consider instead using [pipx](#pipx) or [condax](https://github.com/mariusvniekerk/condax) to avoid dependency conflicts.
