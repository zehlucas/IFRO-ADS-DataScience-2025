
# 🧪 Instruções para Início da Aula - Classificação com Jupyter Notebook

Este guia rápido vai te ajudar a garantir que tudo esteja funcionando corretamente antes de começar a aula prática sobre modelos de **classificação** em Ciência de Dados.

---

## ⚠️ Dica rápida antes de começar

Mesmo que tudo pareça certo, rode este comando **dentro do seu notebook Jupyter** antes de iniciar:

```python
!python -m pip install scikit-learn pandas seaborn matplotlib
```

Isso garante que as bibliotecas estejam instaladas corretamente **no ambiente que o Jupyter está usando**.

---

## ✅ 1. Ative seu ambiente virtual

Antes de iniciar o Jupyter Notebook, **ative seu ambiente virtual**.

### No Windows:

```bash
venv\Scripts\activate
```

### No Linux ou macOS:

```bash
source venv/bin/activate
```

---

## ✅ 2. Instale os pacotes dentro do ambiente virtual

Mesmo que o ambiente esteja ativado, é importante garantir que o Jupyter e o Scikit-Learn estejam corretamente instalados.

Execute estes comandos:

```bash
pip install jupyter scikit-learn pandas seaborn matplotlib
```

---

## ✅ 3. Inicie o Jupyter Notebook

Com tudo instalado, inicie o Jupyter Notebook:

```bash
jupyter notebook
```

---

## ✅ 4. Se der erro com `sklearn`, corrija assim

Se aparecer o erro `ModuleNotFoundError: No module named 'sklearn'` mesmo após instalar, execute **dentro do notebook**:

```python
!python -m pip install scikit-learn
```

---

## ✅ 5. Teste rápido

Depois de instalar, teste com este código:

```python
from sklearn.tree import DecisionTreeClassifier
print("Scikit-learn funcionando!")
```

Se aparecer a mensagem, está tudo certo!

---

## 🐧 Dataset da Aula

Usaremos o dataset real dos **Pinguins de Palmer**, disponível no próprio Seaborn.  
Você **não precisa baixar nada**. Basta rodar:

```python
import seaborn as sns
df = sns.load_dataset("penguins")
df.head()
```

---

Se precisar de ajuda, chame o professor! 😄
