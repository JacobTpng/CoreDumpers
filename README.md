# CoreDumpers
564 Capstone Project

# Spring4Shell‑Capstone (CS564 Cyber Effects)

> One‑command demo: pop a vulnerable Spring app, implant a beacon, and see tasking in operator console, all on laptop.
>
> **For local‑network laboratories only.  Do *NOT* aim the exploit at public hosts.**

---
# Instructions

```bash
# 1. clone & install deps
$ git clone https://github.com/JacobTpng/CoreDumpers.git
$ pip install -r requirements
# or
$ pip install -r .github/workflows/requirements.txt

# IF ON LINUX - may have to run
$ chmod +x /scripts/run_all.sh
$ chmod +x /scripts/cleanup.sh
# to make the start and clean scripts executable

# IF NOT ON LINUX - Open Git Bash as well as Docker for desktop, and run (from the main directory):
$ ./scripts/run_all.sh
# This will start up the vulnerable tomcat docker container that we will attack. 

#TODO: This is where the exploit code needs to start the implant so that it can communicate with the C2. 

# It will also start the C2 server, and wait for the handshake, which should have no issues if the implant brings it up properly. 

# TO CLEAN UP, run:
$ ./scripts/cleanup.sh



