# app.py
# Punto di ingresso principale dell'applicazione, dove vengono creati e gestiti
# i percorsi e le pagine tramite l'uso delle funzioni definite in altri moduli.


import streamlit as st
import utils
from functions.hourly_analysis import Hourly_Analysis
from functions.welcome import Welcome
from functions.your_skipass import Your_SkipassPage
from functions.daily_statistics import Daily_Statistics

# Main dell'applicazione utilizzato per definire le sue pagine
def main():
    utils.load_dataset()
    utils.sidebar(st.session_state.passaggi)
    pages = {
        "Home": [st.Page(Welcome, title="Home", icon="🏠", default=True),],
        "Analisi": [
            st.Page(Hourly_Analysis, title="Analisi orarie", icon="🕓"),
            st.Page(Daily_Statistics, title="Analisi giornaliere", icon="📅")
            ],
        "Skipass": [
            st.Page(Your_SkipassPage, title="il tuo skipass", icon="🎟️"),],
    }
    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()

# Avvio main
if __name__ == "__main__":
    main()
