"""
CAPTURE.PY - Captura de Imagens da Câmera Padrão
- Foca exclusivamente na câmera padrão do Windows
- Melhor tratamento de erros e feedback ao usuário
- Configurações otimizadas para Windows
"""

import cv2
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

# Configuração de importação segura
try:
    from config import DIRECTORIES
except ImportError:
    # Fallback para caso o config.py não seja encontrado
    PROJECT_ROOT = Path(__file__).parent.parent
    sys.path.append(str(PROJECT_ROOT))
    from config import DIRECTORIES

class CaptureApp:
    def __init__(self, root):
        self.root = root
        self.camera_index = 0  # Índice zero para câmera padrão
        self.frame = None
        self.cap = None
        
        # Configurações específicas para Windows
        self.camera_width = 1280
        self.camera_height = 720
        self.camera_fps = 30
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        self.root.title("Captura de Foto - Câmera Padrão")
        self.root.geometry("600x400")
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame de visualização (placeholder)
        self.view_frame = ttk.LabelFrame(main_frame, text="Pré-visualização")
        self.view_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame de controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Botões
        ttk.Button(
            control_frame,
            text="Iniciar Câmera",
            command=self.start_camera,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        self.capture_btn = ttk.Button(
            control_frame,
            text="Capturar Foto",
            command=self.capture_photo,
            state=tk.DISABLED
        )
        self.capture_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="Sair",
            command=self.close_app,
            style="Cancel.TButton"
        ).pack(side=tk.RIGHT, padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Câmera não iniciada")
        ttk.Label(
            main_frame,
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
    
    def start_camera(self):
        """Inicia a câmera padrão com configurações para Windows"""
        try:
            # Força o uso do backend DirectShow no Windows
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            
            if not self.cap.isOpened():
                messagebox.showerror(
                    "Erro de Câmera",
                    "Não foi possível acessar a câmera padrão.\n"
                    "Verifique se a câmera está disponível e não está sendo "
                    "usada por outro aplicativo."
                )
                return
            
            # Configurações otimizadas para Windows
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
            self.cap.set(cv2.CAP_PROP_FPS, self.camera_fps)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            
            self.status_var.set("Câmera iniciada - Pronto para capturar")
            self.capture_btn.config(state=tk.NORMAL)
            
            # Mostra pré-visualização
            self.show_preview()
            
        except Exception as e:
            messagebox.showerror(
                "Erro Inesperado",
                f"Ocorreu um erro ao iniciar a câmera:\n{str(e)}"
            )
    
    def show_preview(self):
        """Mostra a pré-visualização da câmera"""
        ret, self.frame = self.cap.read()
        if ret:
            # Redimensiona para caber no frame
            preview = cv2.resize(self.frame, (640, 480))
            cv2.imshow("Pré-visualização - Câmera Padrão", preview)
        
        # Continua atualizando se a câmera estiver aberta
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.root.after(10, self.show_preview)
    
    def capture_photo(self):
        """Captura e salva uma foto"""
        try:
            if self.frame is None:
                messagebox.showwarning(
                    "Aviso",
                    "Nenhum frame disponível para captura"
                )
                return
            
            os.makedirs(DIRECTORIES['faces'], exist_ok=True)
            photo_path = str(DIRECTORIES['faces'] / 'captura.jpg')
            
            cv2.imwrite(photo_path, self.frame)
            messagebox.showinfo(
                "Sucesso",
                f"Foto capturada com sucesso:\n{photo_path}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Erro ao Salvar",
                f"Não foi possível salvar a foto:\n{str(e)}"
            )
    
    def close_app(self):
        """Libera recursos e fecha o aplicativo"""
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = CaptureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()

if __name__ == "__main__":
    main()