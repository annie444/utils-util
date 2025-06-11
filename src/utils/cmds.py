import os
import shutil
from pathlib import Path
from utils.dir import get_utils_dir
from utils import click

__all__ = ["list_cmd", "error", "add_utility", "remove_utility"]


def list_cmd() -> None:
    """'list' or 'ls' command implementation."""
    utils_path = get_utils_dir()
    for item in utils_path.glob("**/*", recurse_symlinks=True):
        if item.is_file(follow_symlinks=True) and os.access(
            item, mode=os.X_OK | os.R_OK, follow_symlinks=True
        ):
            click.echo(
                click.style(
                    click.format_filename(item, shorten=True), fg="cyan", bold=True
                )
            )


def error(message: str) -> str:
    """Print an error message and exit."""
    return f"{click.style('ERROR:', fg='red', bold=True)} {message}"


def add_utility(utility: Path, copy: bool, update: bool) -> None:
    """'add' and 'install' command implementation."""
    utils_path = get_utils_dir()
    new_name = utility.stem.replace("_", "-").lower()
    new_path = utils_path / new_name
    if new_path.exists():
        if update:
            os.remove(new_path)
        else:
            raise click.ClickException(
                error(
                    f"{click.format_filename(new_name, shorten=True)} already exists in the utilities directory.",
                )
            )
    utility = utility.resolve()
    if copy:
        shutil.copy2(utility, new_path)
    else:
        utility = utility.replace(new_path)
    utility.chmod(0o755)
    echo = click.style(
        "Added utility ",
        fg="cyan",
    )
    echo += click.style(
        click.format_filename(utility, shorten=True), fg="magenta", bold=True
    )
    echo += click.style(" to the utilities directory.", fg="cyan")
    click.echo(echo)
    click.echo(
        f"You can now run it with: '{click.format_filename(utility, shorten=True)} ...args'"
    )


def remove_utility(utility: str) -> None:
    """'remove', 'rm', or 'uninstall' command implementation."""
    utils_path = get_utils_dir()
    utility_path = utils_path / utility.replace("-", "_").lower()
    os.remove(utility_path)
    echo = click.style(
        "Removed utility ",
        fg="cyan",
    )
    echo += click.style(
        click.format_filename(utility_path, shorten=True), fg="magenta", bold=True
    )
    echo += click.style(" from the utilities directory.", fg="cyan")
    click.echo(echo)
