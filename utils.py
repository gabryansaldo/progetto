import polars as pl
import streamlit as st

def load_dataset():
    if "passaggi" not in st.session_state:
        st.session_state.passaggi = Importa_Tab("Passaggi.csv")
    if st.session_state.passaggi.is_empty():
        st.error("Errore nel caricamento del dataset.")
        return False
    return True

@st.cache_data
def Importa_Tab(url):
    try:
        passaggi = pl.read_csv(url, separator=",")
        st.session_state.passaggi = CambiaFormatoData(passaggi)
    except Exception as e:
        st.error(f"Errore durante il caricamento del dataset: {e}")
        return pl.DataFrame()
    return st.session_state.passaggi

#cambio formato di DATAPASSAGGIO da str a Datetime
@st.cache_data
def CambiaFormatoData(_table):
    return _table.with_columns(
        pl.col("DATAPASSAGGIO").str.strptime(pl.Datetime, "%d-%m-%Y %H:%M:%S")
    )

# funzione che ritorna una lista contenente le modalità di una data variabile (colonna)
def lista_modalita(table,variabile):
    if variabile not in table.columns:
        st.warning(f"La colonna '{variabile}' non esiste nel dataset.")
        return []
    return table.select(variabile).unique().sort(variabile)

#sidebar con info utili
def sidebar(table):
    if table.is_empty():
        st.sidebar.warning("Nessun dato disponibile nel dataset.")
        return
    n=len(table)

    st.sidebar.header("Informazioni sul Dataset")
    st.sidebar.write(f"""
    - **Totale passaggi:** {n}
    """)

    data_min = table["DATAPASSAGGIO"].min().strftime("%d-%m-%Y")
    data_max = table["DATAPASSAGGIO"].max().strftime("%d-%m-%Y")

    # Mostra intervallo di date
    if data_min == data_max:
        st.sidebar.write(f"- **Data disponibile:** {data_min}")
    else:
        st.sidebar.write(f"- **Date disponibili:** {data_min} - {data_max}")

#dizionario opzioni scelta
def get_opzioni_map():
    return {
        "Valle": "NOME_VALLEPOSIZIONEIMPIANTO",
        "Impianto": "NOME_IMPIANTO",
    }

#raggruppa per skipass
def group_by_skipass(table):
    # if "DATAPASSAGGIO" not in table.columns or "CODICEBIGLIETTO" not in table.columns:
    #     raise ValueError("Colonne richieste mancanti nel dataset.")
    
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.date().alias("data"))  # Estrai solo la data
        .group_by(["data", "CODICEBIGLIETTO"])  # Raggruppa per data e codice skipass
        .agg(pl.count("DATAPASSAGGIO").alias("passaggi"))  # Conta i passaggi
        .sort(["data", "passaggi"], descending=[False, True])  # Ordina per data e passaggi
    )

def units_per_day(table):
    groupskipass=group_by_skipass(table)
    return groupskipass.group_by("data").agg(pl.count("CODICEBIGLIETTO").alias("persone"))