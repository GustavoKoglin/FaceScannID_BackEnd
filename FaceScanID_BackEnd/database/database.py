# database/database.py
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# ---------------------------------------------------------------------------
# Gerencia a conexão e criação da tabela 'pessoas' com as novas colunas.
# ---------------------------------------------------------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "sua_senha"),
    "database": os.getenv("DB_NAME", "FSID"),
    "port": int(os.getenv("DB_PORT", 3306))
}
def conectar_banco():
    """Estabelece uma conexão com o MySQL usando DB_CONFIG."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"❌ Erro ao conectar no MySQL: {e}")
        return None

def criar_tabela():
    """
    Cria a tabela 'pessoas' com todas as colunas solicitadas.
    Caso já exista, apenas mantém.
    """
    conn = conectar_banco()
    if not conn:
        print("❌ Falha na conexão com o banco de dados. Tabela não foi criada.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_completo VARCHAR(200) NOT NULL,
                doc_identidade VARCHAR(50),
                titulo_eleitor VARCHAR(50),
                certidao_militar VARCHAR(50),
                possui_registro_classe VARCHAR(3),  -- Sim ou Não
                numero_registro_classe VARCHAR(50),
                pis_pasep VARCHAR(50),
                tipo_sanguineo VARCHAR(10),
                telefone VARCHAR(30),
                endereco TEXT,
                emails TEXT,
                possui_imoveis VARCHAR(3),  -- Sim ou Não
                tipo_imovel VARCHAR(20),
                registro_imovel VARCHAR(50),
                endereco_imovel TEXT,
                possui_veiculos VARCHAR(3), -- Sim ou Não
                tipo_veiculo VARCHAR(30),
                marca_veiculo VARCHAR(30),
                registro_veiculo VARCHAR(50),
                possui_parente VARCHAR(3),  -- Sim ou Não
                nome_parente VARCHAR(100),
                doc_parente VARCHAR(50),
                telefone_parente VARCHAR(50),
                endereco_parente TEXT
            );
        """)
        conn.commit()
        print("✅ Tabela 'pessoas' criada ou já existia.")
    except Error as err:
        print(f"❌ Erro ao criar tabela: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    criar_tabela()
