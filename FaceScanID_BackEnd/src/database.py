import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from config import db_config, host, user, password, name, port

class DatabaseManager:
    def __init__(self):
        load_dotenv()  # Carrega variáveis do .env
        DB_CONFIG = {
            "host": host,
            "user": user,
            "password": password,
            "database": name,
            "port": port,
            **db_config  # Desempacota os outros parâmetros de configuração
        }
        self.test_connection()  # Testa a conexão ao inicializar

    def test_connection(self):
        """Testa a conexão com o banco de dados"""
        try:
            conn = mysql.connector.connect(**self.config)
            print("✅ Conexão estabelecida com sucesso")
            conn.close()
            return True
        except Error as e:
            print(f"❌ Falha na conexão: {e}")
            print(f"Configuração usada: { {k: '*****' if k == 'password' else v for k,v in self.config.items()} }")
            return False
    
    def get_connection(self):
        """Estabelece conexão com o MySQL e retorna o objeto de conexão"""
        try:
            conn = mysql.connector.connect(**self.config)
            return conn
        except Error as e:
            print(f"❌ Erro ao conectar: {e}")
            return None
    
    def create_pessoas_table(self):
        """Cria a tabela pessoas com todas as colunas necessárias"""
        columns = [
            "id INT AUTO_INCREMENT PRIMARY KEY",
            "nome_completo VARCHAR(200) NOT NULL",
            "doc_identidade VARCHAR(50)",
            "titulo_eleitor VARCHAR(50)",
            "cpf VARCHAR(20) UNIQUE",  # Adicionado UNIQUE para evitar duplicatas
            "telefone VARCHAR(30)",
            "email VARCHAR(100)",
            "endereco TEXT",
            "numero VARCHAR(10)",
            "complemento VARCHAR(50)",
            "bairro VARCHAR(50)",
            "cidade VARCHAR(50)",
            "estado VARCHAR(2)",
            "cep VARCHAR(10)",
            "pais VARCHAR(50)",
            "data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP"  # Adicionado campo de data
        ]
        
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            create_query = f"""
                CREATE TABLE IF NOT EXISTS pessoas (
                    {', '.join(columns)}
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            cursor.execute(create_query)
            conn.commit()
            print("✅ Tabela 'pessoas' criada/verificada com sucesso")
            return True
        except Error as e:
            conn.rollback()
            print(f"❌ Erro ao criar tabela: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def execute_query(self, query, params=None):
        """Executa uma query genérica com tratamento de erros"""
        conn = self.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
                
        except Error as e:
            conn.rollback()
            print(f"❌ Erro na query: {e}\nQuery: {query}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == "__main__":
    db = DatabaseManager()
    if db.test_connection():
        db.create_pessoas_table()