"""
test_protocol.py – unit-tests for JSON/crypto envelope
=====================================================

Run it
------
$ python -m pytest tests/test_protocol.py -q

No Docker or network needed
"""
# tests/test_protocol.py

import pytest
from common.crypto_lib import generate_keypair, derive_key, aes_gcm_encrypt, aes_gcm_decrypt
import json
from common.protocol import encode_message, decode_message

def test_ecdh_shared_key_consistency():
    # Alice and Bob each generate a keypair
    a_priv, a_pub = generate_keypair()
    b_priv, b_pub = generate_keypair()

    # They compute the shared secret
    key_ab = derive_key(a_priv, b_pub)
    key_ba = derive_key(b_priv, a_pub)

    assert key_ab == key_ba, "ECDH-derived keys must match"

@pytest.mark.parametrize("plaintext", [b"", b"hello", b"a"*1024])
def test_aes_gcm_roundtrip(plaintext):
    # Use a fresh key each time (or reuse key_ab)
    _, pub = generate_keypair()
    # derive a dummy key for testing
    key = derive_key(*generate_keypair())  
    ct = aes_gcm_encrypt(key, plaintext)
    pt = aes_gcm_decrypt(key, ct)
    assert pt == plaintext, "AES-GCM round trip must recover original"

def test_protocol_envelope_roundtrip():
    envelope = {
        "sid": "test-session",
        "seq": 42,
        "cmd": "exec",
        "body": {"cmd": "whoami"},
        # optional fields may be present
    }
    encoded = encode_message(**envelope)
    decoded = decode_message(encoded)

    # Ensure all fields are preserved
    for key, val in envelope.items():
        assert decoded[key] == val

def test_full_transport_cycle():
    # Setup ECDH keys & derive session key
    a_priv, a_pub = generate_keypair()
    b_priv, b_pub = generate_keypair()
    session_key = derive_key(a_priv, b_pub)

    # Build and encrypt a protocol message
    plaintext = encode_message(sid="S", seq=1, cmd="exfil", body="data")
    ciphertext = aes_gcm_encrypt(session_key, plaintext)

    # Decrypt then parse envelope
    recovered = aes_gcm_decrypt(session_key, ciphertext)
    envelope = decode_message(recovered)
    assert envelope["sid"] == "S" and envelope["cmd"] == "exfil"