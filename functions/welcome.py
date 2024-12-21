import streamlit as st
import utils
from pathlib import Path

def Welcome():
    file_path = Path("others") / "background_welcome.webp"
    utils.background(file_path)
    
    st.markdown(
    """
        <style>
        div[data-testid="stTabs"] button {
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    tab1, tab2, tab3 = st.tabs(["Benvenuti", "Informazioni","Guida"])
    st.header("PAGINA CON I TESTI ANCORA DA DEFINIRE")


    with tab1:
        st.markdown(
        """
            <style>
            .title {
                font-size: 48px;
                font-weight: bold;
                text-align: center;
                margin-top: 50px;
                color: black;
                animation: fadeIn 2s ease-in-out;
            }

            .subtitle {
                font-size: 24px;
                text-align: center;
                margin-top: 10px;
                color: black;
                animation: fadeIn 3s ease-in-out;
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            </style>
        """,unsafe_allow_html=True,)
        st.markdown(
            """
            <div class="title">Benvenuto nell'applicazione di Analisi dei Passaggi</div>
            <div class="subtitle">Esplora dati, analizza passaggi e ottieni insights.</div>
            """,
            unsafe_allow_html=True
        )

    with tab2:
        st.markdown("""
            <style>
            .header {
                font-size: 24px;
                font-weight: bold;
                text-align: left;
                margin-top: 10px;
                color: black;
                animation: fadeIn 1s ease-in-out;
            }
            .box {
                border-radius: 20px; 
                padding: 16px; 
                background-color: rgba(200, 218, 221, 0.80); 
                margin-bottom: 16px;
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="box">
            <div class="header">ℹ️ Introduzione</div>
            <p style="color: black">
                Introduzione generale: "Questa applicazione ti permette di esplorare, analizzare e visualizzare i dati relativi agli skipass per scoprire informazioni utili."
            </p>
        </div>
        """,unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="box">
            <div class="header">📃 Informazioni sul dataset</div>
            <p style="color: black">
                come ho ottenuto, dati che contiene (giorni)
            </p>
        </div>
        """,unsafe_allow_html=True)

        st.divider()
    
    with tab3:
        st.markdown("""
            <style>
            .header {
                font-size: 24px;
                font-weight: bold;
                text-align: left;
                margin-top: 10px;
                color: black;
                animation: fadeIn 1s ease-in-out;
            }
            .box {
                border-radius: 20px; 
                padding: 16px; 
                background-color: rgba(200, 218, 221, 0.80); 
                margin-bottom: 16px;
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="box">
            <div class="header">❓ Cosa puoi fare qui?  come iniziare  lib usate</div>
            <p style="color: black">
                analisi orarie, giornaliere, vedere tue statistiche e info su tutto
            </p>
        </div>
        """,unsafe_allow_html=True)
