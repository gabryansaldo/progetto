import streamlit as st
from utils import load_dataset
from utils import sidebar
from functions.hourly_analysis import Hourly_Analysis
from functions.welcome import Welcome
from functions.your_skipass import Your_SkipassPage
from functions.daily_statistics import Daily_Statistics

#main
def main():
    pages = {
        "Home": [st.Page(Welcome, title="Home", icon="🏠", default=True),],
        "Analisi": [
            st.Page(Hourly_Analysis, title="Analisi orarie", icon="🕓"),
            st.Page(Daily_Statistics, title="Analisi giornaliere", icon="📅")
            ],
        "Skipass": [
            st.Page(Your_SkipassPage, title="il tuo skipass", icon="🎟️"),]
    }
    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()
    load_dataset()
    sidebar(st.session_state.passaggi)

if __name__ == "__main__":
    main()



# uv run streamlit run main.py



# IDEE

# - grafico per ora per impianto... in analisi passaggi orari altair

# - st.feedback("stars")

# - tasti in home per cambiare pagina

# - divido in group by data