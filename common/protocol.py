<<<<<<< HEAD
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

=======
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

>>>>>>> 1cdb7db12f4a3f70cf3ad0ae6c32187fc3938f1b
