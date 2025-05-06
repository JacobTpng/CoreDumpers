"""
crypto_lib.py – Thin wrapper around X25519 + AES-GCM
====================================================
Abstracts:
  * keypair generation
  * ECDH shared-secret → HKDF
  * aes_gcm_encrypt / aes_gcm_decrypt

DO NOT log clear-text; use DEBUG_SECRET env var for test dumps.

"""
import os, base64
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Length of derived AES key (32 bytes → AES-256)
HKDF_LENGTH = 32

def generate_keypair():
    """
    Returns:
      priv_bytes (bytes): X25519 private key (raw, 32-byte)
      pub_bytes  (bytes): X25519 public key  (raw, 32-byte)
    """
    priv = X25519PrivateKey.generate()
    pub  = priv.public_key()
    priv_bytes = priv.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_bytes = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return priv_bytes, pub_bytes

def derive_key(priv_bytes: bytes, peer_pub_bytes: bytes) -> bytes:
    """
    ECDH key exchange + HKDF to derive a symmetric key.
    Args:
      priv_bytes     – your raw X25519 private key
      peer_pub_bytes – peer’s raw X25519 public key
    Returns:
      32-byte session key for AES-GCM
    """
    priv     = X25519PrivateKey.from_private_bytes(priv_bytes)
    peer_pub = X25519PublicKey.from_public_bytes(peer_pub_bytes)
    shared   = priv.exchange(peer_pub)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=HKDF_LENGTH,
        salt=None,
        info=b"capstone handshake",
    )
    return hkdf.derive(shared)

def aes_gcm_encrypt(key: bytes, plaintext: bytes) -> bytes:
    """
    AES-GCM encrypt, prefixing a 12-byte nonce.
    Args:
      key       – 32-byte AES key
      plaintext – data to encrypt
    Returns:
      nonce || ciphertext || tag
    """
    aesgcm = AESGCM(key)
    nonce  = os.urandom(12)
    ct     = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    return nonce + ct

def aes_gcm_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """
    AES-GCM decrypt; expects nonce prefixed.
    Args:
      key        – 32-byte AES key
      ciphertext – nonce || ct || tag
    Returns:
      original plaintext
    """
    aesgcm = AESGCM(key)
    nonce, ct = ciphertext[:12], ciphertext[12:]
    return aesgcm.decrypt(nonce, ct, associated_data=None)
