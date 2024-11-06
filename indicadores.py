import streamlit as st
from streamlit import container
from data_loader import carregar_dados
from homepage import coluna_esquerda, coluna_direita
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# Estabelecendo a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Pegando os dados existentes da planilha/banco
existing_data = conn.read(worksheet="Dados", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")

base = existing_data

st.title("Indicadores")

def criar_card(icone, numero, texto, coluna_card):
    container = coluna_card.container(border=True)
    coluna_esquerda, coluna_direita = container.columns([1, 2.5])
    coluna_esquerda.image(f"imagem/{icone}")
    coluna_direita.write(numero)
    coluna_direita.write(texto)
    carregar_dados()

coluna_esquerda, coluna_meio, coluna_direita = st.columns([1, 1, 1])

# Número total de projetos distintos
total_projetos = base['Projeto'].nunique()

# Número total de projetos finalizados (distintos) - onde 'Data_termino' não é nulo
total_projetos_finalizados = base.loc[base['Data_termino'].notna(), 'Projeto'].nunique()

# Calcula o total de projetos em andamento como a diferença
total_proj_andamento = total_projetos - total_projetos_finalizados


criar_card("oportunidades.png", f'{base['Projeto'].nunique()}', "Total de projetos", coluna_esquerda)
criar_card("em_andamento.png", f"{total_proj_andamento}", "Em andamento", coluna_meio)
criar_card("Projetos_fechados.png", f'{base['Data_termino'].notna().sum()}', "Finalizados", coluna_direita)


# Calculando o percentual de progresso
percentual_progresso = (total_projetos_finalizados / total_projetos) * 100

# Exibindo o gráfico de progresso no Streamlit
st.write("## Progresso dos Projetos")
st.progress(percentual_progresso / 100)  # Dividido por 100 para obter o valor entre 0 e 1

# Exibindo o percentual em número
st.write(f"Progresso: {percentual_progresso:.2f}%")

#GRÁFICO DE PIZZA


# Preparando os dados para o gráfico de pizza
labels = ['Projetos Finalizados', 'Projetos em Andamento']
sizes = [total_projetos_finalizados, total_proj_andamento]

# Criando o gráfico de pizza com Plotly
fig = px.pie(values=sizes, names=labels, title="Distribuição dos Projetos", hole=0.3)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig)
