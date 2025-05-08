import streamlit as st

session = st.session_state

if 'cont' not in session:
    session.cont = 0
print(session)
if st.button('Adicionar'):
    session.cont += 1

st.write(session.cont)