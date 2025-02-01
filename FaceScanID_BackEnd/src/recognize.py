import cv2
import os
import tkinter as tk
from tkinter import Button, Label
from deepface import DeepFace
from config import IMAGE_DIR

# Variáveis globais
zoom_factor = 1.0
frame = None
cap = None
camera_on = False
root = None
btn_iniciar = None
panel_camera = None

def aplicar_zoom(frame, zoom_factor):
    """Aplica zoom na imagem."""
    height, width = frame.shape[:2]
    new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)
    resized_frame = cv2.resize(frame, (new_width, new_height))

    if zoom_factor > 1.0:
        x1 = (new_width - width) // 2
        y1 = (new_height - height) // 2
        resized_frame = resized_frame[y1:y1 + height, x1:x1 + width]

    return resized_frame

def reconhecer_faces_camera():
    """Inicia ou encerra a câmera e faz reconhecimento facial."""
    global cap, frame, camera_on, btn_iniciar

    if camera_on:
        encerrar_camera()
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Erro ao acessar a webcam.")
        return

    camera_on = True
    btn_iniciar.config(text="Encerrar Câmera")

    print("🎥 Iniciando reconhecimento facial. Pressione 'q' para encerrar.")

    exibir_camera_tkinter()

def exibir_camera_tkinter():
    """Exibe a câmera na própria interface Tkinter."""
    global frame, camera_on

    if not camera_on:
        return

    ret, frame = cap.read()
    if not ret:
        return

    frame = aplicar_zoom(frame, zoom_factor)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        temp_path = save_temp_frame(frame)

        resultado = DeepFace.find(
            img_path=temp_path,
            db_path=IMAGE_DIR,
            enforce_detection=False,
            model_name="ArcFace",
            detector_backend="mtcnn",
            distance_metric="euclidean_l2",
        )

        if resultado and not resultado[0].empty:
            nome_arquivo = os.path.basename(resultado[0]["identity"][0])
            nome = os.path.splitext(nome_arquivo)[0]
            cor = (0, 255, 0)
        else:
            nome = "Desconhecido"
            cor = (0, 0, 255)

        rostos = DeepFace.extract_faces(img_path=temp_path, detector_backend="mtcnn", enforce_detection=False)
        for rosto in rostos:
            facial_area = rosto["facial_area"]
            x, y, w, h = facial_area["x"], facial_area["y"], facial_area["w"], facial_area["h"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)
            cv2.putText(frame, nome, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cor, 2)

    except Exception as e:
        print(f"⚠️ Erro na detecção facial: {e}")

    cv2.imshow("Reconhecimento Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        encerrar_camera()

    root.after(10, exibir_camera_tkinter)

def encerrar_camera():
    """Fecha a câmera e encerra a exibição."""
    global cap, camera_on, btn_iniciar
    camera_on = False
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    btn_iniciar.config(text="Iniciar Câmera")

def fechar_aplicacao():
    """Fecha a interface gráfica e encerra a câmera se necessário."""
    encerrar_camera()
    root.quit()

def save_temp_frame(frame):
    """Salva o frame atual como imagem temporária e retorna o caminho."""
    temp_path = "temp_frame.jpg"
    cv2.imwrite(temp_path, frame)
    return temp_path

def salvar_foto():
    """Salva uma captura da câmera."""
    global frame
    if frame is not None:
        caminho = os.path.join(IMAGE_DIR, "captura.jpg")
        cv2.imwrite(caminho, frame)
        print(f"📸 Foto salva em: {caminho}")

def aumentar_zoom():
    """Aumenta o zoom na imagem."""
    global zoom_factor
    zoom_factor += 0.1
    print(f"🔍 Zoom aumentado para {zoom_factor:.1f}")

def diminuir_zoom():
    """Diminui o zoom na imagem."""
    global zoom_factor
    zoom_factor = max(1.0, zoom_factor - 0.1)
    print(f"🔎 Zoom reduzido para {zoom_factor:.1f}")

# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Reconhecimento Facial")
root.geometry("1000x600")

# Criando um frame para os botões na lateral esquerda
frame_botoes = tk.Frame(root)
frame_botoes.pack(side="left", padx=20, pady=20)

# Criando botões estilizados
def criar_botao(texto, comando):
    botao = Button(frame_botoes, text=texto, command=comando, font=("Arial", 12),
                   bg="#007BFF", fg="white", activebackground="#0056b3",
                   activeforeground="white", bd=2, relief="raised", width=20, height=2, cursor="hand2")
    botao.pack(pady=5)
    return botao

# Criando botões
btn_iniciar = criar_botao("Iniciar Câmera", reconhecer_faces_camera)
btn_capturar = criar_botao("📸 Capturar Foto", salvar_foto)
btn_zoom_in = criar_botao("🔍 Zoom In", aumentar_zoom)
btn_zoom_out = criar_botao("🔎 Zoom Out", diminuir_zoom)
btn_sair = criar_botao("❌ Fechar", fechar_aplicacao)

# Fecha o programa ao clicar no botão de fechar da janela
root.protocol("WM_DELETE_WINDOW", fechar_aplicacao)

# Executando a interface gráfica
root.mainloop()
