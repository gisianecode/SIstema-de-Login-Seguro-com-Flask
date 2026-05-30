🔐 Sistema de Login Seguro com Flask

Sistema de autenticação simples, seguro e funcional desenvolvido com Python + Flask, com foco em boas práticas de segurança como hash de senha, controle de tentativas de login e proteção básica contra falhas comuns.

⸻

🚀 Funcionalidades

* 👤 Cadastro de usuários
* 🔑 Login com autenticação segura
* 🔒 Senhas criptografadas (bcrypt)
* 🧾 Sessão de usuário (login persistente)
* 🚪 Logout seguro
* 🛡️ Bloqueio após 5 tentativas de login incorretas
* ⚠️ Mensagens genéricas de erro (sem vazamento de informações)
* ✅ Validação de senha e dados de entrada

⸻

🧱 Tecnologias utilizadas

* Python 3
* Flask
* Flask-Login
* Flask-WTF (opcional para formulários)
* SQLite (banco de dados leve)
* bcrypt (hash de senha)
* HTML5
* CSS3

⸻

📁 Estrutura do projeto

/sistema-login-seguro
│
├── app.py
├── models.py
├── config.py
├── requirements.txt
│
├── /templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│
├── /static
│   ├── style.css
│
├── /database
│   └── users.db
│
└── README.md

⸻

🔐 Regras de segurança implementadas

Este projeto simula boas práticas reais de segurança:

* As senhas NUNCA são armazenadas em texto puro
* Uso de hash bcrypt para proteção de senhas
* Bloqueio de conta após 5 tentativas de login inválidas
* Mensagens genéricas como:
    “Usuário ou senha inválidos”
    (evita ataque de enumeração de usuários)
* Sessões protegidas com Flask-Login

⸻

⚙️ Como executar o projeto

1. Clone o repositório

git clone https://github.com/seuusuario/sistema-login-seguro.git

2. Acesse a pasta

cd sistema-login-seguro

3. Crie o ambiente virtual (opcional, mas recomendado)

python -m venv venv

4. Ative o ambiente virtual

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate

5. Instale as dependências

pip install -r requirements.txt

6. Execute o projeto

python app.py

7. Acesse no navegador

http://127.0.0.1:5000

⸻

🧠 O que este projeto demonstra

Este projeto foi desenvolvido para demonstrar conhecimentos em:

* Desenvolvimento Web com Flask
* Autenticação de usuários
* Segurança básica de aplicações web
* Hash de senhas e proteção de dados
* Controle de sessões
* Lógica de backend

⸻

📌 Possíveis melhorias futuras

* 🔐 Login com Google (OAuth)
* 📊 Painel administrativo
* 📱 Interface responsiva (mobile)
* 🧠 Recuperação de senha por e-mail
* 🛑 Sistema de captcha contra bots
* 🗄️ Migração para PostgreSQL

⸻

👨‍💻 Autor

Projeto desenvolvido para fins de estudo e portfólio de desenvolvimento web e segurança da informação.

⸻

⭐ Objetivo

Este projeto faz parte da minha evolução como desenvolvedor, com foco em:
backend, segurança e boas práticas de autenticação.