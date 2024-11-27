import streamlit as st
import utils
from functions.hourly_analysis import Hourly_Analysis
from functions.welcome import Welcome
from functions.your_skipass import Your_SkipassPage
from functions.daily_statistics import Daily_Statistics

from functions.test import Test

#main
def main():
    pages = {
        "Home": [st.Page(Welcome, title="Home", icon="🏠", default=True),],
        "Analisi": [
            st.Page(Hourly_Analysis, title="Analisi orarie", icon="🕓"),
            st.Page(Daily_Statistics, title="Analisi giornaliere", icon="📅")
            ],
        "Skipass": [
            st.Page(Your_SkipassPage, title="il tuo skipass", icon="🎟️"),],
        "Test":[
            st.Page(Test, title="Test", icon="🤷‍♂️"),]
    }
    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()
    utils.load_dataset()
    utils.sidebar(st.session_state.passaggi)

if __name__ == "__main__":
    main()



# IDEE

# - selezione giorno in ogni funzione

# - st.feedback("stars")

# - divido in group by data

# - barra inferiore come enri