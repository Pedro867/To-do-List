# [To-do-List]

## 📌 Sobre o Projeto
Este projeto foi desenvolvido para demonstrar habilidades em Desenvolvimento Web Full Stack, utilizando Python no backend e práticas modernas de manipulação de banco de dados relacional. A aplicação permite que usuários gerenciem suas rotinas através de um sistema de prioridades, com uma interface limpa.

## 🛠 Principais Funcionalidades
- Autenticação Segura: Sistema de login com criptografia de senhas (werkzeug.security).
- Gestão de Tarefas (CRUD): Criação, leitura, edição e exclusão de tarefas.
- Priorização Dinâmica: Filtros por níveis de importância (Baixa, Média, Alta).
- UX Otimizada: Atualização de status via Fetch API (sem recarregamento de página) e Modais de edição.
- Banco de Dados Relacional: Relacionamento 1:N entre usuários e tarefas com integridade referencial.

## 💻 Tecnologias Utilizadas
- Backend: Python + Flask
- ORM: SQLAlchemy do Flask
- Banco de Dados: PostgreSQL
- Frontend: Bootstrap 5, HTML5, JavaScript (ES6+)
- Segurança: Werkzeug (Password Hashing), Flask-Session

## 🚀 Como Executar o Projeto
1. Clone o repositório:
> ```bash
> git clone https://github.com/seu-usuario/seu-repositorio.git
> cd seu-repositorio
> Crie e ative um ambiente virtual:
> ```

2. Crie e ative um ambiente virtual:
> ```bash
> python -m venv venv
> # No Windows:
> venv\Scripts\activate
> # No Linux/Mac:
> source venv/bin/activate
> ```

3. Instale as dependências:
> ```bash
> pip install -r requirements.txt
> ```

4. Configure o Banco de Dados:
Crie um banco PostgreSQL e configure a DATABASE_URL no seu arquivo .env

5. Inicie a aplicação:
> ```bash
> python app.py
> ```

## Imagens
<img width="1918" height="883" alt="image" src="https://github.com/user-attachments/assets/ad46088d-e0bc-412f-8405-eac937187a09" />
