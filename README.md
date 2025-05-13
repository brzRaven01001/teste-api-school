# 🎓 API de Gerenciamento Escolar

Uma API RESTful simples desenvolvida com **Flask** para gerenciamento de dados escolares como **alunos**, **professores** e **turmas**.

Organizada em camadas (Controller, Model, Repository), esta aplicação oferece endpoints para realizar as principais operações CRUD (Create, Read, Update, Delete), além de uma função de **reset** dos dados.

---

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Flask 3.1.0
- Flask-SQLAlchemy 3.1.1
- Flask-RESTx 1.3.0
- Flask-CORS 4.1.0
- Requests 2.32.3
- Docker (opcional)
- Swagger para documentação dos endpoints

---

## 🗂 Estrutura do Projeto

```
teste-api-school/
│
├── controller/       # Arquivos de controle para alunos, turmas e professores
├── models/           # Modelos das entidades
├── repository/       # Lógica de acesso a dados
├── Swagger/          # Documentação da API com Swagger
│
├── app.py            # Arquivo principal da aplicação
├── config.py         # Configurações globais
├── requirements.txt  # Lista de dependências
├── Dockerfile        # Dockerfile para a imagem do projeto
└── docker-compose.yml# Configuração Docker Compose
```

---

## 📦 Requisitos

- Python 3 instalado
- Git (opcional)
- Docker e Docker Compose (se quiser usar containers)

---

## 🧪 Como Rodar o Projeto Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/brzRaven01001/teste-api-school.git
cd teste-api-school
```

### 2. Criar e ativar um ambiente virtual

```bash
python -m venv venv
# Ativar:
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate        # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar o projeto

```bash
python app.py
```

A API estará disponível em `http://127.0.0.1:8000`.

---

## 🐳 Como Rodar com Docker

> Requer Docker e Docker Compose instalados.

### 1. Build da imagem

```bash
docker build -t school-api .
```

### 2. Executar com docker-compose

```bash
docker-compose up
```

---

## 📖 Documentação com Swagger

A documentação interativa estará disponível (após subir o servidor) em:

```
http://127.0.0.1:8000/docs
```

---

## 🧩 Funcionalidades da API

Para **alunos**, **professores** e **turmas**:

- `GET /entidade`: Listar todos
- `POST /entidade`: Criar novo
- `GET /entidade/<id>`: Buscar por ID
- `PUT /entidade/<id>`: Atualizar
- `DELETE /entidade/<id>`: Deletar
- `DELETE /entidade/reset`: Resetar a entidade

> Substitua `entidade` por `alunos`, `professor` ou `turmas`.

---

## 👥 Projeto Acadêmico

Este projeto foi desenvolvido em grupo como parte da disciplina de Desenvolvimento de APIs e Microsserviços na **Faculdade Impacta**, com fins didáticos e de aprendizado prático sobre APIs REST com Flask.


---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
