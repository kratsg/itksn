from __future__ import annotations

import logging

import click

from itksn import __version__
from itksn.core import SerialNumberStruct

logging.basicConfig()
log = logging.getLogger(__name__)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__)
def itksn() -> None:
    pass


@itksn.command()
@click.argument("serialnumber", type=click.STRING)
def parse(serialnumber: str) -> None:
    """
    Parse the provided serial number.
    """
    click.echo(SerialNumberStruct.parse(serialnumber.encode("utf-8")))
