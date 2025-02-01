import os
import cv2
from config import IMAGE_DIR  # Importa caminho das imagens

def corrigir_imagens():
    """Redimensiona e converte imagens para RGB."""
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            caminho = os.path.join(IMAGE_DIR, filename)
            img = cv2.imread(caminho)
            if img is None:
                print(f"❌ Falha ao carregar {filename}")
                continue

            # Converte para RGB e salva novamente
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(caminho, img)

if __name__ == "__main__":
    corrigir_imagens()
