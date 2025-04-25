#!/usr/bin/env bash
# ---------------------------------------------------------------
# cleanup.sh – Tear-down helper for demo / CI pipeline
# ---------------------------------------------------------------
# • Stops and removes the vuln-lab Docker container
# • Kills the local C2 server if it’s running under this UID
# • Removes temp logs & PyInstaller build artefacts
#
# Usage
#   ./scripts/cleanup.sh
#
# Called automatically by GitHub Actions at the end of e2e tests.
# ---------------------------------------------------------------
set -e
docker rm -f spring_lab 2>/dev/null || true
pkill -f "python .*c2_server.py" 2>/dev/null || true
rm -rf implant/build/ implant/dist/ *.log
echo "[+] Environment tidied."
