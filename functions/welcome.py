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
            <div class="header">ℹ️ Descrizione</div>
            <p style="color: black">
                <b>Analisi Skipass</b> è un'applicazione interattiva realizzata con Python e librerie come Polars, Streamlit e Altair. L'app permette di esplorare i dati relativi ai passaggi degli skipass su impianti e valli. Grazie a grafici dinamici e analisi dettagliate, è possibile ottenere una visione approfondita dell'utilizzo degli skipass, utile per scopi personali o analisi di mercato.
            </p>
        </div>
        """,unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="box">
            <div class="header">🛠️ Funzionalità</div>
            <p>
                <ul style="color: black">
                    <li><b>Analisi oraria e giornaliera:</b> Visualizza statistiche sulle giornate o sugli orari.</li>
                    <li><b>Confronto tra valli e impianti:</b> Scopri quali sono i luoghi con maggiore affluenza.</li>
                    <li><b>Grafici interattivi:</b> Seleziona, filtra e approfondisci i dati con diversi grafici.</li>
                    <li><b>Esplorazione dello skipass:</b> Verifica i dettagli del tuo skipass e osserva le tue attività.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("""
        <div class="box">
            <div class="header">📃 Informazioni sul dataset</div>
            <p style="color: black">
                Il dataset registra ogni passaggio effettuato nel comprensorio sciistico di <b>Dolomiti Superski</b>, includendo dettagli su skipass, impianto e orario. Copre un periodo limitato, ma può essere aggiornato per analizzare altri giorni.            
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
                Si utilizzi la <b>sidebar</b> a sinistra per navigare tra le pagine dell'applicazione e accedere a tutte le analisi e funzionalità disponibili.
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