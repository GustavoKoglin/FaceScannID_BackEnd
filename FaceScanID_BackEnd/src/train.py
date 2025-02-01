import os
import pickle
from deepface import DeepFace
from config import IMAGE_DIR, REPRESENTATIONS_FILE  # Importa diretórios de imagem e embeddings

def gerar_representacoes():
    """Gera e salva embeddings faciais com DeepFace."""
    todas_reps = []

    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")) and (caminho := os.path.join(IMAGE_DIR, filename)):
            try:
                if reps := DeepFace.represent(img_path=caminho, enforce_detection=False):
                    todas_reps.append({
                        "arquivo": filename,
                        "representacao": reps[0]["embedding"]
                    })
                    print(f"✅ Processado: {filename}")
            except Exception as e:
                print(f"❌ Erro em {filename}: {e}")
    
    if todas_reps:
        os.makedirs(os.path.dirname(REPRESENTATIONS_FILE), exist_ok=True)
        with open(REPRESENTATIONS_FILE, "wb") as f:
            pickle.dump(todas_reps, f)
        print("✅ Representações salvas com sucesso!")

if __name__ == "__main__":
    gerar_representacoes()
