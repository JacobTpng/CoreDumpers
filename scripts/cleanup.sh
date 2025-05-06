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
#!/usr/bin/env bash

# Exit on any error
set -euo pipefail

#stop C2 server 
echo "[+] Stopping C2 server..."
if [[ -n "${C2_PID:-}" ]]; then
  kill "$C2_PID" || true
fi
#Fallback: kill remaining C2 processes
pkill -f "python3 -m c2.c2_server" || true

# Teardown Docker containers 
echo "[+] Shutting down containers..."
docker-compose down

#Prune unused Docker resources 
echo "[+] Pruning Docker volumes and networks..."
docker system prune -f

echo "[+] cleanup.sh complete."}