import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from typing import Tuple, Optional

# Carregar variáveis do .env
load_dotenv()

# Configuração melhorada do banco de dados
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "fsid_user"),  # Recomendado usar usuário específico
    "password": os.getenv("DB_PASSWORD", ""),  # Nunca armazenar senha no código
    "database": os.getenv("DB_NAME", "FSID"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "auth_plugin": 'mysql_native_password',
    "raise_on_warnings": True,
    "autocommit": False  # Para controle explícito de transações
}

def conectar_banco() -> Optional[mysql.connector.connection.MySQLConnection]:
    """Estabelece conexão com o MySQL com tratamento aprimorado"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conexão estabelecida com sucesso")
        return conn
    except Error as e:
        print(f"❌ Erro ao conectar: {e}")
        # Mostra configuração sem expor a senha
        config_safe = {k: '*****' if k == 'password' else v for k, v in DB_CONFIG.items()}
        print(f"Configuração usada: {config_safe}")
        return None

def validar_dados_pessoa(dados: Tuple) -> bool:
    """Valida os dados antes da inserção"""
    if len(dados) != 14:
        print("❌ Número incorreto de campos para inserção")
        return False
    
    if not dados[0] or not dados[3]:  # Nome e CPF são obrigatórios
        print("❌ Nome completo e CPF são obrigatórios")
        return False
    
    return True

def adicionar_pessoa(dados: Tuple) -> Optional[int]:
    """
    Adiciona uma pessoa no banco de dados
    Retorna o ID gerado ou None em caso de falha
    """
    if not validar_dados_pessoa(dados):
        return None
    
    conn = conectar_banco()
    if not conn:
        return None
    
    cursor = None
    try:
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO pessoas (
                nome_completo, doc_identidade, titulo_eleitor, cpf,
                telefone, email, endereco, numero, complemento,
                bairro, cidade, estado, cep, pais
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, dados)
        conn.commit()
        
        person_id = cursor.lastrowid
        print(f"✅ Pessoa adicionada com ID: {person_id}")
        return person_id
        
    except Error as e:
        conn.rollback()
        print(f"❌ Erro ao inserir dados: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def adicionar_pessoa_exemplo() -> Optional[int]:
    """Adiciona dados de exemplo para teste"""
    dados_exemplo = (
        "Gustavo Koglin",          # nome_completo
        "RG445566",                # doc_identidade
        "TE223344",                # titulo_eleitor
        "789.12345.67-8",          # cpf
        "1195555-4444",            # telefone
        "gustavo.koglin@example.com",  # email
        "Rua das Palmeiras",       # endereco
        "250",                     # numero
        "Sala 101",                # complemento
        "Centro",                  # bairro
        "São Paulo",               # cidade
        "SP",                      # estado
        "01234-567",               # cep
        "Brasil"                   # pais
    )
    return adicionar_pessoa(dados_exemplo)

if __name__ == "__main__":
    resultado = adicionar_pessoa_exemplo()
    if resultado:
        print("Operação concluída com sucesso!")
    else:
        print("Falha ao adicionar pessoa")