import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG  # Importa configurações do banco de dados

def conectar_banco():
    """Estabelece conexão com MySQL."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None

def criar_tabela_pessoas():
    """Cria a tabela 'pessoas' no banco de dados."""
    conn = conectar_banco()
    if not conn:
        print("⚠️ Falha ao conectar ao banco.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_completo VARCHAR(200) NOT NULL,
                doc_identidade VARCHAR(50),
                titulo_eleitor VARCHAR(50),
                telefone VARCHAR(30),
                endereco TEXT
            );
        """)
        conn.commit()
        print("✅ Tabela 'pessoas' criada ou já existe.")
    
    except Error as e:
        print(f"❌ Erro ao criar tabela: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    criar_tabela_pessoas()
