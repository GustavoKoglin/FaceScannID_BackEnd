import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configuração melhorada com tratamento para MySQL 8+
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),  # Removida senha padrão
    "database": os.getenv("DB_NAME", "FSID"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "auth_plugin": 'mysql_native_password',  # Essencial para MySQL 8+
    "raise_on_warnings": True  # Melhora o tratamento de avisos
}

def conectar_banco():
    """Conecta ao MySQL e retorna a conexão com tratamento aprimorado de erros."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conexão estabelecida com sucesso")
        return conn
    except Error as e:
        print(f"❌ Erro ao conectar: {e}")
        # Mostra a configuração sem expor a senha
        config_safe = DB_CONFIG.copy()
        config_safe['password'] = '*****' if config_safe['password'] else 'None'
        print(f"Configuração usada: {config_safe}")
        return None

def criar_tabela():
    """Cria a tabela 'pessoas' com tratamento transacional e UTF-8."""
    conn = conectar_banco()
    if not conn:
        return False
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        # Query com encoding explícito
        create_query = """
            CREATE TABLE IF NOT EXISTS pessoas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_completo VARCHAR(200) NOT NULL,
                doc_identidade VARCHAR(50),
                titulo_eleitor VARCHAR(50),
                cpf VARCHAR(20) UNIQUE,  # Evita CPFs duplicados
                telefone VARCHAR(30),
                email VARCHAR(100),
                endereco TEXT,
                numero VARCHAR(10),
                complemento VARCHAR(50),
                bairro VARCHAR(50),
                cidade VARCHAR(50),
                estado VARCHAR(2),
                cep VARCHAR(10),
                pais VARCHAR(50),
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP  # Campo adicional útil
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        cursor.execute(create_query)
        conn.commit()
        print("✅ Tabela 'pessoas' criada/verificada com sucesso")
        return True
        
    except Error as e:
        print(f"❌ Erro ao criar tabela: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def testar_conexao():
    """Testa a conexão com o banco de dados."""
    return conectar_banco() is not None

if __name__ == "__main__":
    if testar_conexao():
        criar_tabela()