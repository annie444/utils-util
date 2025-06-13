set unstable

bash-init := """
if [ -n "${DEBUG:-}" ]; then
  set -x
fi
set -euo pipefail
"""

mod vm 'vms/justfile'

default:
  just --choose --list-submodules

run *args:
  uv run utils -- {{ args }}
