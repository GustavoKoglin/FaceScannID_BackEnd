# api/app.py
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Inicializa o aplicativo Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir acesso de diferentes origens

def conectar_banco():
    """
    Estabelece conexão com o banco de dados MySQL
    usando as variáveis de ambiente carregadas em config.py.
    """
    try:
        return mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            port=config.DB_PORT
        )
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

@app.route("/buscar/<nome_completo>", methods=["GET"])
def buscar_usuario(nome_completo):
    """
    Busca um usuário pelo nome completo.
    Se a URL enviar nome_completo com `_`, será convertido para espaços.
    """
    nome_completo = nome_completo.replace("_", " ")  # Converte underscores para espaços

    conn = conectar_banco()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pessoas WHERE nome_completo = %s", (nome_completo,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            return jsonify(usuario), 200  # Retorna os dados do usuário encontrado
        else:
            return jsonify({"error": "Usuário não encontrado"}), 404
    except Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route("/adicionar", methods=["POST"])
def adicionar_usuario():
    """
    Endpoint para adicionar um novo usuário ao banco de dados.
    Recebe JSON com todos os campos requisitados.
    """
    dados = request.json  # Obtém dados da requisição JSON

    # Extrai as colunas
    nome_completo = dados.get("nome_completo")
    doc_identidade = dados.get("doc_identidade")
    titulo_eleitor = dados.get("titulo_eleitor")
    certidao_militar = dados.get("certidao_militar")
    possui_registro_classe = dados.get("possui_registro_classe")
    numero_registro_classe = dados.get("numero_registro_classe")
    pis_pasep = dados.get("pis_pasep")
    tipo_sanguineo = dados.get("tipo_sanguineo")
    telefone = dados.get("telefone")
    endereco = dados.get("endereco")
    emails = dados.get("emails")
    possui_imoveis = dados.get("possui_imoveis")
    tipo_imovel = dados.get("tipo_imovel")
    registro_imovel = dados.get("registro_imovel")
    endereco_imovel = dados.get("endereco_imovel")
    possui_veiculos = dados.get("possui_veiculos")
    tipo_veiculo = dados.get("tipo_veiculo")
    marca_veiculo = dados.get("marca_veiculo")
    registro_veiculo = dados.get("registro_veiculo")
    possui_parente = dados.get("possui_parente")
    nome_parente = dados.get("nome_parente")
    doc_parente = dados.get("doc_parente")
    telefone_parente = dados.get("telefone_parente")
    endereco_parente = dados.get("endereco_parente")

    # Verifica se pelo menos nome_completo e doc_identidade foram fornecidos
    if not nome_completo or not doc_identidade:
        return jsonify({"error": "Campo 'nome_completo' e 'doc_identidade' são obrigatórios"}), 400
    
    conn = conectar_banco()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    try:
        cursor = conn.cursor()
        # Insere todos os campos na tabela
        cursor.execute("""
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
        """, (
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
        ))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Usuário adicionado com sucesso!"}), 201
    except Error as e:
        print(f"Erro ao adicionar usuário: {e}")
        return jsonify({"error": "Erro ao inserir no banco de dados"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
