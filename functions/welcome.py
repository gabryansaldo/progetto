import streamlit as st
from utils import load_dataset

def Welcome():
    load_dataset()  
    st.write(f"""
        # Benvenuto sul mio sito sui passaggi
        inizio dataset:
    """)
    st.write(st.session_state.passaggi.head(10))
    st.feedback("stars")