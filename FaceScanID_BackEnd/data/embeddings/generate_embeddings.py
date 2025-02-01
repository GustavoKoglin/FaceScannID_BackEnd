# embeddings/generate_embeddings.py
import os
import pickle
from deepface import DeepFace

# Diretórios
IMAGE_DIR = "data/faces/"       # Onde estão as fotos de rostos
EMBEDDINGS_DIR = "data/embeddings/"  # Onde salvaremos as representações/embeddings
ENCODINGS_FILE = os.path.join(EMBEDDINGS_DIR, "deepface_encodings.pkl")

def gerar_embeddings():
    """
    Gera e salva as representações (embeddings) faciais das imagens de treinamento
    usando a biblioteca DeepFace. Armazena cada embedding individual em um .pkl
    e também todas juntas em 'deepface_encodings.pkl'.

    Observação:
        O DeepFace não usa a mesma lógica de 'face_recognition'. Em 'DeepFace.represent',
        podemos escolher o modelo (ArcFace, Facenet, VGG-Face etc.). Aqui, usamos o default.
    """
    
    # Lista para armazenar todas as embeddings e o nome do arquivo
    todas_embeddings = []

    # Garante que o diretório de embeddings existe
    if not os.path.exists(EMBEDDINGS_DIR):
        os.makedirs(EMBEDDINGS_DIR)

    # Percorre o diretório data/faces e processa cada imagem
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            caminho_imagem = os.path.join(IMAGE_DIR, filename)
            print(f"📷 Processando: {filename}")

            try:
                # Usamos DeepFace.represent para obter a representação facial
                # enforce_detection=False para evitar erro se não encontrar rosto
                representacao = DeepFace.represent(
                    img_path=caminho_imagem,
                    enforce_detection=False
                )

                if representacao and len(representacao) > 0:
                    # representacao é uma lista de dicionários. Exemplo:
                    # [{"embedding": [...], "facial_area": {...}, ...}]
                    emb = representacao[0].get("embedding", None)
                    if emb is None:
                        print(f"⚠️ Não foi possível obter embedding de {filename}.")
                        continue

                    # Nome base do arquivo sem extensão
                    nome_pessoa = os.path.splitext(filename)[0]

                    # Adiciona à lista geral
                    todas_embeddings.append((nome_pessoa, emb))

                    # Salva individualmente cada embedding
                    emb_path = os.path.join(EMBEDDINGS_DIR, f"{nome_pessoa}.pkl")
                    with open(emb_path, "wb") as f:
                        pickle.dump(emb, f)
                        print(f"✅ Embedding individual salvo em: {emb_path}")
                else:
                    print(f"⚠️ Nenhuma representação encontrada em {filename}. Pulando...")

            except Exception as e:
                print(f"❌ Erro ao processar {filename}: {e}")
                continue

    # Se obtivemos ao menos uma embedding, salvamos tudo em um único arquivo .pkl
    if todas_embeddings:
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump(todas_embeddings, f)
        print(f"✅ {len(todas_embeddings)} embeddings geradas e salvas em {ENCODINGS_FILE}!")
    else:
        print("❌ Nenhuma face foi detectada ou nenhuma embedding foi gerada. Verifique suas imagens!")

if __name__ == "__main__":
    gerar_embeddings()
