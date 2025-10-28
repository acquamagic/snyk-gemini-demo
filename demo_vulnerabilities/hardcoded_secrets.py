"""
⚠️  VULNERABLE CODE - FOR LIVE DEMO ONLY ⚠️

This file demonstrates hardcoded secrets and credentials.
USE THIS DURING THE LIVE DEMO to show:
1. Snyk MCP Server immediately flagging hardcoded secrets
2. Gemini suggesting environment variable usage
3. Best practices for secrets management

DO NOT USE IN PRODUCTION!
"""

from flask import Flask, request, jsonify, abort
import jwt
import hashlib

app = Flask(__name__)

# ========================================
# VULNERABILITY 1: Hardcoded Secret Keys
# ========================================

# 🔴 VULNERABLE: Hardcoded Flask secret key
SECRET_KEY = "my-super-secret-key-12345"
# Snyk MCP will flag: "Hardcoded secret detected"

# 🔴 VULNERABLE: Hardcoded JWT secret
JWT_SECRET = "hardcoded-jwt-secret-key-abc123"
# Snyk MCP will flag: "JWT secret should not be hardcoded"

# 🔴 VULNERABLE: Hardcoded API key
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
# Snyk MCP will flag: "API key should be in environment variables"


# ========================================
# VULNERABILITY 2: Hardcoded Database Credentials
# ========================================

# 🔴 VULNERABLE: Database credentials in code
DATABASE_CONFIG = {
    'host': 'production-db.example.com',
    'port': 5432,
    'user': 'admin',
    'password': 'Admin123!',  # 🔴 Snyk will flag this
    'database': 'production_db'
}

# 🔴 VULNERABLE: Connection string with credentials
DB_CONNECTION_STRING = "postgresql://admin:SuperSecret123@db.example.com:5432/mydb"
# Snyk MCP will flag: "Database credentials in connection string"


# ========================================
# VULNERABILITY 3: Hardcoded Cloud Credentials
# ========================================

# 🔴 VULNERABLE: AWS credentials
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
# Snyk MCP will flag: "AWS credentials should not be hardcoded"

# 🔴 VULNERABLE: Google Cloud service account key
GCP_SERVICE_ACCOUNT_KEY = {
    "type": "service_account",
    "project_id": "my-project",
    "private_key_id": "1234567890abcdef",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n-----END PRIVATE KEY-----\n",
    "client_email": "service@my-project.iam.gserviceaccount.com"
}


# ========================================
# VULNERABILITY 4: Hardcoded Encryption Keys
# ========================================

# 🔴 VULNERABLE: Hardcoded encryption key
ENCRYPTION_KEY = "0123456789abcdef0123456789abcdef"
# Snyk MCP will flag: "Encryption key should not be hardcoded"

# 🔴 VULNERABLE: Hardcoded salt for password hashing
PASSWORD_SALT = "hardcoded_salt_value_123"
# Snyk MCP will flag: "Salt should be randomly generated"


# ========================================
# VULNERABILITY 5: Hardcoded Third-Party API Keys
# ========================================

# 🔴 VULNERABLE: Third-party service keys
STRIPE_SECRET_KEY = "sk_live_1234567890abcdefghijklmnop"
SENDGRID_API_KEY = "SG.1234567890abcdefghijklmnopqrstuvwxyz"
TWILIO_AUTH_TOKEN = "1234567890abcdef1234567890abcdef"
OPENAI_API_KEY = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"
# Snyk MCP will flag all of these


# ========================================
# VULNERABILITY 6: Private Keys and Certificates
# ========================================

# 🔴 VULNERABLE: Private key in code
RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdefghijklmnopqrstuvwxyz...
-----END RSA PRIVATE KEY-----"""
# Snyk MCP will flag: "Private key should not be in source code"


# ========================================
# USING THE HARDCODED SECRETS (Shows in demo)
# ========================================

@app.route('/login', methods=['POST'])
def login():
    """
    🔴 VULNERABILITY: Using hardcoded JWT secret
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simplified auth (not the main issue here)
    if username == 'admin' and password == 'password':
        # 🔴 VULNERABLE: Using hardcoded JWT_SECRET
        token = jwt.encode(
            {'user': username, 'role': 'admin'},
            JWT_SECRET,  # This uses the hardcoded secret
            algorithm='HS256'
        )
        return jsonify({'token': token})
    
    abort(401, 'Invalid credentials')


@app.route('/api/data', methods=['GET'])
def get_data():
    """
    🔴 VULNERABILITY: Comparing with hardcoded API key
    """
    api_key = request.headers.get('X-API-Key')
    
    # 🔴 VULNERABLE: Comparing with hardcoded API_KEY
    if api_key == API_KEY:
        return jsonify({'data': 'sensitive information'})
    
    abort(401, 'Invalid API key')


@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    """
    🔴 VULNERABILITY: Using hardcoded encryption key
    """
    data = request.get_json()
    text = data.get('text', '')
    
    # 🔴 VULNERABLE: Using hardcoded ENCRYPTION_KEY
    # In reality, you'd use proper encryption library
    encrypted = hashlib.sha256((text + ENCRYPTION_KEY).encode()).hexdigest()
    
    return jsonify({'encrypted': encrypted})


# ========================================
# HOW TO FIX (Show this during demo with Gemini)
# ========================================

# ✅ SECURE VERSION - Using environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ SECURE: Load from environment
SECURE_SECRET_KEY = os.getenv('SECRET_KEY')
SECURE_JWT_SECRET = os.getenv('JWT_SECRET')
SECURE_API_KEY = os.getenv('API_KEY')

# ✅ SECURE: Database config from environment
SECURE_DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# ✅ SECURE: AWS credentials from environment
SECURE_AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECURE_AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


@app.route('/login-secure', methods=['POST'])
def login_secure():
    """
    ✅ SECURE VERSION
    Gemini will suggest this pattern.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == 'password':
        # ✅ SECURE: Using environment variable
        jwt_secret = os.getenv('JWT_SECRET')
        if not jwt_secret:
            abort(500, 'Server configuration error')
        
        token = jwt.encode(
            {'user': username, 'role': 'admin'},
            jwt_secret,
            algorithm='HS256'
        )
        return jsonify({'token': token})
    
    abort(401, 'Invalid credentials')


if __name__ == '__main__':
    print("⚠️  WARNING: This is vulnerable code for demo purposes only!")
    print("    DO NOT USE IN PRODUCTION")
    print("\n🔴 Hardcoded secrets detected in this file:")
    print("    - SECRET_KEY")
    print("    - JWT_SECRET")
    print("    - API_KEY")
    print("    - Database credentials")
    print("    - AWS credentials")
    print("    - GCP service account key")
    print("    - Encryption keys")
    print("\n✅ Use environment variables instead!")
    app.run(debug=True, port=5002)