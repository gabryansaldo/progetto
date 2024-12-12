import streamlit as st
import utils
from functions.hourly_analysis import Hourly_Analysis
from functions.welcome import Welcome
from functions.your_skipass import Your_SkipassPage
from functions.daily_statistics import Daily_Statistics

from functions.test import Test

#main
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
        "Test":[
            st.Page(Test, title="Test", icon="🤷‍♂️"),]
    }
    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()
    

if __name__ == "__main__":
    main()



# DA FARE

# - modificare testo nelle info in welcome

# - usare colorspace

# - analisi per tipo di biglietto

# - analisi per valle (impianto più usato, pos. classifica valli, npassaggi, persone) foto descizione

# - indice di affollamento giorno (capire asse y) groupby minuto grafico

# - session.state per altri dataset generici

# - mappa impianti con geopandas

# - usare column configuration in st.dataframe (linechartcolumn, format)

# - abbellire sidebar, aggiungere tot persone

# - togliere container daily analysis e lasciare tot pers. giorno/totale selezionato all'inizio aggiungere giorno record contenuto nel dataset

