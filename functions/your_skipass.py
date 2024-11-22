import streamlit as st
import polars as pl
from utils import load_dataset
from utils import group_by_skipass
from utils import units_per_day

def Your_Skipass(table):
    st.title("🎟️ Cerca il tuo Skipass")

    st.write("""
    In questa pagina puoi cercare il tuo skipass utilizzando il suo codice.
    Una volta trovato, visualizzerai i dettagli e le statistiche delle tue attività.
    """)

    codice = st.text_input("Inserisci il codice dello skipass:", placeholder="Es. 161-106-23720")

    if codice:
        skipass_data = table.filter(
            pl.col("CODICEBIGLIETTO") == codice
        )

        if skipass_data.is_empty():
            st.warning("Nessun dato trovato per questo codice skipass.")
        else:
            st.subheader("Dettagli del tuo Skipass")
            st.write(skipass_data)

            st.subheader("Statistiche principali")
            n_passaggi = len(skipass_data)
            primo_passaggio = skipass_data["DATAPASSAGGIO"].min()
            ultimo_passaggio = skipass_data["DATAPASSAGGIO"].max()

            st.markdown(f"**Numero di passaggi totali:** {n_passaggi}")
            st.markdown(f"**Primo passaggio:** {primo_passaggio.strftime('%d-%m-%Y %H:%M:%S')}")
            st.markdown(f"**Ultimo passaggio:** {ultimo_passaggio.strftime('%d-%m-%Y %H:%M:%S')}")

def Your_SkipassPage():
    load_dataset()
    #Your_Skipass(st.session_state.passaggi)
    #st.write(st.session_state.passaggi.sort("CODICEBIGLIETTO"))
    st.write(group_by_skipass(st.session_state.passaggi))


# Icona per la pagina
# Puoi usare l'emoji: 🎟️ (ticket) oppure trovare un'icona SVG da un repository open-source.
