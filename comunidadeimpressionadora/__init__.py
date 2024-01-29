# ============================= ARQUIVO QUE INICIALIZA O PROGRAMA COM CONFIGURACÕES DO SITE ====================================

# Instalando a biblioteca Flask Class
# pip install flask
# Importando a biblioteca Flask Class
from flask import Flask

# Instalando a biblioteca flask-sqlalchemy
# pip install flask-sqlalchemy
# Importando a biblioteca SQLAlchemy para o Banco de Dados
from flask_sqlalchemy import SQLAlchemy

# Instalando a biblioteca flask-bcrypt
# pip install flask-bcrypt
# Importando/Criando uma Instância do Bcrypt para Criptografia da senha dos usuários
from flask_bcrypt import Bcrypt

# Instalando a biblioteca flask-login
# pip install flask-login
# Importando a biblioteca flask_login
from flask_login import LoginManager

# Importando a biblioteca os
import os

# # Importando a biblioteca sqlalchemy
import sqlalchemy

# Criando uma instância da Flask classe
app = Flask(__name__)

# Criando um Token para a Segurança dos Formulários do site
# Obs.: Gerando token no Terminal Normal (Não do Ambiente Virtual) com comandos Python: "import secrets" e "secrets.token_hex(16)"
app.config["SECRET_KEY"] = "af2aa2309390e6e9c40952dccb893398"


# ===================================================================================================
# Configurando o app para um caminho na URL do "railway.app" para o Banco de Dados do Servidor
# Se existe esta variável de ambiente
if os.getenv("DATABASE_URL"):
    # Utilizar o Valor desta Variável de Ambiente
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Caso contrário
else:
    # Configurando o app para um caminho Local para o Banco de Dados "comunidade_impressionadora.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade_impressionadora.db" 
# ===================================================================================================    


# Criando a instância do Banco de Dados
# Obs.1: O SQLAlchemy permite a criação da estrutura do Banco de Dados através da criação das Classes no arquivo "forms.py";
# Obs.2: A criação das Tabelas deverá ser realizada no arquivo "models.py"
database = SQLAlchemy(app)

# Criando uma instância Bcryptt() para criptografia da senha do usuário atribuindo à variável "bcrypt"
bcrypt = Bcrypt(app)

# Criando uma instância LoginManager() para gerenciamento do Logina do usuário atribuindo à variável "login_manager"
login_manager = LoginManager(app)

# Direcionando o Usuário para a Página de fazer o Login ou Criar a Conta 
login_manager.login_view = "login"
# Emitindo uma Mensagem de Alerta Personalizada para o Usuário
# O "login_manager.login_message" pode ser omitido e será utilizada a Mensagem Padrão do Flask
login_manager.login_message = "Favor efetuar Login ou Criar Conta para ter acesso"
# Ver as Categorias de Alertas em https://getbootstrap.com/docs/5.0/components/alerts/
login_manager.login_message_category = "alert-info"


# ===================================================================================================
# Se existe esta variável de ambiente
if os.getenv("DATABASE_URL"):
    # Importando "models.py"
    # Obs.: Para carregar as Tabelas que precisarão estar contidas no Banco de Dados
    from comunidadeimpressionadora import models
    # Criando uma engine para avaliar o Banco de Dados
    # Obs.: A variável "engine" recebe o Link do Banco de Dados
    engine = sqlalchemy.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    # Verificando dentro desta engine (Banco de Dados) se ela tem a Tabela de Usuários
    inspector = sqlalchemy.inspect(engine)
    # Se dentro do inspector, ou seja, da engine não tem a Tabela usuario
    # Obs.: Mesmo que o nome da Classe seja Usuario, utilizar em letras minúsculas
    if not inspector.has_table("usuario"):
        # Criando o contexto para não gerar a mensagem de erro
        with app.app_context():
            # Caso tenha criado um Banco de Dados que não tenha a tabela usuario
            # Obs.: Se for criar e já existir gerará um Erro
            database.drop_all()
            # Criando o Banco de Dados
            database.create_all()
            print("Base de Dados criada")
    # Caso contrário
    else:
        print("Base de Dados já existente")
# ===================================================================================================


# Importando "routes.py" para colocar os Links no ar
from comunidadeimpressionadora import routes
# ------------------- IMPORTANTE -------------------- #
# Esta importação deverá ser feita posterior ao app   #
# pois o route() precisa do app para funcionar        #
# Obs.: Caso contrário gerará uma Referência Circular #
# ----------------------------------------------------#



# ---------- ROTEIRO PARA CRIACÃO DE UMA APLICACÃO UTILIZANDO O FRAMEWORK FLASK ---------------
# *********************************************************************************************
#            Estrutura básica obrigatória para funcionamento de uma aplicação Flask
# *********************************************************************************************
# Criação e ativação de um Ambiente Virtual para o Projeto: python -m venv SiteComunidade
# Criar o arquivo main.py para executar o projeto
# Criação de uma pasta para o Projeto (exemplo: comunidadeimpressionadora) que deverá conter:
# 1) Criar a pasta "templates" para organizar as imagens, etc
# 2) Criar o arquivo __init__.py para definição e criação do site
# 3) Criar o arquivo forms.py para criação dos formulários do site
# 4) Criar o arquivo models.py para criação da estrutura de banco de dados do site
# 5) Criar o arquivo routes.py para criação das rotas (links) do site
# *********************************************************************************************


