from inspect import stack

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# Estabelecendo a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Pegando os dados existentes da planilha/banco
existing_data = conn.read(worksheet="Dados", usecols=list(range(7)), ttl=5)
existing_data = existing_data.dropna(how="all")

base = existing_data

dados_planejados = {}

# Título da aplicação
st.title("Preencha o formulário abaixo para exibição do Planejado x Real")

# Formulário para entrada de dados
with st.form("formulario"):
    nome_projeto = st.selectbox("Selecione o projeto", base['Projeto'].unique())
    horas_mc_estrutural = st.number_input("Horas Marcenaria Estrutural:", min_value=0, max_value=120, step=1)
    horas_acabamento_geral = st.number_input("Horas Acabamento Geral:", min_value=0, max_value=120, step=1)
    horas_marcenaria_moveis = st.number_input("Horas Marcenaria Movéis:", min_value=0, max_value=120, step=1)
    horas_outros = st.number_input("Horas Outros:", min_value=0, max_value=120, step=1)
    horas_eletrica = st.number_input("Horas Elétrica:", min_value=0, max_value=120, step=1)
    horas_piso = st.number_input("Horas Piso:", min_value=0, max_value=120, step=1)
    horas_hidraulica = st.number_input("Horas Hidráulica:", min_value=0, max_value=120, step=1)

    # Botão de envio
    enviado = st.form_submit_button("Enviar")


    if enviado:
        #cria o dataframe referente as horas planejadas
        df_real = base[base['Projeto'] == nome_projeto]
        # Convertendo as colunas para o formato timedelta
        df_real['Hr_inicio'] = pd.to_timedelta(df_real['Hr_inicio'])
        df_real['Hr_final'] = pd.to_timedelta(df_real['Hr_final'])

        # Calculando a diferença e convertendo para horas, e também criando a nova coluna de horas gastas
        df_real['Horas_Gastas'] = (df_real['Hr_final'] - df_real['Hr_inicio']).dt.total_seconds() / 3600

        #agrupando por area e somando as hrs gastas
        df_real = df_real.groupby('Area')['Horas_Gastas'].sum()

        dados_planejados = {
            'Area': ['Marcenaria estrutural', 'Acabamentos Geral', 'Marcenaria móveis', 'Outros', 'Elétrica', 'Piso', 'Hidráulica'],
            'Horas_Gastas': [horas_mc_estrutural, horas_acabamento_geral, horas_marcenaria_moveis, horas_outros, horas_eletrica, horas_piso, horas_hidraulica]
        }

        st.success("Dados enviados com sucesso!")

# Criar o dataframe
if dados_planejados:

    df = pd.DataFrame(dados_planejados)

    # Merge dos DataFrames para plotagem
    df_merge = pd.merge(df, df_real, on='Area', suffixes=('_Planejado', '_Real'))


    #construindo gráfico
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_merge['Area'],
        y=df_merge['Horas_Gastas_Planejado'],
        name='Planejado'
    ))
    fig.add_trace(go.Bar(
        x=df_merge['Area'],
        y=df_merge['Horas_Gastas_Real'],
        name='Real'
    ))

    # Layout
    fig.update_layout(
        title='Planejado vs. Real',
        xaxis=dict(title='Area'),
        yaxis=dict(title='Horas'),
        barmode='group'
    )
    st.plotly_chart(fig)
    st.warning("Consulte a data de Inicio e Término do projeto na aba de Distribuição de horas por área")