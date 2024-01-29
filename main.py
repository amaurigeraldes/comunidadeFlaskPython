# ============================================ EXECUTANDO A APLICACÃO DO SITE =================================================

# Importando o "app" do arquivo "__init__" que está na Pasta "comunidadeimpressionadora"
# Obs.: Como o arquivo "__init__" está dentro da Pasta "comunidadeimpressionadora" não é necessário mencioná-lo
from comunidadeimpressionadora import app

# Executando a página somente se "__name__" estiver dentro de "main.py"
# Obs.: Utilizando "debug = True" para que as edições nos Scripts sejam atualizadas no site durante o desenvolvimento
if __name__ == '__main__':
    app.run(debug = False)
