#!/usr/bin/env bash
set -euo pipefail

export HOME="${HOME:-/home/jovyan}"
export JUPYTER_CONFIG_DIR="${JUPYTER_CONFIG_DIR:-${HOME}/.jupyter}"

cd /opt/mgnify

exec pixi run jupyter lab \
  --ip=0.0.0.0 \
  --port=8888 \
  --no-browser \
  --ServerApp.allow_origin='*' \
  --ServerApp.root_dir="${HOME}" \
  "$@"
