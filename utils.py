import polars as pl
import streamlit as st

@st.cache_data
def Importa_Tab(url):
    if "passaggi" not in st.session_state:
        passaggi = pl.read_csv(url, separator=",")
        st.session_state.passaggi = CambiaFormatoData(passaggi)
    return st.session_state.passaggi

#cambio formato di DATAPASSAGGIO da str a Datetime
@st.cache_data
def CambiaFormatoData(_table):
    return _table.with_columns(
        pl.col("DATAPASSAGGIO").str.strptime(pl.Datetime, "%d-%m-%Y %H:%M:%S")
    )

# funzione che ritorna una lista contenente le modalità di una data variabile (colonna)
def lista_modalità(table,variabile):
    return table.select(variabile).unique().sort(variabile)

#sidebar con info utili
def sidebar(table):
    n=len(table)

    st.sidebar.header("Informazioni sul Dataset")
    st.sidebar.markdown(f"""
    - **Totale passaggi:** {n}
    """)

    data_min = table["DATAPASSAGGIO"].min().strftime("%d-%m-%Y")
    data_max = table["DATAPASSAGGIO"].max().strftime("%d-%m-%Y")

    # Mostra intervallo di date
    if data_min == data_max:
        st.sidebar.markdown(f"- **Data disponibile:** {data_min}")
    else:
        st.sidebar.markdown(f"- **Date disponibili:** {data_min} - {data_max}")
