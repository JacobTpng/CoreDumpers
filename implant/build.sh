#!/usr/bin/env bash
# ------------------------------------------------------------------
# build.sh  –  Produce the stand-alone implant binary
# ------------------------------------------------------------------
# 1. Creates a Python virtual-env (if absent)
# 2. Installs dependencies from ../../requirements.txt
# 3. Uses PyInstaller to generate a single-file executable
# 4. Drops output to  ../dist/implant_<platform>
#
# Usage
# -----
# $ cd implant
# $ ./build.sh
#
# Notes
# -----
# • PyInstaller AES-encrypts the byte-code with the key in
#   PYINSTALLER_KEY (export env var for deterministic builds).
# • For Windows cross-builds run this script **inside** a Win VM.
# ------------------------------------------------------------------
set -e
