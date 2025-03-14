# FaceScanID - Reconhecimento Facial

Este projeto implementa um sistema de **reconhecimento facial** utilizando **DeepFace, OpenCV e Flask**. Ele permite capturar imagens, armazenar registros faciais e realizar comparações em tempo real.

---

## 📁 Estrutura do Projeto

```
FaceScanID/
│── env/                  # Ambiente virtual (NÃO alterar arquivos aqui)
│── data/                 # Armazena imagens e informações de pessoas
│   ├── faces/            # Fotos de pessoas conhecidas
│   ├── embeddings/       # Arquivos com dados de reconhecimento
│── models/               # Modelos treinados para reconhecimento facial
│── database/             # Banco de dados para armazenar informações
│── src/                  # Código-fonte principal do projeto
│   ├── capture.py        # Captura de imagem e reconhecimento facial
│   ├── config.py         # Configurações gerais do projeto
│   ├── train.py          # Treina o modelo de reconhecimento facial
│   ├── recognize.py      # Executa o reconhecimento facial em tempo real
│   ├── database.py       # Gerencia o banco de dados de usuários
│── api/                  # API para fornecer dados via requisições HTTP
│   ├── app.py            # Backend Flask para buscar informações
│── requirements.txt      # Dependências do projeto
│── README.md             # Documentação do projeto
│── .env                  # Variáveis do Projeto
```

---

## 🛠️ Configuração do Ambiente

### 📌 **1. Clonar o Repositório**
```sh
# Clonar o repositório
git clone https://github.com/seu-usuario/FaceScanID.git
cd FaceScanID
```

### 📌 **2. Criar e Ativar Ambiente Virtual**
```sh
# Criar ambiente virtual
python -m venv env
```

**No Windows (PowerShell):**
```sh
.\env\Scripts\Activate
```

**No Linux/macOS:**
```sh
source env/bin/activate
```

---

## 📦 Instalação de Dependências

### 📌 **1. Instalar todas as dependências do projeto**
```sh
pip install -r requirements.txt
```

### 📌 **2. Caso tenha problemas com dependências específicas:**
```sh
pip install python-dotenv mysql-connector-python deepface flask-cors opencv-python
```

**Se houver erro com OpenCV ou TensorFlow:**
```sh
pip install --upgrade --force-reinstall opencv-python-headless
pip install numpy==1.21.2
```

---

## 📊 **Banco de Dados**

Certifique-se de configurar o **MySQL** e criar o banco antes de iniciar.

### 📌 **1. Criar banco de dados**
```sql
CREATE DATABASE FSID;
```

### 📌 **2. Criar a tabela 'pessoas'**
```sql
CREATE TABLE pessoas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_completo VARCHAR(255),
    doc_identidade VARCHAR(50),
    titulo_eleitor VARCHAR(50),
    certidao_militar VARCHAR(50),
    telefone VARCHAR(20),
    endereco TEXT
);

-- Outros dados serão inseridos no decorrer do projeto.
```

---

## 🚀 **Executando o Projeto**

### 📌 **1. Treinar a IA com novas imagens**
Após adicionar imagens na pasta `data/faces/`, execute:
```sh
python src/train.py
```

### 📌 **2. Iniciar o servidor Flask**
```sh
python api/app.py
```
Agora, o backend estará rodando em:
```
http://127.0.0.1:5000/
```
Para buscar um usuário específico:
```
http://127.0.0.1:5000/buscar/nome_completo
```

### 📌 **3. Iniciar o reconhecimento facial em tempo real**
```sh
python src/recognize.py
```
Após abrir a interface, clique em **"Iniciar Câmera"**.
Para encerrar, pressione **'q'** no teclado e clique em "Fechar".

---

## 📝 **Dicas para Resolução de Erros**

### ✅ **1. Verifique se o VS Code está usando o Python correto**
```sh
python -c "import sys; print(sys.executable)"
```
Se não for o do ambiente virtual, selecione manualmente no VS Code:
- Pressione **Ctrl + Shift + P** e digite: **Python: Select Interpreter**
- Escolha o interpretador dentro da pasta **env**.

### ✅ **2. Erro 'ModuleNotFoundError' para mysql.connector**
```sh
pip install --upgrade --force-reinstall mysql-connector-python Flask-Cors
```

### ✅ **3. Erro de TensorFlow no Windows**
```sh
pip install --upgrade --force-reinstall tensorflow
```

---

## 🤝 **Contribuições**

Sinta-se à vontade para contribuir com melhorias neste projeto! Para isso:
1. **Fork** este repositório
2. Crie uma **branch**: `git checkout -b minha-nova-feature`
3. Faça um **commit**: `git commit -m 'Adicionando nova funcionalidade'`
4. Envie para o repositório: `git push origin minha-nova-feature`
5. Crie um **Pull Request** 🚀

---

## 🏆 **Autor**
👤 **Gustavo Koglin**  
📧 [engcomputacao.gustavokoglin@gmail.com](mailto:engcomputacao.gustavokoglin@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/gustavokoglin/)

