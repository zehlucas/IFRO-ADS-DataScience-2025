from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd

model = joblib.load("model.pkl")

app = FastAPI()

class Endereco(BaseModel):
    rua: str
    numero: int

# Classe que representa os nossos alunos
class Aluno(BaseModel):
    horas: float
    nota: float
    presenca: float
    endereco: Endereco

# Rota de predição, para saber se o aluno passou ou não
@app.post("/predict")
def prever(dados: Aluno):
    '''
    teste
    '''
    entrada = pd.DataFrame([{
        "horas_estudo": dados.horas,
        "nota_provas": dados.nota,
        "presenca (%)": dados.presenca
    }])
    predicao = model.predict(entrada)
    return {"Resultado": int(predicao[0])}