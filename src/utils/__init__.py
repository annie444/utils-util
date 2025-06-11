from .cmds import list_cmd, add_utility, remove_utility

import rich_click as click
from pathlib import Path

click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_ARGUMENT = "bold cyan"
click.rich_click.STYLE_COMMAND = "bold cyan"
click.rich_click.STYLE_SWITCH = "bold green"
click.rich_click.STYLE_METAVAR = "bold yellow"
click.rich_click.STYLE_METAVAR_SEPARATOR = "dim"
click.rich_click.STYLE_USAGE = "bold yellow"
click.rich_click.STYLE_USAGE_COMMAND = "bold"
click.rich_click.STYLE_HELPTEXT_FIRST_LINE = ""
click.rich_click.STYLE_HELPTEXT = "dim"
click.rich_click.STYLE_OPTION_DEFAULT = "dim"
click.rich_click.STYLE_REQUIRED_SHORT = "red"
click.rich_click.STYLE_REQUIRED_LONG = "dim red"
click.rich_click.STYLE_OPTIONS_PANEL_BORDER = "dim"
click.rich_click.STYLE_COMMANDS_PANEL_BORDER = "dim"


@click.group(no_args_is_help=True, invoke_without_command=False)
def utils() -> None:
    """Manage user maintenance utilities.

    This script provides commands to manage custom user utilities.
    These utilities can be any executable script or program. This
    utility simply provides a standardized way to manage these
    custiom utilities.
    """
    pass


@utils.command()
def list() -> None:
    """List all available utilities"""
    list_cmd()


@utils.command(hidden=True)
def ls() -> None:
    """Alias for 'list' command."""
    list_cmd()


@utils.command(no_args_is_help=True)
@click.argument(
    "utility",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
        writable=False,
        executable=False,
        path_type=Path,
        resolve_path=True,
        allow_dash=False,
    ),
)
@click.option(
    "--force", "-f", is_flag=True, help="Force overwrite if utility already exists."
)
@click.option("--copy", "-c", is_flag=True, help="Copy the file instead of move it.")
def add(utility: Path, force: bool = False, copy: bool = False) -> None:
    """Installs the specified utility to the user's utilities directory.

    This command will move the specified utility to the user's utilities
    directory, removing the file extension is any exist, replacing any
    underscores with dashes, make the name lowercase, and ensuring the
    file is executable.
    """
    add_utility(utility, copy, update=force)


@utils.command(hidden=True, no_args_is_help=True)
@click.argument(
    "utility",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
        writable=False,
        executable=False,
        path_type=Path,
        resolve_path=True,
        allow_dash=False,
    ),
)
@click.option(
    "--force", "-f", is_flag=True, help="Force overwrite if utility already exists."
)
@click.option("--copy", "-c", is_flag=True, help="Copy the file instead of move it.")
def install(utility: Path, force: bool = False, copy: bool = False) -> None:
    """Alias for 'add'."""
    add_utility(utility, copy, update=force)


@utils.command(no_args_is_help=True)
@click.argument(
    "utility",
    type=str,
)
@click.confirmation_option()
def remove(utility: str) -> None:
    """Remove the specified utility from the user's utilities directory."""
    remove_utility(utility)


@utils.command(hidden=True, no_args_is_help=True)
@click.argument(
    "utility",
    type=str,
)
@click.confirmation_option()
def rm(utility: str) -> None:
    """Alias for 'remove' command."""
    remove_utility(utility)


@utils.command(hidden=True, no_args_is_help=True)
@click.argument(
    "utility",
    type=str,
)
@click.confirmation_option()
def uninstall(utility: str) -> None:
    """Alias for 'remove' command."""
    remove_utility(utility)


def main() -> None:
    print("Hello from utils!")
