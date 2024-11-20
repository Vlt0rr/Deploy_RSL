import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from banco_dados import Session, Usuario
from streamlit import title

from criar_admin import usuario

# autenticator usado: pip install streamlit-authenticator==0.3.3(versão mais atual dá erro)

# query que pega todos os usuario e coloca em uma lista python

try:
    lista_usuarios = Session.query(Usuario).all()
except Exception as e:
    Session.rollback()
    print("Erro ao buscar usuários:", e)
finally:
    Session.close()

# lista_usuarios = Session.query(Usuario).all()

# senhas_criptogradas = stauth.Hasher(["1234", "12345", "123456"]).generate()

# preencha os dados que o usuario vai utilizar para fazer login
credenciais = {"usernames":
    {
        usuario.telefone: {"name": usuario.nome, "password": usuario.senha} for usuario in lista_usuarios
    }

}

authenticator = stauth.Authenticate(credenciais, "credenciais_rsl", "fsyklawen48nj", cookie_expiry_days=1)


def autenticar_usuario(authenticator):
    nome, status_autenticacao, username = authenticator.login()

    if status_autenticacao:
        return {"nome": nome, "username": username}
    elif status_autenticacao == False:
        st.error("Usuário ou senha estão errados ou não existem.")
    else:
        st.error("Preencha seus dados para fazer login.")


def logout():
    authenticator.logout()


dados_usuario = autenticar_usuario(authenticator)

if dados_usuario:
    telefone_usuario = dados_usuario["username"]
    usuario = Session.query(Usuario).filter_by(telefone=telefone_usuario).first()

    if usuario.admin:
        pg = st.navigation({
            "Home": [st.Page("homepage.py", title="Formulário")],
            "Análises": [st.Page("tabela.py", title="Base de dados"), st.Page("indicadores.py", title="Indicadores"),
                         st.Page("graficos.py", title="Distribuição de horas por área"),
                         st.Page("planejadoxreal.py", title="Planejado x Real")],
            "Conta": [st.Page(logout, title="Sair"), st.Page("criar_conta.py", title="Criar Conta")]
        })
    else:
        pg = st.navigation({
            "Home": [st.Page("homepage.py", title="Formulário")],
            "Conta": [st.Page(logout, title="Sair")]
        })

    pg.run()
