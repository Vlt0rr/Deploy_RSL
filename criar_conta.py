import streamlit as st
from banco_dados import Session, Usuario
import streamlit_authenticator as stauth

st.title("criar conta")

form = st.form("form_criar_conta")
nome_usuario = form.text_input("Nome do Usuário")
Tel_usuario = form.text_input("Telefone do usuário")
senha_usuario = form.text_input("Senha do Usuário", type="password")
admin_usuario = form.checkbox("É um admin?")
botao_submit = form.form_submit_button("Enviar")

if botao_submit:
    lista_usuarios_existentes = Session.query(Usuario).filter_by(telefone=Tel_usuario).all()

    if len(lista_usuarios_existentes) > 0:
        st.write("Usuário cadastrado já existe")
    elif len(Tel_usuario) < 9 or len(senha_usuario) < 5:
        st.write("Senha/login não obdecem a regra. A senha deve conter pelo menos 5 caracteres")
    else:
        senha_criptografada = stauth.Hasher([senha_usuario]).generate()[0]
        usuario = Usuario(nome=nome_usuario, senha=senha_criptografada, telefone=Tel_usuario, admin=admin_usuario)

        Session.add(usuario)
        Session.commit()
        st.success("Usuário criado com sucesso!")