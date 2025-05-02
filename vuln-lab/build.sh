#!/usr/bin/env bash
# ------------------------------------------------------------------
# build.sh – Convenience wrapper for the vulnerable Spring-Boot lab
# ------------------------------------------------------------------
# Builds the Docker image defined by Dockerfile and tags it
#   spring4shell/lab:latest
#
# Usage
#   ./build.sh          # build only
#   ./build.sh run      # build + run container on port 8080
#
# WARNING: The resulting container is intentionally vulnerable; keep
# it bound to 127.0.0.1 or an isolated VM network.
# ------------------------------------------------------------------
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
docker build -t spring4shell/lab:latest "$SCRIPT_DIR"

if [[ "$1" == "run" ]]; then
  docker run -d --rm -p 8080:8080 --name spring_lab spring4shell/lab:latest
  echo "[+] Lab running at http://127.0.0.1:8080/ (ctrl-c to stop)"
fi
