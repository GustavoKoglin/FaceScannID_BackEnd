"""
RECOGNIZE.PY - Versão Melhorada
- Reconhecimento facial em tempo real com OpenCV e DeepFace
- Interface aprimorada com Tkinter
- Controles de câmera e zoom
"""

import cv2
import os
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys
from deepface import DeepFace
import numpy as np

# Configuração de importação segura
try:
    from config import DIRECTORIES, FILES, DEEPFACE_CONFIG
except ImportError:
    PROJECT_ROOT = Path(__file__).parent.parent
    sys.path.append(str(PROJECT_ROOT))
    from config import DIRECTORIES, FILES, DEEPFACE_CONFIG

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.zoom_factor = 1.0
        self.frame = None
        self.cap = None
        self.camera_on = False
        self.recognized_faces = []
        
        # Configurações da câmera
        self.camera_index = 0  # Câmera padrão
        self.camera_width = 1280
        self.camera_height = 720
        self.camera_fps = 30
        
        self.setup_ui()
        self.bind_keys()
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        self.root.title("Reconhecimento Facial")
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame de controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Botões
        self.btn_start = ttk.Button(
            control_frame, 
            text="Iniciar Câmera", 
            command=self.toggle_camera,
            style="Accent.TButton"
        )
        self.btn_start.pack(pady=10, fill=tk.X)
        
        ttk.Button(
            control_frame, 
            text="Capturar Foto", 
            command=self.save_photo
        ).pack(pady=5, fill=tk.X)
        
        ttk.Button(
            control_frame, 
            text="Zoom +", 
            command=lambda: self.adjust_zoom(0.1)
        ).pack(pady=5, fill=tk.X)
        
        ttk.Button(
            control_frame, 
            text="Zoom -", 
            command=lambda: self.adjust_zoom(-0.1)
        ).pack(pady=5, fill=tk.X)
        
        ttk.Button(
            control_frame, 
            text="Sair", 
            command=self.close_app,
            style="Cancel.TButton"
        ).pack(pady=20, fill=tk.X)
        
        # Status
        self.status_var = tk.StringVar(value="Câmera: DESLIGADA")
        ttk.Label(
            control_frame, 
            textvariable=self.status_var,
            foreground="red"
        ).pack(pady=10)
        
        # Estilo
        self.setup_styles()
    
    def setup_styles(self):
        """Configura estilos visuais"""
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="black", background="#0078D7")
        style.configure("Cancel.TButton", foreground="black", background="#D73A3A")
        style.map("Accent.TButton",
                 background=[("active", "#106EBE"), ("pressed", "#005A9E")])
        style.map("Cancel.TButton",
                 background=[("active", "#BE1010"), ("pressed", "#9E0000")])
    
    def bind_keys(self):
        """Configura atalhos de teclado"""
        self.root.bind('<q>', lambda e: self.toggle_camera())
        self.root.bind('<Escape>', lambda e: self.close_app())
        self.root.bind('<plus>', lambda e: self.adjust_zoom(0.1))
        self.root.bind('<minus>', lambda e: self.adjust_zoom(-0.1))
    
    def toggle_camera(self):
        """Inicia/para a câmera padrão"""
        if self.camera_on:
            self.stop_camera()
        else:
            self.start_camera()
    
    def start_camera(self):
        """Inicia a câmera com configurações otimizadas"""
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        
        # Configurações da câmera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
        self.cap.set(cv2.CAP_PROP_FPS, self.camera_fps)
        
        if not self.cap.isOpened():
            messagebox.showerror(
                "Erro de Câmera",
                "Não foi possível acessar a câmera.\nVerifique se está disponível."
            )
            return
        
        self.camera_on = True
        self.btn_start.config(text="Parar Câmera")
        self.status_var.set("Câmera: LIGADA")
        self.update_camera()
    
    def stop_camera(self):
        """Para a câmera e libera recursos"""
        self.camera_on = False
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        self.btn_start.config(text="Iniciar Câmera")
        self.status_var.set("Câmera: DESLIGADA")
    
    def update_camera(self):
        """Atualiza o feed da câmera com reconhecimento facial"""
        if not self.camera_on:
            return
        
        ret, self.frame = self.cap.read()
        if not ret:
            print("Erro ao capturar frame")
            self.stop_camera()
            return
        
        # Aplica zoom
        frame = self.apply_zoom(self.frame, self.zoom_factor)
        
        try:
            # Converte para RGB (DeepFace trabalha com RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detecta rostos
            self.recognized_faces = DeepFace.extract_faces(
                img_path=rgb_frame,
                detector_backend="mtcnn",
                enforce_detection=False,
                align=True
            )
            
            # Processa cada rosto detectado
            for face in self.recognized_faces:
                if 'facial_area' in face and face['confidence'] > 0.85:
                    self.process_face(frame, face)
            
        except Exception as e:
            print(f"Erro durante reconhecimento: {str(e)}")
        
        # Exibe o frame
        cv2.imshow("Reconhecimento Facial", frame)
        
        # Agenda próxima atualização
        self.root.after(10, self.update_camera)
    
    def process_face(self, frame, face):
        """Processa e desenha informações para cada rosto detectado"""
        facial_area = face['facial_area']
        x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
        
        # Desenha retângulo ao redor do rosto
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Tenta reconhecer a pessoa
        try:
            # Extrai a região do rosto
            face_region = frame[y:y+h, x:x+w]
            
            # Faz o reconhecimento
            results = DeepFace.find(
                img_path=face_region,
                db_path=str(DIRECTORIES['faces']),
                enforce_detection=False,
                silent=True
            )
            
            # Mostra resultado
            if results and not results[0].empty:
                identity = os.path.splitext(os.path.basename(results[0]['identity'][0]))[0]
                cv2.putText(
                    frame, identity, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
                )
            else:
                cv2.putText(
                    frame, "Desconhecido", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
                )
                
        except Exception as e:
            print(f"Erro no reconhecimento: {str(e)}")
            cv2.putText(
                frame, "Erro", (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2
            )
    
    def apply_zoom(self, frame, zoom_factor):
        """Aplica zoom mantendo proporções"""
        if zoom_factor == 1.0:
            return frame
            
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        new_width = int(width / zoom_factor)
        new_height = int(height / zoom_factor)
        
        x1 = max(0, center_x - new_width // 2)
        y1 = max(0, center_y - new_height // 2)
        x2 = min(width, center_x + new_width // 2)
        y2 = min(height, center_y + new_height // 2)
        
        cropped = frame[y1:y2, x1:x2]
        return cv2.resize(cropped, (width, height))
    
    def adjust_zoom(self, increment):
        """Ajusta o zoom"""
        self.zoom_factor = max(1.0, min(3.0, self.zoom_factor + increment))
        print(f"Zoom ajustado: {self.zoom_factor:.1f}x")
    
    def save_photo(self):
        """Salva o frame atual"""
        if self.frame is not None:
            photo_path = str(DIRECTORIES['faces'] / 'captura.jpg')
            cv2.imwrite(photo_path, self.frame)
            messagebox.showinfo(
                "Foto Salva",
                f"Foto capturada salva em:\n{photo_path}"
            )
    
    def close_app(self):
        """Fecha o aplicativo corretamente"""
        self.stop_camera()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()

if __name__ == "__main__":
    main()