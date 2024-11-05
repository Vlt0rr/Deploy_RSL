import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection


# Estabelecendo a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Pegando os dados existentes da planilha/banco
existing_data = conn.read(worksheet="Dados", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")

@st.cache_data
def carregar_dados():
    tabela = existing_data
    return tabela


