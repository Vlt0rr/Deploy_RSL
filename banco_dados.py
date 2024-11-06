import streamlit as st
from sqlalchemy import create_engine, Integer, String, Boolean, Column
from sqlalchemy.orm import sessionmaker, declarative_base


# Obter informações do banco de dados a partir das variáveis de ambiente
username = st.secrets["database"]["DB_USERNAME"]
password = st.secrets["database"]["DB_PASSWORD"]
host = st.secrets["database"]["DB_HOST"]
port = st.secrets["database"]["DB_PORT"]
database = st.secrets["database"]["DB_NAME"]

# Crie a URL de conexão
db_url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'

# Crie a engine de conexão
db = create_engine(db_url)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    senha = Column("senha", String)
    telefone = Column("telefone", String)
    admin = Column("admin", Boolean)

    def __init__(self, nome, senha, telefone, admin=False):
        self.nome = nome
        self.senha = senha
        self.telefone = telefone
        self.admin = admin

# Cria as tabelas no banco de dados
Base.metadata.create_all(db)
