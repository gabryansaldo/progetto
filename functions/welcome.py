import streamlit as st
import utils
from pathlib import Path

# funzione main della pagina, scrive titolo ecc
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
    tab1, tab2, tab3 = st.tabs(["Benvenuti", "Informazioni","Esempio Dataset"])

    with tab1:
        st.markdown(
        """
            <style>
            .pretitle {
                font-size: 30px;
                text-align: center;
                margin-top: 60px;
                color: black;
                animation: fadeIn 1s ease-in-out;
            }

            .title {
                font-size: 60px;
                font-weight: bold;
                text-align: center;
                margin-top: 0px;
                color: black;
                animation: fadeIn 2s ease-in-out;
            }

            .subtitle {
                font-size: 22px;
                text-align: center;
                margin-top: 5px;
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
            <div class="pretitle">Benvenuto nell'Applicazione di</div>
            <div class="title">Analisi SkiPass</div>
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
                Questa applicazione offre strumenti avanzati per l'analisi dei passaggi sugli impianti sciistici. Grazie a grafici interattivi, puoi esplorare e approfondire analisi giornaliere e orarie relative a skipass, impianti e valli. Ideale per scoprire trend, preferenze dei visitatori e supportare decisioni strategiche come analisi di mercato.
            </p>
        </div>
        """,unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="box">
            <div class="header">📃 Informazioni sul dataset</div>
            <p style="color: black">
                Il dataset utilizzato rappresenta ogni passaggio su un impianto sciistico, corrispondente a un utilizzo di skipass da parte di una persona. Ogni riga contiene informazioni dettagliate sullo skipass, sull'impianto in cui è stato utilizzato e sull'orario del passaggio. Attualmente, il dataset copre un numero limitato di giorni, ma è possibile elaborare anche periodi diversi semplicemente aggiornando il dataframe.
            </p>
            <p style="color: black">
                Questo subpull di dati è stato fornito in forma anonima dal federconsorzi <a href="https://www.dolomitisuperski.com/" target="_blank">Dolomiti Superski</a> al fine di poter implementare questa applicazione.
            </p>
        </div>
        """,unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="box">
            <div class="header">❓ Come iniziare</div>
            <p style="color: black">
                Si utilizzi la sidebar a sinistra per navigare tra le pagine dell'applicazione e accedere a tutte le analisi e funzionalità disponibili.
            </p>
        </div>
        """,unsafe_allow_html=True)
    
    with tab3:
        utils.load_dataset()
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
            <div class="header">Esempio di Dataset</div>
            <p style="color: black">
                Di seguito vengono riportate le prime 100 righe del dataset utilizzato nell'applicazione, come esempio rappresentativo dei dati analizzati.
            </p>
        </div>
        """,unsafe_allow_html=True)

        st.dataframe(st.session_state.passaggi[:100])