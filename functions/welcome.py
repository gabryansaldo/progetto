import streamlit as st
import utils

def Welcome():
    utils.background("others/background2.webp")
    
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
    tab1, tab2 = st.tabs(["Benvenuti", "Informazioni"])

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
                animation: fadeIn 3s ease-in-out;
            }

            .subtitle {
                font-size: 24px;
                text-align: center;
                margin-top: 10px;
                color: black;
                animation: fadeIn 5s ease-in-out;
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
                font-weight: normal;
                text-align: left;
                margin-top: 10px;
                color: black;
                animation: fadeIn 2s ease-in-out;
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="header">Introduzione</div>
        <p style="color: black">
            Introduzione generale: "Questa applicazione ti permette di esplorare, analizzare e visualizzare i dati relativi agli skipass per scoprire informazioni utili."
        </p>
        """,unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="header">Cosa Puoi Fare Qui?</div>
        <p style="color: black">
            analisi orarie, giornaliere, vedere tue statistiche e info su tutto
        </p>
        """,unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="header">Informazioni sul dataset</div>
        <p style="color: black">
            come ho ottenuto, dati che contiene (giorni)
        </p>
        """,unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="header">come iniziare</div>
        <p style="color: black">
            sidebar
        </p>
        """,unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="header">cose usate? </div>
        <p style="color: black">
            librerie?
        </p>
        """,unsafe_allow_html=True)

    