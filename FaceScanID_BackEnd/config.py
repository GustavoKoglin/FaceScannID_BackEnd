"""
Arquivo: config.py
Descrição:
    - Define constantes e variáveis utilizadas em todo o projeto.
    - Em um ambiente de produção, considere o uso de variáveis de ambiente
      para armazenar credenciais e caminhos sensíveis.
"""

# Carrega as variáveis do arquivo .env
import os
from dotenv import load_dotenv

# Agora podemos acessar com os.getenv
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "***********")
DB_NAME = os.getenv("DB_NAME", "FSID")
DB_PORT = int(os.getenv("DB_PORT", 3306))

# Caminhos principais
# Diretório onde estão as imagens de rostos a serem reconhecidos
FACE_DATA_PATH = "data/faces"

# Diretório onde salvaremos as representações (embeddings) do DeepFace
EMBEDDINGS_DIR = "data/embeddings"

# Arquivo global de embeddings do DeepFace
GLOBAL_EMBEDDINGS_FILE = "data/embeddings/generate_encodings.pkl"

# Diretório para salvar modelos ou dados extras (se necessário)
MODELS_PATH = "models"

# Nome (ou tipo) do modelo padrão do DeepFace que será usado
DEEPFACE_MODEL = "VGG-Face"
# Exemplos: "Facenet", "Facenet512", "ArcFace", "SFace", etc.

"""
Observação:
    - Caso você queira mudar para outro modelo do DeepFace, basta alterar DEEPFACE_MODEL.
    - Se quiser armazenar as representações com outro nome de arquivo, mude GLOBAL_EMBEDDINGS_FILE.
    - Para um ambiente real, remova a senha do banco (DB_PASSWORD) e armazene em variáveis de ambiente,
      usando, por exemplo, os módulos 'os' e 'dotenv'.
"""
