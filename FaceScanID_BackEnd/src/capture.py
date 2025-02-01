import cv2
import os
from config import IMAGE_DIR  # Importa caminho das imagens

def capturar_foto(nome_arquivo="captura.jpg", camera_index=0):
    """
    Captura uma imagem da webcam e salva no diretório de faces.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"❌ Não foi possível acessar a câmera {camera_index}.")
        return

    ret, frame = cap.read()
    if ret:
        os.makedirs(IMAGE_DIR, exist_ok=True)
        caminho_arquivo = os.path.join(IMAGE_DIR, nome_arquivo)
        cv2.imwrite(caminho_arquivo, frame)
        print(f"✅ Imagem salva em: {caminho_arquivo}")
    else:
        print("❌ Falha ao capturar imagem.")

    cap.release()

if __name__ == "__main__":
    capturar_foto()
