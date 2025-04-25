"""
crypto_lib.py – Thin wrapper around X25519 + AES-GCM
====================================================
Abstracts:
  * keypair generation
  * ECDH shared-secret → HKDF
  * aes_gcm_encrypt / aes_gcm_decrypt

DO NOT log clear-text; use DEBUG_SECRET env var for test dumps.

"""

