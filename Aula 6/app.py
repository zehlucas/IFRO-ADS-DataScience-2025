import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.title("📊 Dashboard de Acidentes - Página Inicial")


# ------------------------------
# 📥 Carregar os dataframes
# ------------------------------
if 'df_localidades' not in st.session_state:
    st.session_state['df_localidades'] = pd.read_csv("../localidades.csv", low_memory=False)
if 'df_acidentes' not in st.session_state:
    st.session_state['df_acidentes'] = pd.read_csv("../acidentes.csv", low_memory=False)

df_localidades = st.session_state['df_localidades']
df_acidentes = st.session_state['df_acidentes']


# ------------------------------
# 📊 Menu lateral para seleção do estado
# ------------------------------

st.sidebar.title("🚦 Análise de Acidentes dos Estados Brasileiros")
opcao = st.sidebar.selectbox(
    "Selecione o estado", ["Todos os Estados"] + df_localidades['uf'].unique().tolist()
)

# ------------------------------
# 🔍 Filtrar apenas para o estado selecionado
# ------------------------------
if opcao != "Todos os Estados":
    df_localidades = df_localidades[df_localidades['uf'] == opcao]
    df_acidentes = df_acidentes[df_acidentes['uf_acidente'] == opcao]


# ------------------------------
# 📅 Filtros temporais
# ------------------------------
st.sidebar.subheader("Filtro de Período")
periodo = st.sidebar.selectbox("Selecione o intervalo", ["Ano inteiro", "1º Trimestre", "2º Trimestre", "3º Trimestre", "4º Trimestre", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])

# ------------------------------
# 📅 Filtros temporais usando ano_acidente e mes_acidente
# ------------------------------
if periodo != "Ano inteiro":
    if "Trimestre" in periodo:
        trimestre = int(periodo[0])
        meses_trimestre = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12]
        }
        df_acidentes = df_acidentes[df_acidentes['mes_acidente'].isin(meses_trimestre[trimestre])]
    else:
        meses = {
            "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
            "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
            "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
        }
        df_acidentes = df_acidentes[df_acidentes['mes_acidente'] == meses[periodo]]


# Criar coluna 'ano_mes' para agrupamento (ex: '2022-01')
df_acidentes['ano_mes'] = df_acidentes['ano_acidente'].astype(str) + '-' + df_acidentes['mes_acidente'].astype(str).str.zfill(2)


st.header("📅 Distribuição Temporal dos Acidentes")

acidentes_por_mes = df_acidentes.groupby('ano_mes').size().reset_index(name='total_acidentes')

fig = px.bar(
    acidentes_por_mes,
    x='ano_mes',
    y='total_acidentes',
    labels={'ano_mes': 'Ano-Mês', 'total_acidentes': 'Total de Acidentes'},
    title="Acidentes por Mês"
)

st.plotly_chart(fig, use_container_width=True)

# Certifique-se de que é string e preencha com zeros à esquerda (caso haja horários como '53400')
df_acidentes['hora_str'] = df_acidentes['hora_acidente'].astype(str).str.zfill(6)

# ✅ Filtra apenas strings válidas no formato HHMMSS (ex: 053400, 123400, etc.)
validos = df_acidentes['hora_str'].str.match(r'^[0-2][0-9][0-5][0-9][0-5][0-9]$')

# ✅ Converte apenas os valores válidos
df_acidentes.loc[validos, 'hora'] = pd.to_datetime(df_acidentes.loc[validos, 'hora_str'], format='%H%M%S').dt.time

# ✅ Remove entradas com hora inválida
df_acidentes = df_acidentes.dropna(subset=['hora'])

# Certifique-se de que 'data_acidente' está em datetime
df_acidentes['data_acidente'] = pd.to_datetime(df_acidentes['data_acidente'], errors='coerce')

# Dia da semana (segunda = 0, domingo = 6)
df_acidentes['dia_semana'] = df_acidentes['data_acidente'].dt.dayofweek

# Nome do dia da semana (segunda, terça, ...)
dias_nome = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
df_acidentes['dia_semana_nome'] = df_acidentes['dia_semana'].map(lambda x: dias_nome[x])

# Extrair hora (inteira) da coluna `hora`
df_acidentes['hora_inteira'] = df_acidentes['hora'].apply(lambda x: x.hour)


heatmap_data = df_acidentes.groupby(['dia_semana_nome', 'hora_inteira']).size().reset_index(name='total')

# Pivotar para formato de matriz
heatmap_pivot = heatmap_data.pivot(index='dia_semana_nome', columns='hora_inteira', values='total').fillna(0)

# Reordenar os dias da semana
heatmap_pivot = heatmap_pivot.reindex(dias_nome)

import plotly.express as px

st.header("🕒 Heatmap de Acidentes por Dia da Semana e Hora")

fig = px.imshow(
    heatmap_pivot,
    labels=dict(x="Hora do Dia", y="Dia da Semana", color="Acidentes"),
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    color_continuous_scale='Reds',
    aspect='auto'
)

st.plotly_chart(fig, use_container_width=True)


# ------------------------------
# Exibição do mapa com os acidentes
# ------------------------------
#st.header("📍 Mapa de Acidentes do Brasil")

df_acidentes_mapa = df_acidentes.copy()
df_acidentes_mapa.rename(columns={"latitude_acidente": "latitude"}, inplace=True)
df_acidentes_mapa.rename(columns={"longitude_acidente": "longitude"}, inplace=True)

df_acidentes_mapa.dropna(subset=['latitude', 'longitude'], inplace=True)
st.header("Mapa de Acidentes do Brasil")
st.map(df_acidentes_mapa, zoom=4, use_container_width=True)



# ------------------------------
# 📊 Agrupar acidentes por município (IBGE)
# ------------------------------
df_acidentes_por_cidade = df_acidentes.groupby('codigo_ibge').size().reset_index(name='total_acidentes')

# Usar apenas uma linha única por cidade para pegar o nome
municipios_unicos = df_localidades[['codigo_ibge', 'municipio']].drop_duplicates(subset='codigo_ibge')

df_acidentes_por_cidade = pd.merge(
    df_acidentes_por_cidade,
    municipios_unicos,
    on='codigo_ibge',
    how='left'
)

# Ordenar do maior para o menor número de acidentes
top5 = df_acidentes_por_cidade.sort_values(by='total_acidentes', ascending=False).head(5)

# Título da seção
#st.header(f"🚗 Top 5 Cidades com Mais Acidentes em {opcao}")

# Gráfico relativo à população
fig = px.bar(
    top5,
    x='municipio',
    y='total_acidentes',
    labels={'municipio': 'Município', 'total_acidentes': 'Acidentes'},
)

# Exibir no Streamlit
st.plotly_chart(fig)


# -----------------------------------
# 👥 Gráfico: Acidentes por mil habitantes
# -----------------------------------

# Obter população única por município
populacao_unica = df_localidades[['codigo_ibge', 'municipio', 'qtde_habitantes']].drop_duplicates(subset='codigo_ibge')

# Juntar população com acidentes
df_relativo = pd.merge(df_acidentes_por_cidade, populacao_unica, on=['codigo_ibge', 'municipio'], how='left')

# Remover municípios com população inválida
df_relativo = df_relativo[df_relativo['qtde_habitantes'] > 0].copy()

# Calcular acidentes por mil habitantes
df_relativo['acidentes_por_mil_hab'] = (df_relativo['total_acidentes'] / df_relativo['qtde_habitantes']) * 1000

# Selecionar top 5 cidades com maior índice relativo
top5_relativo = df_relativo.sort_values(by='acidentes_por_mil_hab', ascending=False).head(5)

# Título do novo gráfico
#st.header(f"📊 Top 5 Cidades com Maior Índice de Acidentes por Habitante em {opcao}")

# Gráfico relativo à população
fig = px.bar(
    top5_relativo,
    x='municipio',
    y='acidentes_por_mil_hab',
    labels={'municipio': 'Município', 'acidentes_por_mil_hab': 'Acidentes por 1.000 Habitantes'},
)

# Exibir no Streamlit
st.plotly_chart(fig)

# -----------------------------------
# 🚘 Gráfico: Acidentes por mil veículos
# -----------------------------------

# Obter frota total por município (único)
frota_unica = df_localidades[['codigo_ibge', 'municipio', 'frota_total']].drop_duplicates(subset='codigo_ibge')

# Juntar com os dados de acidentes
df_veiculos = pd.merge(df_acidentes_por_cidade, frota_unica, on=['codigo_ibge', 'municipio'], how='left')

# Filtrar municípios com frota válida (> 0)
df_veiculos = df_veiculos[df_veiculos['frota_total'] > 0].copy()

# Calcular acidentes por mil veículos
df_veiculos['acidentes_por_mil_veic'] = (df_veiculos['total_acidentes'] / df_veiculos['frota_total']) * 1000

# Selecionar Top 5 cidades com maior índice relativo
top5_veiculos = df_veiculos.sort_values(by='acidentes_por_mil_veic', ascending=False).head(5)

# Título do novo gráfico
#st.header(f"🚘 Top 5 Cidades com Maior Índice de Acidentes por Veículo em {opcao}")

# Criar o gráfico
fig = px.bar(
    top5_veiculos,
    x='municipio',
    y='acidentes_por_mil_veic',
    labels={'municipio': 'Município', 'acidentes_por_mil_veic': 'Acidentes por 1.000 Veículos'},
)

# Exibir no Streamlit
st.plotly_chart(fig)

df_correlacao = df_relativo.merge(
    df_veiculos[['codigo_ibge', 'acidentes_por_mil_veic', 'frota_total']],
    on='codigo_ibge',
    how='inner'
)


# Selecionar apenas as colunas relevantes para correlação
df_corr_vars = df_correlacao[[
    'total_acidentes',
    'qtde_habitantes',
    'frota_total',
    'acidentes_por_mil_hab',
    'acidentes_por_mil_veic'
]]

# Calcular a correlação de Pearson
matriz_corr = df_corr_vars.corr()

st.header("🔗 Correlação entre Variáveis")

fig = px.imshow(
    matriz_corr,
    text_auto=True,
    labels=dict(x="Variáveis", y="Variáveis", color="Correlação"),
    x=matriz_corr.columns,
    y=matriz_corr.index,
    color_continuous_scale="RdBu",
    zmin=-1, zmax=1
)

st.plotly_chart(fig, use_container_width=True)
