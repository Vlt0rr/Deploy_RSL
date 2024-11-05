from banco_dados import Session, Usuario
import streamlit_authenticator as stauth

senha_criptografada = stauth.Hasher(["12345"]).generate()[0]
usuario = Usuario(nome="Vitor", senha=senha_criptografada, telefone="11963918705", admin=False)

Session.add(usuario)
Session.commit()