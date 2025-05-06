# Project Layout & File Roles  
Reference this to understand the layout and use of all files contained. 


# Top‑level overview
```
spring4shell-capstone/
│   README.md           - 60‑second build/run cheatsheet for graders
│   .gitignore          - excludes build artifacts, venvs, secrets
│   docker-compose.yml  - brings up vulnerable Spring app + DB
|   .dockerignore       - resources for docker to ignore to prevent conflicts and increase efficiency
│
├── .github/            - github coms to setup lab environment for vulnerable target
├── docs/               - design docs, slides, demo logs
├── vuln-lab/           - Docker recipe for vulnerable Tomcat‑Spring
├── exploit/            - Spring4Shell weaponised exploit chain
├── common/             - code shared by implant & C2 (crypto / JSON)
├── .pytest_cache       - resources form downloading and using pytest for test functions
├── c2/                 - command‑and‑control server & implant UI, including implant file
├── scripts/            - helper shell scripts (launch, cleanup …)
└── tests/              - pytest unit + end‑to‑end checks
```

# detailed breakdown
---

## `.github`
| File / sub‑dir                 
|---------------------------------
| `worflow/ci.yml`   | github actions to setup and run fresh lab environment to use implant on. This lab runs pytest (which calls stage0_exploit.py, waits for the implant beacon, checks C2 API, etc.)
| `rewuirements.txt` | version requirements for .yml file like pytest~=8.2, cryptography~=42.0, Flask~=3.0, etc

## `/docs`
| File / sub‑dir                 
|---------------------------------
| `design.md`           | Threat‑model, crypto decisions, protocol spec.  
| `Layout.md`           | This file    
| `slides/`             | Final presentation                              
| `video_link.txt`      | Single line: link to presentation

---

## `/vuln-lab`
| File                 
|-----------------------
| `Dockerfile`         | Builds Ubuntu + JDK 11 + Tomcat 9 + vulnerable Spring 5.3.15 WAR. SHOULD ONLY RUN LOCALLY
| `build.sh`           | Convenience script (`docker build && docker run …`), creates image tag `spring4shell-lab:latest`
| `app.war`            | Pre-built Spring-Boot.2.6.4 WAR vulnerable to Spring4Shell CVE from https://github.com/sinjap/spring4shell/tree/main repo
| `README.txt`         | Instructions to run to lab environment and close it

---

## `/exploit`
| File                 
|-------------------------
| `poc`                  | Vanilla public PoC kept _read‑only_ for citation from github. Shouldn't be executed in our pipeline, just reference. From https://github.com/entropyqueen/spring4shell-demo
| `stage0_exploit.py`    | checks version, writes `payload.jsp`, triggers stager, called by `scripts/run_all.sh`
| `payload.jsp`          | JSP stager - downloads and launches the Python implant

---

## `/common`
| File            
|------------------
| `protocol.py`   | JSON envelope for encode_message / decode_message.
| `crypto_lib.py` | X25519 keypair + HKDF to AES‑GCM encrypt/decrypt

---

## `/c2`
| File            
|--------------------
| `c2_server.py`    | Flask app exposing endpoints: handshake, tasking, exfil, admin.
| `static/`         | Public static files served at /static - HOLDS implant.py with Rich‑TUI (or web) for live tasking; calls REST locally
| `__init__.py`     | marks c2 and implant.py as python package for imports 

Run: `python -m c2.c2_server` and `python -m c2.static.implant` to get them up (can replace with python3 or any other local version) since we're using __init__.py locators to put them on import path.
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

Last updated: May 5 2025

