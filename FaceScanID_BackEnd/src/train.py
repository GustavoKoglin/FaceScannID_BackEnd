"""
TRAIN.PY - Versão Final Corrigida
- Corrige problemas com arquivos cascade do OpenCV
- Configuração otimizada para detecção de faces
- Tratamento robusto de erros
"""

import os
import pickle
import shutil
from deepface import DeepFace
from pathlib import Path
import sys
import numpy as np
from tqdm import tqdm
import tempfile
import cv2

# Configuração de caminhos
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from config import DIRECTORIES, FILES, DEEPFACE_CONFIG

def verificar_arquivos_cascade():
    """Verifica e corrige os caminhos dos arquivos cascade do OpenCV."""
    try:
        # Verifica se os arquivos cascade existem no local padrão
        cascade_path = Path(cv2.__file__).parent / 'data'
        frontalface_path = cascade_path / 'haarcascade_frontalface_default.xml'
        eye_path = cascade_path / 'haarcascade_eye.xml'
        
        if not frontalface_path.exists():
            print(f"⚠️ Arquivo cascade não encontrado: {frontalface_path}")
            # Tenta encontrar em outro local comum
            alt_path = Path(sys.prefix) / 'Lib' / 'site-packages' / 'cv2' / 'data'
            if (alt_path / 'haarcascade_frontalface_default.xml').exists():
                cascade_path = alt_path
                print(f"✅ Arquivos cascade encontrados em: {cascade_path}")
        
        return str(cascade_path / 'haarcascade_frontalface_default.xml')
    except Exception as e:
        print(f"❌ Erro ao verificar arquivos cascade: {e}")
        return None

def gerar_representacoes():
    """Gera e salva embeddings faciais com DeepFace."""
    # Verifica arquivos cascade
    cascade_file = verificar_arquivos_cascade()
    if not cascade_file:
        print("❌ Não foi possível encontrar os arquivos necessários para detecção facial")
        return False

    # Verifica se o diretório de imagens existe
    if not DIRECTORIES['faces'].exists():
        print(f"❌ Diretório de imagens não encontrado: {DIRECTORIES['faces']}")
        return False

    # Cria um diretório temporário para cópias seguras das imagens
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        # Lista arquivos de imagem válidos e cria cópias com nomes seguros
        arquivos_seguros = []
        for arquivo in DIRECTORIES['faces'].iterdir():
            if arquivo.suffix.lower() in ('.jpg', '.jpeg', '.png'):
                # Cria um nome de arquivo seguro (sem caracteres especiais)
                nome_seguro = f"temp_{len(arquivos_seguros)}{arquivo.suffix}"
                caminho_seguro = temp_dir_path / nome_seguro
                
                # Copia o arquivo para o diretório temporário
                shutil.copy2(arquivo, caminho_seguro)
                arquivos_seguros.append({
                    'original': arquivo.name,
                    'temp_path': caminho_seguro
                })

        if not arquivos_seguros:
            print("❌ Nenhuma imagem válida encontrada no diretório de faces")
            return False

        print(f"🔍 Encontradas {len(arquivos_seguros)} imagens para processamento")

        todas_reps = []
        processados = 0
        erros = 0

        # Configurações do DeepFace otimizadas
        model_name = DEEPFACE_CONFIG.get('model_name', 'VGG-Face')
        detector_backend = 'mtcnn'  # Mais robusto que opencv
        enforce_detection = False  # Permite processar mesmo sem detecção
        align = True

        # Processa imagens com barra de progresso
        for arquivo in tqdm(arquivos_seguros, desc="Processando imagens"):
            try:
                # Verifica se a imagem é válida antes de processar
                img = cv2.imread(str(arquivo['temp_path']))
                if img is None:
                    print(f"⚠️ Imagem inválida: {arquivo['original']}")
                    erros += 1
                    continue

                # Gera representação facial usando o caminho temporário seguro
                reps = DeepFace.represent(
                    img_path=str(arquivo['temp_path']),
                    model_name=model_name,
                    detector_backend=detector_backend,
                    enforce_detection=enforce_detection,
                    align=align
                )

                if reps:
                    todas_reps.append({
                        "arquivo": arquivo['original'],  # Usa o nome original
                        "representacao": np.array(reps[0]["embedding"])
                    })
                    processados += 1
                else:
                    print(f"⚠️ Nenhuma face detectada em: {arquivo['original']}")
                    erros += 1

            except Exception as e:
                print(f"❌ Erro ao processar {arquivo['original']}: {str(e)}")
                erros += 1

        # Salva representações se houve sucesso
        if todas_reps:
            # Garante que o diretório existe
            FILES['representations'].parent.mkdir(parents=True, exist_ok=True)
            
            # Salva em formato pickle
            with open(FILES['representations'], 'wb') as f:
                pickle.dump(todas_reps, f, protocol=pickle.HIGHEST_PROTOCOL)

            print(f"\n✅ Processamento concluído com sucesso!")
            print(f"   - Imagens processadas: {processados}")
            print(f"   - Erros encontrados: {erros}")
            print(f"   - Arquivo salvo em: {FILES['representations']}")
            return True
        else:
            print("\n❌ Nenhuma representação foi gerada")
            return False

if __name__ == "__main__":
    gerar_representacoes()