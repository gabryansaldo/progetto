import streamlit as st
from utils import Importa_Tab
from utils import sidebar
from pages.analisi import Analisi_oraria
from pages.welcome import Welcome

#main
def main():
    pages = {
        "Home": [
            st.Page(Welcome, title="Home", icon="🏠", default=True),
        ],
        "Analisi": [
            st.Page(Analisi_oraria, title="Analisi orarie", icon="📈"),
        ],
    }
    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()
    st.session_state.passaggi = Importa_Tab("Passaggi.csv")
    sidebar(st.session_state.passaggi)

if __name__ == "__main__":
    main()

# IDEE

# - grafico per ora per impianto... in analisi passaggi orari (forse non ha senso)

# - st.feedback("stars")

# - tasti in home per cambiare pagina

# - TASTI PER CAMBIARE PAGINA PIù BELLI NON RIESCO AAAAA

# - quasifatto --> USA funzioni per pagine che richiamano funzioni main degli altri file, non ricordo ma cerca comandi su api ost.page o navigation

# - pagina benvenuto

# - capire come mettere le altre pagine in una cartella