import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "sua_senha"),
    "database": os.getenv("DB_NAME", "FSID"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def conectar_banco():
    """Conecta ao MySQL e retorna a conexão."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None

def adicionar_pessoa_exemplo():
    """Adiciona uma pessoa de exemplo no banco."""
    conn = conectar_banco()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO pessoas (
                nome_completo, 
                doc_identidade, 
                titulo_eleitor, 
                certidao_militar,
                possui_registro_classe, 
                numero_registro_classe, 
                pis_pasep,
                tipo_sanguineo, 
                telefone, 
                endereco, 
                emails,
                possui_imoveis, 
                tipo_imovel, 
                registro_imovel, 
                endereco_imovel,
                possui_veiculos, 
                tipo_veiculo, 
                marca_veiculo, 
                registro_veiculo,
                possui_parente, 
                nome_parente, 
                doc_parente, 
                telefone_parente, 
                endereco_parente
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            "Céline Dion",
            "RG445566",
            "TE223344",
            "CertMil777",
            "Sim",
            "CR445566",
            "789.12345.67-8",
            "O+",
            "1195555-4444",
            "Rua das Palmeiras, 250 - Centro",
            "maria.oliveira@example.com",
            "Não",    # possui_imoveis
            "",       # tipo_imovel
            "",       # registro_imovel
            "",       # endereco_imovel
            "Sim",    # possui_veiculos
            "Carro",
            "Chevrolet",
            "DEF-2468",
            "Sim",    # possui_parente
            "João Oliveira",
            "RG778899",
             "11933332222",
            "Rua dos Coqueiros, 100 - Jardim Primavera"
        )
        cursor.execute(sql, valores)
        conn.commit()
        print("✅ Pessoa adicionada com sucesso!")

    except Error as e:
        print(f"Erro ao inserir dados: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    adicionar_pessoa_exemplo()
