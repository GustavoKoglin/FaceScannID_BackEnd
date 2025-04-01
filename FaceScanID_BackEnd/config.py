"""
CONFIG.PY - Global Project Configuration
- Defines constants and global configurations
- Uses environment variables for sensitive data
- Configures database, DeepFace, and paths
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables
load_dotenv()

# Project root directory (more reliable way to get it)
PROJECT_ROOT = Path(__file__).parent

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Gbk@2027"),
    "database": os.getenv("DB_NAME", "FSID"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "auth_plugin": 'mysql_native_password'
}

# Directory Structure
DIRECTORIES = {
    'data': PROJECT_ROOT / 'data',
    'faces': PROJECT_ROOT / 'data' / 'faces',
    'embeddings': PROJECT_ROOT / 'data' / 'embeddings',
    'models': PROJECT_ROOT / 'models',
    'temp': PROJECT_ROOT / 'temp'
}

# File Paths
FILES = {
    'encodings': DIRECTORIES['embeddings'] / 'deepface_encodings.pkl',
    'representations': DIRECTORIES['embeddings'] / 'deepface_representations.pkl'
}

# DeepFace Configuration
DEEPFACE_CONFIG = {
    'model_name': "VGG-Face",
    'detector_backend': "opencv",
    'distance_metric': "cosine",
    'enforce_detection': True,
    'align': True
}

def initialize_directories():
    """Create required directories if they don't exist"""
    for dir_path in DIRECTORIES.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory ensured: {dir_path}")

def test_database_connection():
    """Test database connection with error handling"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Database connection successful")
        conn.close()
        return True
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        print(f"Configuration used: {DB_CONFIG}")
        return False

# Initialize the project environment
initialize_directories()
test_database_connection()