import rich_click as click
from pathlib import Path
import os
import sys

__all__ = ["get_utils_dir", "utils_in_path", "create_utils_dir", "add_utils_to_path"]

UTILS_DIR = Path.home() / ".local" / "share" / "utils" / "bin"

shrc = f"""
# ADDED BY 'utils' SCRIPT >>>
# Add utilities directory to PATH
UTILS_PATH="{UTILS_DIR}"
case ":${{PATH}}:" in
    *:"${{UTILS_PATH}}":*)
        ;;
    *)
        export PATH="$PATH:$UTILS_PATH"
        ;;
esac
# <<< END OF 'utils' SCRIPT
"""
shadd = f'export PATH="$PATH:{UTILS_DIR}"'

bashrc = f"""
# ADDED BY 'utils' SCRIPT >>>
# Add utilities directory to PATH
UTILS_PATH="{UTILS_DIR}"
if [[ $PATH != *"${{UTILS_PATH}}"* ]]; then
    export PATH="$PATH:$UTILS_PATH"
fi
# <<< END OF 'utils' SCRIPT
"""

fishrc = f"""
# ADDED BY 'utils' SCRIPT >>>
# Add utilities directory to PATH
set -l utils_path "{UTILS_DIR}"
if not contains $utils_path $PATH
    set -gx --append PATH $utils_path
end
# <<< END OF 'utils' SCRIPT
"""
fishadd = f'set -gx --append PATH "{UTILS_DIR}"'

nurc = f"""
# ADDED BY 'utils' SCRIPT >>>
# Add utilities directory to PATH
$env.UTILS_PATH = '{UTILS_DIR}'
if $env.UTILS_PATH not-in $env.path {{
    $env.path ++= [$env.UTILS_PATH]
}}
# <<< END OF 'utils' SCRIPT
"""
nuadd = f'$env.path ++= ["{UTILS_DIR}"]'


def get_utils_dir() -> Path:
    """Get the utilities directory path."""
    if not UTILS_DIR.exists() or not utils_in_path():
        create_utils_dir()
    return UTILS_DIR


def utils_in_path() -> bool:
    path_var = [p for p in os.environ.get("PATH", "").split(":") if p]
    return str(UTILS_DIR) in path_var


def create_utils_dir() -> None:
    """Create the utilities directory if it does not exist."""
    UTILS_DIR.mkdir(parents=True, exist_ok=True)
    if utils_in_path():
        add_utils_to_path()


def get_config_dir() -> Path:
    """Get the default user configuration directory."""
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        return Path(xdg_config)
    else:
        # Fallback to the home directory if XDG_CONFIG_HOME is not set
        match sys.platform:
            case "linux":
                return Path.home() / ".config"
            case "darwin":
                return Path.home() / "Library" / "Application Support"
            case "win32":
                return Path.home() / "AppData" / "Roaming"
            case _:
                echo = click.style("Unsupported platform ", fg="red", bold=True)
                echo += click.style(
                    f"{sys.platform}",
                    fg="yellow",
                    bold=True,
                )
                echo += click.style(
                    ". Cannot determine default configuration directory.",
                    fg="red",
                    bold=True,
                )
                raise click.ClickException(echo)


def echo_added_to_rc(rc_file: Path, rc_add: str, already: bool) -> None:
    color1 = "yellow" if already else "cyan"
    color2 = "green" if already else "magenta"
    echo = click.style(
        f"Utilities directory {'already ' if already else ''}added to ",
        fg=color1,
        bold=True,
    )
    echo += click.style(click.format_filename(rc_file), fg=color2, bold=True)
    echo += click.style(". Please refresh your shell.", fg=color1, bold=True)
    click.echo(echo)
    click.echo(
        click.style(
            "Example:",
            bold=True,
        )
    )
    click.echo()
    click.echo("exec $SHELL")
    click.echo()
    click.echo(click.style("or:", bold=True))
    click.echo()
    click.echo(f"{rc_add}")


def add_utils_to_path() -> None:
    """Add the utilities directory to the PATH environment variable."""
    shell = os.environ.get("SHELL", "")
    if shell == "":
        echo = click.style("No shell detected.", fg="red", bold=True)
        echo += "\n"
        echo += click.style(
            " Please add the utilities directory to your PATH manually."
        )
        echo += "\n"
        echo += click.style(
            "Example:",
            bold=True,
        )
        echo += "\n    export PATH=$PATH:~/.local/share/utils/bin"
        raise click.ClickException(echo)
    else:
        shell = Path(shell).stem
        rc_file: Path = Path()
        rc_text: str = ""
        rc_add: str = ""
        match shell:
            case "sh":
                rc_file = Path.home() / ".profile"
                rc_text = shrc
                rc_add = shadd
            case "bash":
                rc_file = Path.home() / ".bashrc"
                rc_text = bashrc
                rc_add = shadd
            case "zsh":
                rc_file = Path.home() / ".zshrc"
                rc_text = bashrc
                rc_add = shadd
            case "fish":
                rc_file = Path.home() / ".config" / "fish" / "config.fish"
                rc_text = fishrc
                rc_add = fishadd
            case "nu":
                rc_file = get_config_dir() / "nushell" / "config.nu"
                rc_text = nurc
                rc_add = nuadd
            case _:
                echo = click.style(
                    f"Unsupported shell: {click.format_filename(shell)}.",
                    fg="red",
                    bold=True,
                )
                echo += click.style(
                    "\nPlease add the utilities directory to your PATH manually."
                )
                raise click.ClickException(echo)
        # Ensure the shell config exists
        if not rc_file.exists() or not rc_file.is_file():
            if not rc_file.parent.exists() or not rc_file.parent.is_dir():
                rc_file.parent.mkdir(parents=True, exist_ok=True)
            rc_file.touch()
        with click.open_file(rc_file, "r") as f:
            for line in f:
                if rc_text.splitlines()[0] in line:
                    echo_added_to_rc(rc_file, rc_add, True)
                    return
        with click.open_file(rc_file, "a") as f:
            f.write(rc_text)
        echo_added_to_rc(rc_file, rc_add, False)
