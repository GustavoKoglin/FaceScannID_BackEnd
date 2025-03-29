"""
ARQUIVO: CONFIG.PY
DESCRIÇÃO:
    - DEFINE CONSTANTES E CONFIGURAÇÕES GLOBAIS DO PROJETO
    - UTILIZA VARIÁVEIS DE AMBIENTE PARA DADOS SENSÍVEIS
    - CONFIGURAÇÕES PARA BANCO DE DADOS, DEEPFACE E CAMINHOS
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# CARREGA VARIÁVEIS DE AMBIENTE
load_dotenv()

# CONFIGURAÇÕES DO BANCO DE DADOS
DB_CONFIG = {
  "host": os.getenv("DB_HOST", "localhost"),  # Note: chaves em minúsculo
  "user": os.getenv("DB_USER", "root"),
  "password": os.getenv("DB_PASSWORD", "Gbk@2027"),  # Verifique esta senha
  "database": os.getenv("DB_NAME", "FSID_DEV"),
  "port": int(os.getenv("DB_PORT", 3306)),
  "auth_plugin": 'mysql_native_password'  # Padronizado para minúsculo
}

# CAMINHOS DO PROJETO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

PATHS = {
    'FACE_DATA': os.path.join(DATA_DIR, 'faces'),
    'EMBEDDINGS': os.path.join(DATA_DIR, 'embeddings'),
    'GLOBAL_EMBEDDINGS': os.path.join(DATA_DIR, 'embeddings', 'encodings.pkl'),
    'MODELS': os.path.join(BASE_DIR, 'models')
}

# CONFIGURAÇÕES DO DEEPFACE
DEEPFACE_CONFIG = {
  'MODEL_NAME': "VGG-Face",
  'DETECTOR_BACKEND': "opencv",
  'DISTANCE_METRIC': "cosine",
  'ENFORCE_DETECTION': True,
  'ALIGN': True
}

def testar_conexao():
    """Testa a conexão com o banco de dados"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conexão bem-sucedida com o banco de dados")
        conn.close()
        return True
    except Error as e:
        print(f"❌ Falha na conexão: {e}")
        print(f"Configuração usada: {DB_CONFIG}")
        return False

# CRIAÇÃO DE DIRETÓRIOS SE NÃO EXISTIREM
for PATH in PATHS.values():
    if not os.path.exists(PATH):
        os.makedirs(PATH)
        print(f"DIRETÓRIO CRIADO: {PATH}")

    testar_conexao()