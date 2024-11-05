import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Estabelecendo a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Pegando os dados existentes da planilha/banco
existing_data = conn.read(worksheet="Dados", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")

# Exiba o DataFrame no Streamlit
st.subheader('Dados preenchidos pelos usuários')
st.dataframe(existing_data)
