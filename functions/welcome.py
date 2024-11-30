import streamlit as st
import utils

def Welcome():
    bg_image = utils.get_base64("others/background2.webp")

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
    tab1, tab2, tab3 = st.tabs(["Benvenuti", "Informazioni", "Guida"])

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)  #attachment: scroll ma non va

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
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="title">Benvenuto nell'applicazione di Analisi dei Passaggi</div>
            <div class="subtitle">Esplora dati, analizza passaggi e ottieni insights.</div>
            """,
            unsafe_allow_html=True
        )

    with tab2:
        st.markdown("""
        <p style="color: black; background: none; font-size: 16px; text-align: left;">
            ## 2. Cosa Puoi Fare Qui?
            Introduzione generale: "Questa applicazione ti permette di esplorare, analizzare e visualizzare i dati relativi agli skipass per scoprire informazioni utili."


            ## 3. Seleziona l'Analisi che Vuoi Esplorare
            Analisi Oraria: "Esplora i passaggi per ora, sia in totale che per impianto o valle."
            Dettagli Skipass: "Consulta le informazioni dettagliate sui tuoi skipass e scopri come vengono utilizzati."
            Statistiche Personali: "Analizza la distribuzione dei tipi di persona e altre informazioni demografiche."

            ---

            ## 4. Funzionalità Principali
            Visualizza Passaggi Orari: "Accedi all'analisi delle ore di utilizzo degli skipass e visualizza i picchi di traffico."
            Esplora per Valle o Impianto: "Filtra i dati per valle o impianto e scopri dove vengono effettuati più passaggi."
            Confronta Tipi di Biglietto: "Confronta l'uso dei diversi tipi di biglietto e scopri quale è più popolare."

            ---

            ## 5. Statistiche e Tendenze
            Vedi la Classifica dei Tipi di Persona: "Analizza quanti utenti hanno utilizzato il tuo impianto e dividi per categorie come maschio, femmina, o bambini."
            Panoramica Generale dei Passaggi: "Ottieni una panoramica generale del traffico giornaliero e le tendenze sugli impianti e valli."

            ---

            ## 6. Esplora e Filtra i Dati
            Scegli come Filtrare i Dati: "Puoi scegliere di visualizzare i dati per specifici impianti, valli o tipi di biglietto."
            Filtra per Data: "Esplora i dati in base alle date specifiche per avere una visione più dettagliata."

            ---

            ## 7. Risultati e Visualizzazioni
            Grafici e Tabelle Interattive: "Visualizza i risultati sotto forma di grafici e tabelle interattive per un'analisi approfondita."
            Personalizza la tua Analisi: "Adatta le visualizzazioni ai tuoi bisogni e scopri insight specifici."

            ---

            ## 8. Perché Usare Questa Applicazione?
            Semplicità e Accessibilità: "Interfaccia user-friendly che ti consente di esplorare facilmente i dati senza complicazioni."
            Analisi Approfondita: "Fornisce un'analisi approfondita dei passaggi degli skipass, ottimizzata per la tua esperienza."

            ---

            ## 9. Inizia Subito!
            Guida rapida: "Segui le istruzioni qui sotto per iniziare la tua analisi. Scegli il tipo di visualizzazione che ti interessa di più e inizia a esplorare!"
            Pulsante o link: "Inizia ora" o "Esplora i Dati"
            
            ---
                
            ## 10. Informazioni sul Dataset
            Origine del Dataset: "Questo dataset contiene informazioni dettagliate sui passaggi degli utenti su impianti sciistici. I dati sono stati raccolti da un sistema di biglietteria che traccia gli skipass utilizzati durante la giornata."
            Struttura dei Dati: "Il dataset è composto da diverse colonne che contengono dati cruciali per l'analisi degli impianti e delle valli, nonché informazioni sui tipi di biglietti e sui passeggeri."
        </p>
        """, unsafe_allow_html=True)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    