import streamlit as st
import utils
import base64
import streamlit as st
import pandas as pd
import numpy as np
import time


def Test():

    def get_base64(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # Percorso all'immagine di sfondo
    bg_image = get_base64("others/logo.webp")

    # HTML e CSS per impostare lo sfondo
    html = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """

    # Iniezione dello stile nella pagina
    st.markdown(html, unsafe_allow_html=True)

    # Contenuto della Home Page
    st.title("Benvenuto nella Gestione degli Skipass!")
    st.write("Esplora dati, analizza passaggi, e ottieni insights sul tuo impianto sciistico.")

    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



