#!/usr/bin/env bash

# This script installs the necessary dependencies for the project.
# It is intended to be run in a Unix-like environment.
# Usage: ./install.sh

set -eo pipefail

CYAN='\033[0;36m'
BOLD_RED='\033[1;31m'
RESET='\033[0m'

install_uv() {
  if command -v curl &>/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
  elif command -v wget &>/dev/null; then
    wget -qO- https://astral.sh/uv/install.sh | sh
  elif command -v wget2 &>/dev/null; then
    wget2 -qO- https://astral.sh/uv/install.sh | sh
  else
    >&2 echo -e "${BOLD_RED}Error${RESET}: ${CYAN}curl${RESET}, ${CYAN}wget${RESET}, or ${CYAN}wget2${RESET} is required to install."
    exit 1
  fi

  if [ -n "${UV_INSTALL_DIR:-}" ]; then
    export UV_INSTALL_DIR="${UV_INSTALL_DIR}"
  elif [ -n "${CARGO_DIST_FORCE_INSTALL_DIR:-}" ]; then
    export UV_INSTALL_DIR="${CARGO_DIST_FORCE_INSTALL_DIR}"
  elif [ -n "${UNMANAGED_INSTALL}" ]; then
    export UV_INSTALL_DIR="${UNMANAGED_INSTALL}"
  elif [ -n "${XDG_BIN_HOME:-}" ]; then
    export UV_INSTALL_DIR="${XDG_BIN_HOME}"
  elif [ -n "${XDG_DATA_HOME:-}" ]; then
    export UV_INSTALL_DIR="${XDG_DATA_HOME}/../bin"
  elif [ -n "${HOME:-}" ]; then
    export UV_INSTALL_DIR="$HOME/.local/bin"
  else
    >&2 echo -e "${BOLD_RED}Error${RESET}: Unable to determine installation directory. Please set ${CYAN}XDG_BIN_HOME${RESET}, ${CYAN}XDG_DATA_HOME${RESET}, or ${CYAN}HOME${RESET} environment variable."
    exit 1
  fi

  source "${UV_INSTALL_DIR}/env" || {
    >&2 echo -e "${BOLD_RED}Error${RESET}: Failed to source ${CYAN}${UV_INSTALL_DIR}/env${RESET}. Please check your installation."
    exit 1
  }

  if ! command -v uv &>/dev/null; then
    >&2 echo -e "${BOLD_RED}Error${RESET}: ${CYAN}uv${RESET} installation failed. Please check your environment."
    exit 1
  fi
}

if ! command -v uv &>/dev/null; then
  install_uv
fi

if ! uv tool install --compile-bytecode git+https://github.com/annie444/utils-util; then
  >&2 echo -e "${BOLD_RED}Error${RESET}: Failed to install ${CYAN}utils${RESET}. Please check your network connection or repository URL."
  exit 1
else
  echo -e "${CYAN}utils${RESET} installed successfully!"
fi
