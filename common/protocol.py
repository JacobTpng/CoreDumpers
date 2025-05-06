"""
Common protocol helpers
-----------------------
Defines the JSON envelope shared by implant and C2.

Fields
  • sid : session UUID (base64url)
  • seq : uint32 monotonic counter
  • cmd : string task verb
  • body: arbitrary JSON data (encrypted)

All functions here must stay *perfectly* in sync on both sides.

Author       : capstone-team
Dependencies : cryptography, msgpack
"""
import json
import time

def encode_message(sid: str, seq: int, cmd: str, body) -> bytes:
    """
    Build and serialize a protocol envelope.

    Args:
      sid  – session identifier
      seq  – sequence counter (monotonic)
      cmd  – command string ("task", "exfil", etc.)
      body – payload (JSON-serializable)

    Returns:
      UTF-8 encoded JSON bytes
    """
    envelope = {
        "sid": sid,
        "seq": seq,
        "cmd": cmd,
        "body": body,
        "ts": int(time.time())
    }
    return json.dumps(envelope).encode('utf-8')


def decode_message(blob: bytes) -> dict:
    """
    Parse and return fields from a protocol envelope.

    Args:
      blob – UTF-8 encoded JSON bytes containing the envelope

    Returns:
      dict with keys 'sid', 'seq', 'cmd', 'body', 'ts'
    """
    data = json.loads(blob.decode('utf-8'))
    # Validate required fields
    for field in ('sid', 'seq', 'cmd', 'body'):
        if field not in data:
            raise ValueError(f"Missing required protocol field: {field}")
    return data
