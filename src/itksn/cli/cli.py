import logging
import click

from ..version import __version__
from ..core import SerialNumberStruct

logging.basicConfig()
log = logging.getLogger(__name__)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version=__version__)
def itksn():
    pass


@itksn.command()
@click.argument("serialnumber", type=click.STRING)
def parse(serialnumber):
    """
    Parse the provided serial number.
    """
    click.echo(SerialNumberStruct.parse(serialnumber.encode("utf-8")))
