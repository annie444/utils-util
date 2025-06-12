from .cmds import list_cmd, add_utility, remove_utility
from .click import click
from .log import get_level, LOG_FORMAT

from pathlib import Path
import logging

logging.basicConfig(level=get_level(), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


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
    logger.debug("Executing 'list' command.")
    list_cmd()


@utils.command(hidden=True)
def ls() -> None:
    """Alias for 'list' command."""
    logger.debug("Executing 'list' command.")
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
    logger.debug("Executing 'add' command.")
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
    logger.debug("Executing 'add' command.")
    add_utility(utility, copy, update=force)


@utils.command(no_args_is_help=True)
@click.argument(
    "utility",
    type=str,
)
@click.confirmation_option()
def remove(utility: str) -> None:
    """Remove the specified utility from the user's utilities directory."""
    logger.debug("Executing 'remove' command.")
    remove_utility(utility)


@utils.command(hidden=True, no_args_is_help=True)
@click.argument(
    "utility",
    type=str,
)
@click.confirmation_option()
def rm(utility: str) -> None:
    """Alias for 'remove' command."""
    logger.debug("Executing 'remove' command.")
    remove_utility(utility)


@utils.command(hidden=True, no_args_is_help=True)
@click.argument(
    "utility",
    type=str,
)
@click.confirmation_option()
def uninstall(utility: str) -> None:
    """Alias for 'remove' command."""
    logger.debug("Executing 'remove' command.")
    remove_utility(utility)
