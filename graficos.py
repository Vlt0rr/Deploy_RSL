import pandas as pd
import plotly.express as px
import streamlit as st

from data_loader import carregar_dados

base = carregar_dados()

# Verificar e corrigir valores inválidos nas colunas de hora
base['Hr_inicio'] = pd.to_datetime(base['Hr_inicio'], format='%H:%M:%S', errors='coerce')
base['Hr_final'] = pd.to_datetime(base['Hr_final'], format='%H:%M:%S', errors='coerce')
base = base.dropna(subset=['Hr_inicio', 'Hr_final'])

# Converter a coluna 'Data' para o formato datetime
base['Data'] = pd.to_datetime(base['Data'], errors='coerce')

# Calcular o total de horas trabalhadas para cada entrada
base['Horas_trabalhadas'] = (base['Hr_final'] - base['Hr_inicio']).dt.total_seconds() / 3600

# Seleção de projeto pelo usuário
projeto_selecionado = st.selectbox("Selecione o projeto", base['Projeto'].unique())

# Filtrar os dados pelo projeto selecionado
filtro_projeto = base[base['Projeto'] == projeto_selecionado]

# Seleção de intervalo de datas pelo usuário
intervalo_datas = st.date_input("Selecione o intervalo de datas", [])

# Verificar se o usuário selecionou duas datas
if len(intervalo_datas) == 2:
    data_inicio, data_fim = intervalo_datas
    # Aplicar o filtro de data
    filtro_projeto = filtro_projeto[(filtro_projeto['Data'] >= pd.to_datetime(data_inicio)) &
                                    (filtro_projeto['Data'] <= pd.to_datetime(data_fim))]

# Calcular o total de horas trabalhadas por área para o projeto e período selecionados
horas_por_area = filtro_projeto.groupby('Area')['Horas_trabalhadas'].sum().reset_index()

# Criar o gráfico com todas as áreas para o projeto e período selecionados
fig = px.bar(horas_por_area, x='Area', y='Horas_trabalhadas', title="Total de Horas Trabalhadas por Área")
st.plotly_chart(fig)
