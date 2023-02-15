from __future__ import annotations

import typer

from itksn import __version__
from itksn.core import SerialNumberStruct

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", help="Print the current version."),
) -> None:
    """
    Manage top-level options
    """
    if version:
        typer.echo(__version__)
        raise typer.Exit()


@app.command()
def parse(serialnumber: str) -> None:
    """
    Parse the provided serial number.
    """
    typer.echo(SerialNumberStruct.parse(serialnumber.encode("utf-8")))


# for generating documentation using mkdocs-click
typer_click_object = typer.main.get_command(app)

if __name__ == "__main__":
    typer.run(main)
