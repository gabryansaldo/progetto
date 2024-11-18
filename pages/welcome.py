import streamlit as st
from utils import Importa_Tab  

def Welcome():
    st.session_state.passaggi = Importa_Tab("Passaggi.csv")   
    st.write(f"""
        # Benvenuto sul mio sito sui passaggi
        inizio dataset:
    """)
    st.write(st.session_state.passaggi.head(10))