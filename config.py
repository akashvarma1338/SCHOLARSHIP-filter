"""
Configuration settings for Scholarship Eligibility Filter
"""

import os
import secrets

# Generate a secure secret key if not provided
def generate_secret_key():
    return secrets.token_hex(32)

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'scholarship.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret key for session management - generates once and reuses
SECRET_KEY = os.environ.get('SECRET_KEY', 'scholarship-eligibility-secret-key-2024-production')

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '614974869577-deg382b8fhal3ir3f12v9p150bb15j4h.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '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')
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

# For development/demo mode
DEMO_MODE = os.environ.get('DEMO_MODE', 'True').lower() == 'true'

# Use simulated authentication for development
USE_SIMULATED_AUTH = os.environ.get('USE_SIMULATED_AUTH', 'False').lower() == 'true'
USE_SIMULATED_AUTH_STUDENT = os.environ.get('USE_SIMULATED_AUTH_STUDENT', 'False').lower() == 'true'
