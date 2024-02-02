# ================================= CRIANDO TODAS AS BASES E TABELAS DO BANCO DE DADOS ============================================

# Criando um Banco de Dados para armazenar as informações dos Usuários, os Posts, etc

# Importando o "database" e o "login_manager" do arquivo "__init__.py" da Pasta "comunidadeimpressionadora"
# Obs.: O "database" é quem utiliza o SQLAlchemy
from comunidadeimpressionadora import database, login_manager

# Importando a biblioteca datetime
from datetime import datetime

# Importando a biblioteca UserMixin 
# É um parâmetro que será passado para a Classe Usuario e que atribuirá a essa Classe todas as características necessárias que o "login_manager" precisa para controlar o Login e para manter o Login conectado quando o usuário sai do Site
from flask_login import UserMixin


# O "@login_manager.user_loader" diz que a Função "load_usuario" carrega o Usuário
@login_manager.user_loader
# Criando uma Função para fazer o Login do Usuário
# Obs.: Passando o "id_usuario"
def load_usuario(id_usuario):
    # Encontrando um usuário que tenha o "id_usuario"
    return Usuario.query.get(int(id_usuario))


# Construindo a Tabela "Usuario" no Banco de Dados
# Obs.1: É uma Subclasse que receberá como herança de uma outra Classe padrão de Banco de Dados do SQLAlchemy "database.Model"
# Obs.2: Não será necessário definir o "__init__" e de criar uma série de coisas que já virão prontas e aparecerão no Banco de Dados
# Obs.3: Passando o parâmetro de "UserMixin" para o "login_manager" controlar o Login
class Usuario(database.Model, UserMixin):
    # Criando as Colunas do Banco de Dados
    # Obs.1: Definir qual é o tipo da Coluna: Integer, String, Text, DateTime
    # Obs.2: Parâmetro "primary_key = True" é a Chave Primária única que é preenchida automaticamente
    # Obs.3: Parâmetro "nullable = False" para definir que não pode ser um campo vazio
    # Obs.4: Parâmetro "unique = True" para definir que o campo precisará ter um valor único
    # Obs.5: Parâmetro "default = 'default.jpg'" para definir uma imagem padrão para o Campo, caso ainda não haja uma Foto do Usuário
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, nullable = False)
    email = database.Column(database.String, unique = True, nullable = False)
    senha = database.Column(database.String, nullable = False)
    cursos = database.Column(database.String, nullable = False, default = "Não Informado")
    foto_perfil = database.Column(database.String, default = "default.jpg")
    # Relacionando o Usuário com o Post
    # Obs.1: Parâmetro "backref = "autor"" para relacionar o Post com que criou o Post
    # Obs.2: Parâmetro "lazy = True" para passar para o Banco de Dados todas as informações do autor
    posts = database.relationship("Post", backref = "autor", lazy = True)
    
    # Criando um método exclusivo do Usuário
    # Obs.: Só vai receber como parâmetro o "self" que é a instãncia do Usuário 
    def contar_posts(self):
        # Retorna como resposta a quantidade de posts
        return len(self.posts)





# Construindo a Tabela "Post" no Banco de Dados
# Obs.1: É uma Subclasse que receberá como herança de uma outra Classe padrão de Banco de Dados do SQLAlchemy "database.Model"
# Obs.2: Não será necessário definir o "__init__" e de criar uma série de coisas que já virão prontas e aparecerão no Banco de Dados
class Post(database.Model):
    # Criando as Colunas do Banco de Dados
    # Obs.1: Definir qual é o tipo da Coluna: Integer, String, Text, DateTime
    # Obs.2: Parâmetro "primary_key = True" para chave primária única que é preenchida automaticamente
    # Obs.3: Parâmetro "nullable = False" para definir que não pode ser um campo vazio
    # Obs.4: Parâmetro "unique = True" para definir que o campo precisará ter um valor único
    # Obs.5: Parâmetro "default = 'datetime.utcnow'" para definir a Data conforme Fuso Horário UTC.
    id = database.Column(database.Integer, primary_key = True)
    titulo = database.Column(database.String, nullable = False)
    corpo = database.Column(database.Text, nullable = False)
    data_criacao = database.Column(database.DateTime, nullable = False, default = datetime.now())
    # Criando a Coluna para o Relacionando com o Usuário que criou o Post
    # Obs.1: O parâmetro ForeignKey é quem cria a relação entre a Class Post e a Class Usuario
    # Obs.2: O parâmetro "database.ForeignKey("usuario.id")" Chave Extrangeira é posicional e não poderá ser o último parâmetro
    # Obs.3: O parâmetro "database.ForeignKey("usuario.id")" passar a Class "Usuario" em minúsculas concatenando com o Atributo "id"
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable = False)
