import streamlit as st
import requests

st.set_page_config(page_title="Predição de Alunos", page_icon="🎓")

st.title("🎓 Predição de Aprovação do Aluno")
st.write("Preencha os dados abaixo para saber se o aluno foi aprovado.")

# Formulário
horas = st.slider("Horas de estudo por dia", 0.0, 6.0, step=0.5)
nota = st.slider("Nota nas provas", 0.0, 100.0, step=1.0)
presenca = st.slider("Presença (%)", 0.0, 100.0, step=1.0)
rua = st.text_input("Rua")
numero = st.number_input("Número", step=1)

if st.button("🔮 Prever"):
    payload = {
        "horas": horas,
        "nota": nota,
        "presenca": presenca,
        "endereco": {
            "rua": rua,
            "numero": int(numero)
        }
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            resultado = response.json()["Resultado"]
            st.success(f"✅ Resultado da predição: **{resultado}**")
        else:
            st.error(f"Erro: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Não foi possível conectar à API. Verifique se o servidor FastAPI está rodando.")
