#crypto_utils.py
# Provides functions to encrypt and decrypt messages with AES in CBC mode.
# Uses cryptography library to handle cryptographic operations,
# PKCS7 padding, and a random IV for each message.
# After padding and IV, concatenates the IV with the ciphertext, and returns result in base64 encoding

from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

# THE secret key used for AES encryption/decryption
KEY = b'ThisIsASecretKey'  # AES-128 using a 16-byte key

def encrypt_message(plaintext):
    # Generate random IV
    iv = os.urandom(16)
    # create padder for 16 byte / 128 bit block size
    padder = padding.PKCS7(128).padder()
    # Pad plaintext to block size
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    # create AES-CBC cipher object with the KEY and IV
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Encrypt padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    #concatenate IV and ciphertext and encode as base64 string
    return base64.b64encode(iv + ciphertext).decode()

def decrypt_message(ciphertext_b64):
    """
    Decodes the base64 string, extracts IV, decrypts ciphertext,
    and removes PKCS7 padding to return original plaintext.
    """
    # Decode base64 string for raw bytes
    raw = base64.b64decode(ciphertext_b64.encode())
    #first 16 bytes are the IV
    iv = raw[:16]
    ciphertext = raw[16:]
    # Create cipher object for decryption using the same key and IV
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    # Decrypt ciphertext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    # remove padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

