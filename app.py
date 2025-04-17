import pandas as pd
import streamlit as st

# ------------------------------
# 📥 Carregar os dataframes
# ------------------------------
df_localidades = pd.read_csv("localidades.csv")
df_acidentes = pd.read_csv("acidentes.csv", low_memory=False)

# ------------------------------
# 🔍 Filtrar apenas para RO
# ------------------------------
df_localidades = df_localidades[df_localidades['uf'] == 'RO']
df_acidentes = df_acidentes[df_acidentes['uf_acidente'] == 'RO']

# ------------------------------
# 📊 Agrupar acidentes por município (IBGE)
# ------------------------------
df_acidentes_por_cidade = df_acidentes.groupby('codigo_ibge').size().reset_index(name='total_acidentes')

# ------------------------------
# 🔗 Juntar com dados de localidade
# ------------------------------
df_rank = pd.merge(df_acidentes_por_cidade, df_localidades, on='codigo_ibge')

# ------------------------------
# ❌ Remover dados inválidos (zero ou ausente)
# ------------------------------
df_rank = df_rank[
    (df_rank['qtde_habitantes'] > 0) &
    (df_rank['frota_total'] > 0)
].copy()

# Verificar se há dados suficientes
if df_rank.empty:
    st.error("⚠️ Nenhum município de RO possui dados válidos de frota e população para análise.")
else:
    # ------------------------------
    # 📈 Calcular métricas relativas
    # ------------------------------
    df_rank['acidentes_por_mil_hab'] = (df_rank['total_acidentes'] / df_rank['qtde_habitantes']) * 1000
    df_rank['acidentes_por_mil_veic'] = (df_rank['total_acidentes'] / df_rank['frota_total']) * 1000

    # ------------------------------
    # 🥇 Gerar rankings
    # ------------------------------
    rank_absoluto = df_rank.sort_values(by='total_acidentes', ascending=False).head(10)
    rank_por_habitante = df_rank.sort_values(by='acidentes_por_mil_hab', ascending=False).head(10)
    rank_por_veiculo = df_rank.sort_values(by='acidentes_por_mil_veic', ascending=False).head(10)

    # ------------------------------
    # 📋 Título
    # ------------------------------
    st.title("Ranking de Cidades com Mais Acidentes em RO")

    # ------------------------------
    # 📊 Gráficos
    # ------------------------------
    st.subheader("Ranking Absoluto de Acidentes")
    st.bar_chart(rank_absoluto.set_index('municipio')['total_acidentes'])

    st.subheader("Acidentes por 1.000 Habitantes")
    st.bar_chart(rank_por_habitante.set_index('municipio')['acidentes_por_mil_hab'])

    st.subheader("Acidentes por 1.000 Veículos")
    st.bar_chart(rank_por_veiculo.set_index('municipio')['acidentes_por_mil_veic'])
