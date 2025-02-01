Estrutura do Projeto:

FaceScanID/
│── env/                  # Ambiente virtual (NÃO alterar arquivos aqui)
│── data/                 # Armazena imagens e informações de pessoas
│   ├── faces/            # Fotos de pessoas conhecidas
│   ├── embeddings/       # Arquivos com dados de reconhecimento
│── models/               # Modelos treinados para reconhecimento facial
│── database/             # Banco de dados para armazenar informações
│── src/                  # Código-fonte principal do projeto
│   ├── capture.py        # Captura de imagem e reconhecimento facial
|   │── config.py         # Configurações gerais do projeto
│   ├── train.py          # Treina o modelo de reconhecimento facial
│   ├── recognize.py      # Executa o reconhecimento facial em tempo real
│   ├── database.py       # Gerencia o banco de dados de usuários
│── api/                  # API para fornecer dados via requisições HTTP
│   ├── app.py            # Backend Flask para buscar informações
│── requirements.txt      # Dependências do projeto
│── README.md             # Documentação do projetos
|── .env                  # Variáveis do Projeto.

__________________________________________________________________________________________

INSTALANDO AS DEPENDÊNCIAS:
__________________________________________________________________________________________

📌 Acesse a pasta do projeto (onde o repositório foi clonado):
Ex: cd caminho/para/o/repo
   

___________________________________________________________________________________________

📌 Ative o ambiente virtual (se estiver usando um):
Windows (PowerShell):
.\env\Scripts\Activate

___________________________________________________________________________________________
📌Instalação de Bibliotecas:

pip install python-dotenv

pip install mysql-connector-python

pip install deepface

pip install flask-cors

pip install opencv-python


EM CASO DE ERROS COM AS BIBLIOTECAS:

✅ Passo 1: Verificar qual Python o VS Code está usando
Abra o terminal no VS Code e execute:

powershell
python -c "import sys; print(sys.executable)"

Isso mostrará o caminho do interpretador Python que o VS Code está usando. Se não for o Python do ambiente virtual (env), precisamos corrigir isso.

✅ Passo 2: Ativar o ambiente virtual corretamente
Ative o ambiente virtual manualmente:

No PowerShell:

powershell
env\Scripts\Activate


No CMD:
cmd
env\Scripts\activate.bat

Agora, execute o Python novamente para ver se ele reconhece os pacotes:

powershell
python -c "import mysql.connector"

Se não der erro, o ambiente virtual está ativado corretamente.

✅ Passo 3: Configurar o Python correto no VS Code

Pressione Ctrl + Shift + P (ou F1) para abrir a Command Palette

Digite: Python: Select Interpreter

Escolha o Python dentro do seu ambiente virtual, que será algo como:

local:\ ... \FaceScanID_BackEnd\env\Scripts\python.exe
Reinicie o VS Code (Ctrl + Shift + P → Reload Window)

✅ Passo 4: Testar se o problema foi resolvido
Agora, abra o terminal dentro do VS Code e execute:

powershell
python -c "import mysql.connector"
Se não houver erro, agora o VS Code está usando o ambiente correto! 🚀

Se ainda houver erro, tente forçar a reinstalação do pacote dentro do ambiente virtual:

powershell
pip install --upgrade --force-reinstall mysql-connector-python Flask-Cors
___________________________________________________________________________________________
📌 Instale todas as dependências com pip:
pip install -r requirements.txt

e

pip freeze > requirements.txt 
(Para adicionar os pacotes automaticamente no requiremens.txt ao instalar outras bibliotecas.)

____________________________________________________________________________________________
📌 Caso tenha problemas com o OpenCV e TensorFlow (erro de permissão ou incompatibilidade):
Se necessário, reinstale manualmente:

pip install --upgrade --force-reinstall opencv-python-headless

pip install numpy==1.21.2

_____________________________________________________________________________________________
📌Pasta "data/faces/" - Contem todas as fotos para reconhecimento facial.

Ao adicionar as fotos, dgite o comando abaixo para treinar a IA:

python src/train.py

______________________________________________________________________________________________
📌 O comando abaixo irá iniciar o servidor:

python api/app.py

Para buscar diretamente um nome, digite na URL do navegador:

http://127.0.0.1:5000/buscar/nome_completo


______________________________________________________________________________________________
📌Para Iniciar a Câmera e o Reconhecimento Facial, digite o comando abaixo:

python src/recognize.py

Ao iniciar, clique em "Inicar Câmera".
Para fechar/encerrar a câmera, tecle a leta "q" em seu teclado, e clique em fechar no menu aberto.