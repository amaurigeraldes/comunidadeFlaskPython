# ================================== CRIANDO AS FUNCÕES DE PÁGINA E OS LINKS DO SITE ===============================================

# Importando as Instâncias "app", "database" e "bcrypt" do arquivo "__init__.py" da Pasta "comunidadeimpressionadora"
from comunidadeimpressionadora import app, database, bcrypt

# Importando as informações dos Formulários do arquivo "forms.py" 
# 1) FormLogin: para fazer login
# 2) FormCriarConta: para Criar Conta
# 3) FormEditarPerfil: para Editar Perfil
# 4) FormCriarPost: para Criar Criar Post
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost

# Importando as Classes Usuario e Post do arquivo "models.py" que cria as Tabelas do Banco de Dados
from comunidadeimpressionadora.models import Usuario, Post

# Importando a biblioteca secret para Adicionar um Código Aleatório para o Nome da Imagem no Upload de Foto do Perfil
import secrets

# Importando a biblioteca os para separar o nome do arquivo da sua extensão
import os

# Instalando a biblioteca que permite a compactação de Imagens/Fotos
# pip install pillow
# Importando a biblioteca que permite a compactação de Imagens/Fotos
from PIL import Image

# Importando a biblioteca BooleanField para Lembrar Dados nos Campos dos Formulários
from wtforms import BooleanField

# Importando a biblioteca datetime
from datetime import datetime


# Instalando a biblioteca pytz
# pip install pytz
# Importando a biblioteca pytz
import pytz


# Importando as bibliotecas
# 1) login_user: função para fazer o Login do Usuário 
# 2) logout_user: função para fazer o o logout do Usuário
# 3) current_user: função aplicada no "navbar.html" para verificar se o Usuário está ou não Logado
# 4) login_required: função para exigir o Login do Usuário para acessar a Página
from flask_login import login_user, logout_user, current_user, login_required

# Importando as bibliotecas do Flask
from flask import render_template, url_for, request, flash, redirect, abort
# Obs.1: A biblioteca "render_template" retorna o arquivo HTML
# Obs.2: A biblioteca "url_for" padroniza os links das funções do site no navbar.html no href = "{{ url_for('nome_da_funcao')}}"
# Obs.3: A biblioteca "request" para a checagem de qual dos Botões foi Clicado. Motivo: 2 Forms na mesma Página de Login
# Obs.4: A biblioteca "flash" para emitir Mensagens de Alerta
# Obs.5: A biblioteca "redirect" para redirecionar o usuário para a página desejada
# Obs.6: A biblioteca "abort" para Travar a tentaiva de executar uma operação não permitida


# Usar o "route()" decorator para informar ao Flask qual URL deve acionar nossa função
# A função retorna a mensagem que queremos exibir no navegador do usuário. 
# Obs.: O tipo de conteúdo padrão é HTML, portanto o HTML na string será renderizado pelo navegador.


# Criando a rota e a função para a página de início "home.html"
@app.route('/')
def home():
    # Pegando todos os posts e atribuindo à variável "posts"
    # Obs.: Fazendo a Classificação dos Posts na Ordem Decrescente de Número de Id para ser exibido nesta ordem
    posts = Post.query.order_by(Post.id.desc())
    # Renderizando o template da página "home.html"
    # Obs.: Passando a instância "posts" para a página "home.html"
    return render_template("home.html", posts = posts)


# Criando a rota e a função para a página "contato.html"
@app.route('/contato')
def contato():
    # Renderizando o template da página "contato.html"
    return render_template("contato.html")


# Criando a rota e a função para a página "usuarios.html"
@app.route('/usuarios')
# Para acessar a Página o Usuário deverá ter que fazer o Login, obrigatóriamente
@login_required
def usuarios():
    # Definindo a Lista com todos os Usuários
    lista_usuarios = Usuario.query.all()
    # Renderizando o template da página "usuarios.html"
    # Obs.: Passando a instância "lista_usuarios" para a página "usuarios.html"
    return render_template("usuarios.html", lista_usuarios = lista_usuarios)


# Criando a rota e a função para a página "login.html"
# Obs.: Liberando o Método POST usando "methods = ["GET", "POST"]", uma vez que o Método GET é Default
@app.route('/login', methods = ["GET", "POST"])
def login():
    # Importando os Formulários de Login e Criar Conta para a Função "login()"
    # Obs.: Criando as instâncias dos Formulários e atribuindo às variáveis "form_login" e "form_criarconta"
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    # Validando o Formulário de Login na Conta
    # Obs.1: Validando a instãncia "form_login" e o botão "botao_submit_login" foi Clicado
    # Obs.2: Se os Formulários estivessem em páginas diferentes não seria necessária a validação do botão
    if form_login.validate_on_submit() and "botao_submit_login" in request.form:
        # Verificando se o E-mail informado pelo usuário no Formulário existe no Cadastro do Banco de Dados
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        # Se o Usuário existe e a Senha que ele preencheu no Formulário é a mesma que está no Cadastro do Banco de Dados
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # Fazendo efetivamente o Login do Usuário
            # Obs.: Usando o parâmetro "remember = form_login.lembrar_dados.data" para que o Usuário selecione ou não a Caixa
            login_user(usuario, remember = form_login.lembrar_dados.data)
            # Exibindo a mensagem de login com sucesso
            # Obs.1: O "form_login.email.data" é o resultado do campo preenchido pelo usuário no "form_login"
            # Obs.2: "alert-success" ver as Categorias de Alertas em https://getbootstrap.com/docs/5.0/components/alerts/
            flash(f"Login realizado com sucesso para o usuário de-mail: {form_login.email.data}", "alert-success")
            # Verificando/Pegando os Parâmetros de URL que estão no argumento "next" e atribuindo à variável "parametro_next"
            # Obs.: Esta é a Página para onde o Usuário está querendo ir/abrir
            parametro_next = request.args.get("next")
            # Se "parametro_next" existe
            if parametro_next:
                # Redirecionando para a Página do Parâmetro "next"
                return redirect(parametro_next)
            # Caso contrário
            else:
                # Redirecionando para a página "home.html"
                return redirect(url_for("home"))
        # Caso contrário
        else:
            # Exibindo a mensagem de falha no login
            # Obs.1: O "form_login.email.data" é o resultado do campo preenchido pelo usuário no "form_login"
            # Obs.2: "alert-danger" ver as Categorias de Alertas em https://getbootstrap.com/docs/5.0/components/alerts/
            flash(f"Falha no Login. E-mail ou senha incorretos", "alert-danger")
    # Validando o Formulário de Criação da Conta
    # Obs.1: Validando a instãncia "form_criarconta" e o botão "botao_submit_criarconta" foi Clicado
    # Obs.2: Se os Formulários estivessem em páginas diferentes não seria necessária a validação do botão
    if form_criarconta.validate_on_submit() and "botao_submit_criarconta" in request.form:
        # Transformando a senha informada pelo usuário em uma senha criptografada
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # Criando o Usuário no Banco de Dados
        # A variável usuário é uma instância da Classe Usuario
        usuario = Usuario(username = form_criarconta.username.data,
                          email = form_criarconta.email.data,
                          senha = senha_crypt)
        # Adicionando a Sessão no Banco de Dados
        database.session.add(usuario)
        # Fazendo o Commit na Sessão do Banco de Dados
        database.session.commit()
        # Exibir mensagem de Conta criada com sucesso
        # Obs.1: O "form_criarconta.email.data" é o resultado do campo preenchido pelo usuário no "form_criarconta"
        # Obs.2: "alert-success" ver as Categorias de Alertas em https://getbootstrap.com/docs/5.0/components/alerts/
        flash(f"A Conta foi criada com sucesso para usuário do e-mail: {form_criarconta.email.data}", "alert-success")
        # Redirecionando para a página "home.html"
        return redirect(url_for("home"))
    # Renderizando o template da página "login.html"
    # Obs.: Passando as instâncias "form_login" e "form_criarconta" para a página "login.html"
    return render_template("login.html", form_login = form_login, form_criarconta = form_criarconta)


# Saindo da Página
# Criando a rota e a função para a página "home.html"
@app.route("/sair")
# Para acessar a Página o Usuário deverá ter que fazer o Login, obrigatóriamente
@login_required
def sair():
    # Fazendo efetivamente o Logout do Site
    logout_user()
    # Exibindo a mensagem de Logout realizado com sucesso
    flash(f"Logout realizado com sucesso", "alert-success")
    # Redirecionando para a página "home.html"
    return redirect(url_for("home"))


# Indo para a Página de Pefil do Usuário
# Criando a rota e a função para a página "perfil.html"
@app.route("/perfil")
# Para acessar a Página o Usuário deverá ter que fazer o Login, obrigatóriamente
@login_required
def perfil():
    # Definindo o Caminho para a Foto de Perfil do Usuário que está Logado e atribuindo à variável "foto_perfil"
    # Obs.: Informando o Caminho do Campo "foto_perfil" na Tabela Usuario no arquivo "models.py"
    foto_perfil = url_for("static", filename = "fotos_perfil/{}".format(current_user.foto_perfil))
    # Renderizando o template da página "perfil.html"
    # Obs.: Usando o parâmetro "foto_perfil = foto_perfil" para passar a variável "foto_perfil" Python para dentro do HTML
    return render_template("perfil.html", foto_perfil = foto_perfil)


# Indo para a Página de Visualização ou Criação de Posts
# Criando a rota e a função para a página "criar_post.html"
# Obs.: Liberando o Método POST usando "methods = ["GET", "POST"]", uma vez que o Método GET é Default
@app.route("/post/criar", methods = ["GET", "POST"])
# Para acessar a Página o Usuário deverá ter que fazer o Login, obrigatóriamente
@login_required
def criar_post():
    # Importando o Formulário de Criar Post a Função "criar_post()"
    # Obs.: Criando a instâncias do Formulário e atribuindo à variável "form_criar_post"
    form_criar_post = FormCriarPost()
    # Validando o Formulário de Criar Post
    # Obs.: Validando a instãncia "form_criar_post"
    if form_criar_post.validate_on_submit():
        # Criando o Post no Banco de Dados com os Campos do Formulário
        # Obs.: A variável "post" recebe uma Instãncia da Classe Post com os parâmetros "titulo", "corpo" e "autor"
        post = Post(titulo = form_criar_post.titulo.data, corpo = form_criar_post.corpo.data, autor = current_user)
        # Adicionando o Post no Banco de Dados
        database.session.add(post)
        # Fazendo o Commit no Banco de Dados
        database.session.commit()
        # Exibir mensagem de Perfil Atualizado com sucesso
        # Obs.: "alert-success" ver as Categorias de Alertas em https://getbootstrap.com/docs/5.0/components/alerts/
        flash(f"Post criado com sucesso!", "alert-success")
        # Redirecionando para a página "home.html"
        return redirect(url_for("home"))
    # Renderizando o template da página "criar_post.html"
    # Obs.: Passando a instância "form_criar_post" Python para a página "criar_post.html"
    return render_template("criar_post.html", form_criar_post = form_criar_post)




# ***************************************************** FUNCÕES *********************************************************************
# Criando a Função "salvar_imagem" para Salvar a Foto de Perfil do Usuário dentro da Função "editar_perfil"
# Obs.: O objeto "imagem" é a Foto que o Usuário fez Upload
def salvar_imagem(imagem):
    # Adicionando um Código Aleatório para o Nome da Imagem
    # Gerando um Token de 8 bytes e atribuindo à variável "codigo"
    codigo = secrets.token_hex(8)
    # Separando o Nome do Arquivo da Extensão do Arquivo armazenando o Nome numa variável e a Extensão na outra variável
    # Obs.: O objeto "imagem" tem a característica "filename" que é o Nome do Arquivo e a sua Extensão
    nome, extensao = os.path.splitext(imagem.filename)
    # Juntando nome + codigo + extensao e atribuindo à variável "nome_arquivo"
    # Obs.: Fazendo a concatenação
    nome_arquivo = nome + codigo + extensao
    # Definindo o Caminho onde a Foto do Perfil deverá ser Salva na Pasta "static/fotos_perfil"
    # Usando do "os": os.path.join()
    # Usando do "app": app.root_path
    caminho_completo = os.path.join(app.root_path, "static/fotos_perfil", nome_arquivo)
    # Reduzindo o Tamanho da Imagem
    # 1) Criando a variável "tamanho" com uma Tupla (400, 400) para definir o tamanho que a imagem deverá ter
    tamanho = (400, 400)
    # 2) Usando a biblioteca "Image" que permite compactar Imagens/Fotos
    imagem_reduzida = Image.open(imagem)
    # 3) Reduzindo efetivamente a Imagem/Foto
    imagem_reduzida.thumbnail(tamanho)
    # Salvando a Imagem Reduzida na Pasta "static/fotos_perfil"
    imagem_reduzida.save(caminho_completo)
    # Retornando como resultado da Função
    return nome_arquivo


# Criando a Função "atualizar_cursos" para pegar os Cursos selecionados no Perfil do Usuário dentro da Função "editar_perfil"
# Obs.: O objeto "form_editar_perfil" receberá "form_editar_perfil" como parâmetro
def atualizar_cursos(form_editar_perfil):
    # Criando uma Lista de Cursos vazia e atribuindo à variável "lista_cursos"
    lista_cursos = []
    # Percorrendo todos os Campos do Formulário, verificando se o Campo é um dos campos dos cursos disponíveis para selecionar e criando uma Lista com os Cursos
    for campo in form_editar_perfil:
        # Se existir "curso_" no Nome do Campo
        if "curso_" in campo.name:
            # Verificando quais as Caixas dos Cursos do Usuário Logado que estão selecionadas
            if campo.data:
                # Selecionando o texto do "campo.label" (Exemplo: Excel) na Lista de Cursos
                # Obs.: Usando o ".text" para adicionar o texto do "campo.label" na variável "lista_cursos" no Python
                lista_cursos.append(campo.label.text)
    # Transformando a Lista "lista_cursos" em uma String (um texto único) usando o método "';'.join(lista_cursos)"
    lista_cursos = ';'.join(lista_cursos)  
    # Se o Tamanho da String "lista_cursos" for igual a 0
    if len(lista_cursos) == 0:
        # Atribuindo o valor 'Não Informado' à variável "lista_cursos"
        lista_cursos = 'Não Informado'
    # Retornando a String "lista_cursos" como resultado da função para a variável "current_user.cursos"        
    return lista_cursos
# ***********************************************************************************************************************************

# Editando o Perfil do Usuário
# Criando a rota e a função para a página "editar_perfil.html"
# Obs.: Liberando o Método POST usando "methods = ["GET", "POST"]", uma vez que o Método GET é Default
@app.route("/perfil/editar", methods = ["GET", "POST"])
# Para acessar a Página o Usuário deverá ter que fazer o Login, obrigatóriamente
@login_required
def editar_perfil():
    # Importando o Formulário de Editar Perfil a Função "editar_perfil()"
    # Obs.: Criando a instâncias do Formulário e atribuindo à variável "form_editar_perfil"
    form_editar_perfil = FormEditarPerfil()
    # Validando o Formulário de Editar Perfil
    # Obs.: Validando a instãncia "form_editar_perfil"
    if form_editar_perfil.validate_on_submit():
        # Se o Formulário for válido, editar e atualizar as informações desse Usuário
        # Obs.1: O E-mail do Usuário que está Logado será Alterado para o e-mail informado no Formulário de Edição
        # Obs.2: O Username do Usuário que está Logado será Alterado para o username informado no Formulário de Edição
        current_user.email = form_editar_perfil.email.data
        current_user.username = form_editar_perfil.username.data
        # Verificando se o Usuário alterou a Foto do Perfil e atualizar a Foto
        if form_editar_perfil.foto_perfil.data:
            # Se existir uma Foto na Caixa do Formulário, chamando a Função "salvar_imagem"
            # Obs.: Passando como parâmetro a foto carregada na Caixa do Formulário "form_editar_perfil.foto_perfil.data"
            nome_arquivo_imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            # O arquivo "foto_perfil" do Usuário Logado recebe o "nome_arquivo_imagem"
            current_user.foto_perfil = nome_arquivo_imagem
        # Atualizando o Campo de Cursos
        # Obs.1: O campo cursos do Usuário Logado receberá como resultado da Função "atualizar_cursos()" 
        # Obs.2: A Função "atualizar_cursos()" receberá "form_editar_perfil" como parâmetro
        current_user.cursos = atualizar_cursos(form_editar_perfil)
        # Fazendo o Commit no Banco de Dados
        # Obs.: Pois não é necessário adicionar o Usuário, sendo que ele já está adicionado
        database.session.commit()
        # Exibir mensagem de Perfil Atualizado com sucesso
        # Obs.: "alert-success" ver as Categorias de Alertas em https://getbootstrap.com/docs/5.0/components/alerts/
        flash(f"O Perfil foi atualizado com sucesso!", "alert-success")
        # Redirecionando para a página "perfil.html"
        return redirect(url_for("perfil"))
    # Para que o Formulário já apareça com o(s) Campo(s) Preenchidos para o Usuário Logado
    elif request.method == "GET":
        # O E-mail exibido no Formulário será o "email" do Usuário Logado
        form_editar_perfil.email.data = current_user.email
        # O Usuário exibido no Formulário será o "username" do Usuário Logado
        form_editar_perfil.username.data = current_user.username
        # Para que as Caixas dos Cursos selecionados inicialmente já apareçam Clicadas ao Editar Perfil
        # Percorrendo campo na Lista "form_editar_perfil"
        for campo in form_editar_perfil:
            # Percorrendo curso na String "current_user.cursos.split(';')"
            for curso in current_user.cursos.split(';'):
                # Se o Nome do Curso já estiver aparecendo no Campo Label
                if curso in str(campo.label):
                    # Marcar a Caixa do(s) Curso(s) correspondente(s)
                    campo.data = BooleanField(default='checked')
    # Definindo o Caminho para a Foto de Perfil do Usuário que está Logado e atribuindo à variável "foto_perfil"
    # Obs.: Informando o Caminho do Campo "foto_perfil" na Tabela Usuario no arquivo "models.py"
    foto_perfil = url_for("static", filename = "fotos_perfil/{}".format(current_user.foto_perfil))
    # Obs.1: Usando o parâmetro "foto_perfil = foto_perfil" para passar a variável "foto_perfil" Python para dentro do HTML na Página "perfil.html"
    # Obs.2: Usando o parâmetro "form_editar_perfil = form_editar_perfil" para passar a variável "form_editar_perfil" Python para dentro do HTML na Página "editar_perfil.html"
    return render_template("editar_perfil.html", foto_perfil = foto_perfil, form_editar_perfil = form_editar_perfil)




# Indo para a Página de um Post do Usuário
# Criando a rota e a função para a página "post.html", e criando dinâmicamente uma Página para cada Post
# Obs.1: "<post_id>" é uma variável chamada "post_id"
# Obs.2: Liberando o Método POST usando "methods = ["GET", "POST"]", uma vez que o Método GET é Default
@app.route("/post/<post_id>", methods = ["GET", "POST"])
# Para acessar a Página o Usuário deverá ter que fazer o Login, obrigatóriamente
@login_required
# Obs.: A função "exibir_post" recebe "post_id" como variável
def exibir_post(post_id):
    # A variável "post" recebe o Post que tem o mesmo Id da URL
    # O "get" retornará um Post que tem o Id igual a "post_id"
    post = Post.query.get(post_id)
    # Verificando se o Usuário Logado é o Autor do Post
    if current_user == post.autor:
        # Aproveitando o mesmo Formulário utilizado para Criar Post
        # Obs.: O Formulário será exibido
        form_exibir_post = FormCriarPost()
        # Retornando as informações preenchidas pelo Usuário no Título e Corpo ao editar o Post 
        # Fazendo a verificação do método
        # Obs.: Se o usuário estiver Editando o Formulário
        if request.method == "GET":
            # Preenchendo os Campos com as informações para serem Editadas
            form_exibir_post.titulo.data = post.titulo
            form_exibir_post.corpo.data = post.corpo
        # Caso contrário, criando a Lógica para Editar ou Deletar o Post
        # Se o Formulário está validado
        elif form_exibir_post.validate_on_submit():
            # Editando as informações nos Campos do Post
            # Obs.: Passando as informações que o usuário alterar nos campos titulo e corpo
            post.titulo = form_exibir_post.titulo.data
            post.corpo = form_exibir_post.corpo.data
            # Salvando as alterações na Tabela do Database
            # Obs.: Fazendo o commit direto pois o Usuário já está logado na própria conta dele e o Post já existe
            database.session.commit()
            # Exibir mensagem de Post Atualizado com sucesso
            # Obs.: "alert-success" ver as Categorias de Alertas em https://getbootstrap.com/docs/5.0/components/alerts/
            flash(f"O Post foi atualizado com sucesso!", "alert-success")
            # Redirecionando para a página "home.html"
            return redirect(url_for("home"))
    # Caso contrário
    else:
        # Obs.: Nenhum Formulário será exibido
        form_exibir_post = None
    # Renderizando o template da página "post.html"
    # Obs.1: Passando a instância "post" Python para a página "post.html"
    # Obs.2: Passando a instância "form_exibir_post" Python para a página "post.html"
    return render_template("post.html", post = post, form_exibir_post = form_exibir_post)



# Excluindo Post
# Criando a rota e a função para a página "post.html", e criando dinâmicamente uma Página para cada Post
# Obs.1: "<post_id>" é uma variável chamada "post_id"
# Obs.2: Liberando o Método POST usando "methods = ["GET", "POST"]", uma vez que o Método GET é Default
# Obs.3: EM "/post/<post_id>/excluir" o "id" é importante para saber qual Post excluir
@app.route("/post/<post_id>/excluir", methods = ["GET", "POST"])
# Para acessar a Página o Usuário deverá ter que fazer o Login, obrigatóriamente
@login_required
# Obs.: A função "excluir_post" recebe "post_id" como variável
def excluir_post(post_id):
    # A variável "post" recebe o Post que tem o mesmo Id da URL
    # O "get" retornará um Post que tem o Id igual a "post_id"
    post = Post.query.get(post_id)
    # Verificando se o Usuário Logado é o Autor do Post
    if current_user == post.autor:
        # Deletando o Post
        database.session.delete(post)
        # Salvando as alterações na Tabela do Database
        # Obs.: Fazendo o commit direto pois o Usuário já está logado na própria conta dele e o Post já existe
        database.session.commit()
        # Exibir mensagem de Post Atualizado com sucesso
        # Obs.: "alert-success" ver as Categorias de Alertas em https://getbootstrap.com/docs/5.0/components/alerts/
        flash(f"O Post foi excluído com sucesso!", "alert-danger")
        # Redirecionando para a página "home.html"
        return redirect(url_for("home"))
    # Caso contrário
    else:
        # Operação abortada 
        # Obs.1: O usuário está entrando em um Link que não está autorizado
        # Obs.2: Será gerada a Mensagem de Erro Forbidden (Não permitido, proibido)
        abort(403)
        










# # Define o fuso horário de Brasília
# brasil_tz = pytz.timezone('America/Sao_Paulo')
# # # Obtém a data e hora atual em Brasília
# utc_time = datetime.now(brasil_tz)
# # # Transformando UTC para Local
# local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(brasil_tz)

