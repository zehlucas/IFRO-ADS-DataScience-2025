import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
# ------------------------------
# 📥 Carregar os dataframes
# ------------------------------
df_localidades = pd.read_csv("../localidades.csv", low_memory=False)
df_acidentes = pd.read_csv("../acidentes.csv", low_memory=False)

# ------------------------------
# 📊 Menu lateral para seleção do estado
# ------------------------------

st.sidebar.title("🚦 Análise de Acidentes dos Estados Brasileiros")
opcao = st.sidebar.selectbox(
    "Selecione o estado", ["Todos os Estados"] + df_localidades['uf'].unique().tolist()
)

# ------------------------------
# Exibição do mapa com os acidentes
# ------------------------------
#st.header("📍 Mapa de Acidentes do Brasil")

df_acidentes_mapa = df_acidentes.copy()
df_acidentes_mapa.rename(columns={"latitude_acidente": "latitude"}, inplace=True)
df_acidentes_mapa.rename(columns={"longitude_acidente": "longitude"}, inplace=True)

df_acidentes_mapa.dropna(subset=['latitude', 'longitude'], inplace=True)
st.header("Teste")
st.map(df_acidentes_mapa, zoom=4, use_container_width=True)


# ------------------------------
# 🔍 Filtrar apenas para o estado selecionado
# ------------------------------
if opcao != "Todos os Estados":
    df_localidades = df_localidades[df_localidades['uf'] == opcao]
    df_acidentes = df_acidentes[df_acidentes['uf_acidente'] == opcao]

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
