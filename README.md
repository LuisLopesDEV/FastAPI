# 🛒 API de Pedidos com Autenticação JWT (FastAPI + MySQL)

API REST desenvolvida com FastAPI para gerenciamento de usuários e pedidos, com autenticação segura via JWT, controle de permissões (admin/usuário) e integração com banco de dados MySQL utilizando SQLAlchemy.

---

## 🛠️ Tecnologias utilizadas

- **Python**
- **FastAPI**
- **MySQL**
- **SQLAlchemy**
- **Alembic** (migrations)
- **JWT (JSON Web Token)**
- **bcrypt** (hash de senha)
- **Pydantic**
- **OAuth2**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

---

## ⚙️ Funcionalidades

### 🔐 Autenticação
- Cadastro de usuários
- Login com geração de **access token** e **refresh token**
- Autenticação via JWT
- Proteção de rotas com OAuth2
- Renovação de token com refresh token

### 👤 Usuários
- Controle de permissões (usuário comum e administrador)
- Restrições de acesso baseadas em perfil

### 🛒 Pedidos
- Criação de pedidos
- Cancelamento e finalização de pedidos
- Listagem de pedidos (admin)
- Listagem de pedidos por usuário
- Adição e remoção de itens em pedidos
- Cálculo automático do valor total do pedido

---

## 🧠 Conceitos aplicados

- Autenticação e autorização com JWT
- Hash seguro de senhas com bcrypt
- Arquitetura REST
- Injeção de dependências (FastAPI)
- Relacionamentos ORM (SQLAlchemy)
- Controle de acesso por nível de usuário
- Versionamento de banco de dados com Alembic
- Boas práticas de segurança em APIs
---

## 🗂 Estrutura do Projeto

```bash
.
├── DataBase
│   └── models.py
├── Routes
│   ├── order_routes.py
│   ├── auth_routes.py
│   └── dependencies.py
├── schemas.py
├── main.py
└── README.md
```

---

## 🔐 Autenticação e Autorização

A API utiliza **JWT** para autenticação:

* Todas as rotas de pedidos exigem token
* Usuários comuns só podem acessar seus próprios pedidos
* Usuários **admin** podem acessar todos os pedidos

O token deve ser enviado no header:

```http
Authorization: Bearer <seu_token_aqui>
```

---

## 👤 Usuários

### Modelo de Usuário

* `id`
* `name`
* `email`
* `senha` (hash)
* `ativo`
* `admin`

---

## 📦 Pedidos

### Status possíveis

* `PENDENTE`
* `CANCELADO`
* `FINALIZADO`

### Um pedido possui:

* Usuário dono
* Lista de itens
* Preço total calculado automaticamente

---

## 📌 Principais Endpoints

### 🔹 Criar Pedido

`POST /order/pedidos`

Cria um novo pedido para um usuário.

---

### 🔹 Cancelar Pedido

`POST /order/pedidos/cancelar/{id_pedido}`

Cancela um pedido existente (admin ou dono).

---

### 🔹 Finalizar Pedido

`POST /order/pedidos/finalizar/{id_pedido}`

Finaliza um pedido existente.

---

### 🔹 Adicionar Item ao Pedido

`POST /order/pedido/adcionar/{id_pedido}`

Adiciona um item a um pedido e recalcula o preço.

---

### 🔹 Remover Item do Pedido

`POST /order/pedido/remover/{id_item_pedido}`

Remove um item do pedido e recalcula o preço.

---

### 🔹 Ver Pedido

`GET /order/pedido/{id_pedido}`

Retorna os detalhes de um pedido específico.

---

### 🔹 Listar Pedidos (Admin)

`GET /order/listar`

Lista todos os pedidos do sistema (apenas admin).

---

### 🔹 Listar Pedidos do Usuário

`GET /order/listar/pedidos-usuario`

Lista apenas os pedidos do usuário autenticado.

---

## 🧪 Documentação Automática

Após rodar o projeto, acesse:

* Swagger UI: `http://localhost:8000/docs`
* Redoc: `http://localhost:8000/redoc`

---

## ▶️ Como Executar o Projeto

### 1️⃣ Clonar o repositório

```bash
git clone <url-do-repositorio>
cd projeto
```

### 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar o banco de dados

Atualize a string de conexão em `models.py`:

```python
create_engine("mysql+pymysql://usuario:senha@localhost:3306/meubanco")
```

---

### 5️⃣ Rodar a aplicação

```bash
uvicorn main:app --reload
```

---

## 📌 Observações

* O preço do pedido é recalculado automaticamente ao adicionar/remover itens
* O controle de permissões é feito via dependências do FastAPI
* O projeto segue boas práticas de organização e tipagem

---

## ✨ Possíveis Melhorias Futuras

* Paginação de pedidos
* Histórico de status
* Testes automatizados
* Dockerização
* Cache com Redis

---

## 👨‍💻 Autor

Projeto desenvolvido para fins de estudo e prática com **FastAPI + SQLAlchemy**.
