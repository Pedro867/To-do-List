# To-do List

## 📌 Sobre o Projeto
Este projeto foi desenvolvido para demonstrar habilidades em Desenvolvimento Web Full Stack, utilizando Python no backend e práticas modernas de manipulação de banco de dados relacional. A aplicação permite que usuários gerenciem suas rotinas através de um sistema de prioridades, com uma interface limpa.

## 🛠 Principais Funcionalidades
- Autenticação Segura: Sistema de login com criptografia de senhas (werkzeug.security).
- Gestão de Tarefas (CRUD): Criação, leitura, edição e exclusão de tarefas.
- Priorização Dinâmica: Filtros por níveis de importância (Baixa, Média, Alta).
- UX Otimizada: Atualização de status via Fetch API (sem recarregamento de página) e Modais de edição.
- Banco de Dados Relacional: Relacionamento 1:N entre usuários e tarefas com integridade referencial.

## 💻 Tecnologias Utilizadas
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Neon](https://img.shields.io/badge/Neon-00E599?style=for-the-badge&logo=neon&logoColor=black)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

* **Backend:** Python + Flask.
* **ORM:** SQLAlchemy (mapeamento objeto-relacional dinâmico).
* **Banco de Dados:** PostgreSQL hospedado no **Neon.tech** (Cloud Serverless).
* **Frontend:** HTML5, JavaScript (ES6+) e estilização com Bootstrap 5.
* **Segurança:** Proteção de dados com Werkzeug (*Password Hashing*) e gerenciamento de sessões com Flask-Session.

## 🚀 Deploy e Infraestrutura

### 🗄️ Banco de Dados (Cloud)
O projeto utiliza o **[Neon](https://neon.tech/)**, um banco de dados PostgreSQL *Serverless* de alto desempenho.
* **Persistência em Nuvem**: Garante que os dados de usuários e tarefas estejam seguros e acessíveis de qualquer lugar.
* **Segurança**: A conexão utiliza autenticação **Scram-SHA-256** e criptografia **SSL (require)** obrigatória para proteção dos dados em trânsito.
* **Arquitetura**: Beneficia-se do modelo *Scale-to-Zero*, que otimiza recursos durante períodos de inatividade.

### ☁️ Hospedagem (PaaS)
A aplicação está oficialmente hospedada na **[Render](https://render.com/)**.
* **Integração Contínua (CI/CD)**: O deploy é realizado automaticamente a cada atualização no repositório do GitHub.
* **Servidor de Produção**: Para garantir robustez e concorrência, a aplicação roda sob o **Gunicorn** (`gunicorn app:app`).
* **Segurança de Variáveis**: Informações sensíveis (como credenciais do banco) são gerenciadas via *Environment Variables* diretamente no painel da Render, mantendo o arquivo `.env` fora do versionamento público.

## 🚀 Como Executar o Projeto
1. Clone o repositório:
> ```bash
> git clone https://github.com/Pedro867/To-do-List.git
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

## 🧪 Como Executar os Testes
Este projeto possui testes automatizados construídos com **Pytest** para validar o comportamento das rotas da aplicação.

1. Instale as dependências de teste (caso não tenha instalado via requirements.txt):
> ```bash
> pip install pytest pytest-cov
> ```

2. Para rodar os testes:
> ```bash
> pytest
> ```

3. Para gerar o relatório de cobertura de código (Coverage):
> ```bash
> pytest --cov=. --cov-report term-missing
> ```

## Imagens
<img width="1918" height="883" alt="image" src="https://github.com/user-attachments/assets/ad46088d-e0bc-412f-8405-eac937187a09" />
