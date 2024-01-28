# ========================================= CRIANDO TODOS OS FORMULÁRIOS DO SITE ===================================================

# Instalando a biblioteca do Flask para Formulários 
# pip install flask-wtf

# Importando a biblioteca FlaskForm
from flask_wtf import FlaskForm

# Importando do WTForms, para cada tipo de campo, os campos de String, de Senha, de Botão, de Lembrar Dados e de Área de Texto
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField

# Importando do WTForms os Validadores para cada um dos tipos de campos 
# Obs.1: Obrigatórios, Tamanho, Email, de Confirmação e de Validação de Erros
# Obs.2: Por algum motivo não está na biblioteca "Email", então fazer no Terminal o pip install email_validator
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# Importando a Classe Usuario do arquivo "models.py" que cria as Tabelas do Banco de Dados
from comunidadeimpressionadora.models import Usuario

# Importando a biblioteca
# current_user: função aplicada no "navbar.html" para verificar se o Usuário está ou não Logado
from flask_login import current_user

# Importando as bibliotecas
# 1) FileField: Para abrir a Caixa para o Usuário escolher o Arquivo com a Foto
# 2) FileAllowed: É um Validador que permite definir quais Estensões de Arquivos serão permitidas para fazer Upload
from flask_wtf.file import FileField, FileAllowed



# Criando uma Classe para o Formulário de Criar Conta
# Obs.: É uma subclasse do FlaskForm, então passar "(FlaskForm)"
class FormCriarConta(FlaskForm):
    # Definindo os campos necessários ao formulário
    # Obs.: Passando uma Lista com os Validadores "validators = []"
    username = StringField("Nome de Usuário", validators = [DataRequired()])
    email = StringField("E-mail", validators = [DataRequired(), Email()])
    senha = PasswordField("Senha", validators = [DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação da Senha", validators = [DataRequired(), EqualTo("senha")])
    botao_submit_criarconta = SubmitField("Criar Conta")
    # Criando uma função para fazer a Validação do "email"
    # Obs.1: No "models" o campo "email" foi definido com o Parâmetro "unique = True"
    # Obs.2: Para garantirmos que não exista a tentativa de fazer Commit no Banco de Dados e a geração de erro
    # Obs.3: A função obrigatóriamente deverá ter o nome de "validate_email" porque é o que faz o "validate_on_submit()" utilizado no arquivo "routes.py" que define as Funções e Links conseguir fazer essa verificação 
    # Obs.4: Usando "self" por já estar dentro do arquivo "forms.py" que está criando os Formulários
    def validate_email(self, email):
        # Verificando se o "email.data" que foi informado pelo usuário já existe no Cadastro de Emails no Banco de Dados
        # Fazendo uma query no Banco de Dados e atribuindo à variável "usuario"
        usuario = Usuario.query.filter_by(email = email.data).first()
        # Se existir "usuario", exibir a Mensagem de Erro
        if usuario:
            # Exibindo a Mensagem de Erro
            raise ValidationError("E-mail já está cadastrado! Cadastre-se com outro e-mail ou faça Login para continuar.")
        

# Criando uma Classe para o Formulário de Login
# Obs.: É uma subclasse do FlaskForm, então passar "(FlaskForm)"
class FormLogin(FlaskForm):
    # Definindo os campos necessários ao formulário
    # Obs.: Passando uma Lista com os Validadores "validators = []"
    email = StringField("E-mail", validators = [DataRequired(), Email()])
    senha = PasswordField("Senha", validators = [DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField("Lembrar dados de acesso?")
    botao_submit_login = SubmitField("Fazer Login")



# Criando uma Classe para o Formulário para Editar Perfil
# Obs.: É uma subclasse do FlaskForm, então passar "(FlaskForm)"
class FormEditarPerfil(FlaskForm):
    # Definindo os campos necessários ao formulário
    # Obs.1: Passando uma Lista com os Validadores "validators = []"
    # Obs.2: Incluindo o campo "foto_perfil" com as bibliotecas, configurações, parâmetros e lista de Estensões
    username = StringField("Nome de Usuário", validators = [DataRequired()])
    email = StringField("E-mail", validators = [DataRequired(), Email()])
    foto_perfil = FileField("Atualizar Foto de Perfil", validators = [FileAllowed(["jpg", "png"])])
    curso_ciencia = BooleanField("Ciência de Dados")
    curso_excel = BooleanField("Excel")
    curso_vba = BooleanField("VBA")
    curso_powerbi = BooleanField("PowerBI")
    curso_python = BooleanField("Python")
    curso_ppt = BooleanField("PowerPoint")
    curso_sql = BooleanField("SQL")
    botao_submit_editarperfil = SubmitField("Confirmar Edição")
    # Criando uma função para fazer a Validação do "email"
    # Obs.1: No "models" o campo "email" foi definido com o Parâmetro "unique = True"
    # Obs.2: Para garantirmos que não exista a tentativa de fazer Commit no Banco de Dados e a geração de erro
    # Obs.3: A função obrigatóriamente deverá ter o nome de "validate_email" porque é o que faz o "validate_on_submit()" utilizado no arquivo "routes.py" que define as Funções e Links conseguir fazer essa verificação 
    # Obs.4: Usando "self" por já estar dentro do arquivo "forms.py" que está criando os Formulários
    def validate_email(self, email):
        # Verificando se o Usuário está Alterando o seu E-mail
        # Se o E-mail do Usuário for diferente do que ele preencheu no Formulário
        if current_user.email != email.data:
            # Verificando se o "email.data" que foi informado pelo usuário já existe no Cadastro de Emails no Banco de Dados
            # Fazendo uma query no Banco de Dados e atribuindo à variável "usuario"
            usuario = Usuario.query.filter_by(email = email.data).first()
            # Se existir "usuario", exibir a Mensagem de Erro
            if usuario:
                # Exibindo a Mensagem de Erro
                raise ValidationError("Já existe um usuário com esse e-Mail. Cadastre um outro e-mail para continuar.")




# Criando uma Classe para o Formulário para Criar Post
# Obs.: É uma subclasse do FlaskForm, então passar "(FlaskForm)"
class FormCriarPost(FlaskForm):
    # Definindo os campos necessários ao formulário
    # Obs.1: Passando uma Lista com os Validadores "validators = []"
    # Obs.2: Incluindo o campo "foto_perfil" com as bibliotecas, configurações, parâmetros e lista de Estensões
    titulo = StringField("Título do Post", validators = [DataRequired(), Length(2, 140)])
    corpo = TextAreaField("Escreva seu Post aqui!", validators = [DataRequired()])
    botao_submit_criarpost = SubmitField("Enviar Post")

