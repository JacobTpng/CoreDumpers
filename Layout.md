# Project Layout & File Roles  
Reference this to understand the layout and use of all files contained. 


# Top‑level overview
```
spring4shell-capstone/
│   README.md           - 60‑second build/run cheatsheet for graders
│   Layout.md-          - **this file**
│   .gitignore          - excludes build artifacts, venvs, secrets
│   docker-compose.yml  - brings up vulnerable Spring app + DB
│
├── docs/               - design docs, slides, demo logs
├── vuln-lab/           - Docker recipe for vulnerable Tomcat‑Spring
├── exploit/            - Spring4Shell weaponised exploit chain
├── common/             - code shared by implant & C2 (crypto / JSON)
├── implant/            - field implant that runs on the target host
├── c2/                 - command‑and‑control server & implant UI
├── scripts/            - helper shell scripts (launch, cleanup …)
└── tests/              - pytest unit + end‑to‑end checks
```

# detailed breakdown
---

## `/docs`
| File / sub‑dir                 
|---------------------------------
| `design.md`           | Threat‑model, crypto decisions, protocol spec.      
| `slides/`             | Final presentation                              
| `video_link.txt`      | Single line: link to presentation

---

## `/vuln-lab`
| File                 
|-----------------------
| `Dockerfile`         | Builds Ubuntu + JDK 11 + Tomcat 9 + vulnerable Spring 5.3.15 WAR. SHOULD ONLY RUN LOCALLY
| `build.sh`           | Convenience script (`docker build && docker run …`), creates image tag `spring4shell-lab:latest`

---

## `/exploit`
| File                 
|-------------------------
| `poc_orig.py`          | Vanilla public PoC kept _read‑only_ for citation from github. Shouldn't be executed in our pipeline, just reference
| `stage0_exploit.py`    | checks version, writes `payload.jsp`, triggers stager, called by `scripts/run_all.sh`
| `payload.jsp`          | 9‑line JSP stager - `curl` the implant & exec, lands on the vulnerable server during exploitation

---

## `/common`
Shared helper code so that implant and C2 server dont drift

| File            
|------------------
| `protocol.py`   | Defines JSON schema (`{nonce,cmd,payload}`) plus `encode()/decode()` helpers
| `crypto_lib.py` | ECDH key‑exchange + AES‑GCM encrypt/decrypt wrappers

Write unit tests for both in `/tests` so refactors are safe.
---

## `/implant`
| File / sub‑dir  |
|------------------
| `implant.py`    | Main loop: handshake → long‑poll → execute tasks → respond. Packed with PyInstaller by `build.sh`
| `persist/`      | OS‑specific persistence (e.g., `install_user_service.sh`, `add_run_key.ps1`). Called by `payload.jsp` post‑download
| `build.sh`      | Creates `implant.exe` (Windows) or statically linked ELF (Linux). Run on dev box; artefact not checked into git. 

---

## `/c2`
| File            
|--------------------
| `c2_server.py`    | Flask app: `/handshake`, `/tasks`, `/results` endpoints; SQLite storage. 
| `implant.py`  | Rich‑TUI (or web) for live tasking; calls REST locally. 
| `crypto_utils.py` | Thin shim that just `import common.crypto_lib` (kept for legacy). 

Run: `python c2/c2_server.py` and `python c2/implant.py` to get them up 
---

## `/scripts`
| Script           
|-------------------
| `run_all.sh`     | brings up lab container, starts C2, launches exploit
| `cleanup.sh`     | Stops containers, kills C2, prunes volumes

---

## `/tests`
| Test file                  
|----------------------------------
| `test_protocol.py`         | Round‑trip encode/decode and AES‑GCM decrypt matches plaintext
| `test_exploit_e2e.py`      | Spins up lab via docker → runs `stage0_exploit.py` → waits for implant beacon

Can run with `pytest -q` locally
---

### Glossary
* **Stager** – tiny first payload whose only job is to download the real implant.
* **Beacon** – the periodic HTTPS POST the implant sends to ask for tasks.
* **ECDH** – Elliptic‑Curve Diffie‑Hellman; used to derive per‑session key.

---

Last updated: April 25 2025

