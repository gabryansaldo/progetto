import polars as pl
import streamlit as st
import time

#se il dataset non è ancora caricato richiama read_dataset
def load_dataset():
    if "passaggi" not in st.session_state:
        st.session_state.passaggi = read_dataset("Passaggi.csv")
    if st.session_state.passaggi.is_empty():
        st.error("Errore nel caricamento del dataset.")
        return False
    return True

#importo il dataset
@st.cache_data
def read_dataset(url):
    try:
        passaggi = pl.read_csv(url, separator=",")
        st.session_state.passaggi = CambiaFormatoData(passaggi)
    except Exception as e:
        st.error(f"Errore durante il caricamento del dataset: {e}")
        return pl.DataFrame()
    return st.session_state.passaggi

#cambio formato di DATAPASSAGGIO da str a Datetime
def CambiaFormatoData(table):
    return table.with_columns(
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

    data_min = table["DATAPASSAGGIO"].min().strftime("%d-%m-%Y")
    data_max = table["DATAPASSAGGIO"].max().strftime("%d-%m-%Y")

    if data_min == data_max:
        st.sidebar.write(f"- **Data disponibile:** {data_min}")
    else:
        st.sidebar.write(f"- **Date disponibili:** {data_min} - {data_max}")
    
    st.sidebar.write(f"""
    - **Totale passaggi:** {n}
    """)

    commento()

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
        .with_columns(pl.col("DATAPASSAGGIO").dt.date().alias("data"))
        .group_by(["data", "CODICEBIGLIETTO", "NOME_TIPOPERSONA"])
        .agg(pl.count("DATAPASSAGGIO").alias("passaggi"))
        .sort(["data", "passaggi"], descending=[False, True])
    )

#persone per ciascun giorno
def units_per_day(table):
    groupskipass=group_by_skipass(table)
    return groupskipass.group_by("data").agg(pl.count("CODICEBIGLIETTO").alias("persone"))

#tiene solo ora e poi raggruppa per le colonne passate
def group_by_hour(table, groupby):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.hour().alias("ora"))
        .group_by(groupby).agg(pl.len().alias("PASSAGGI"))
    )

#conta numero modalità diverse di una variabile
def conta_mod(table,var):
    return len(lista_modalita(table,var))

#conta skipass per modalità di una variabile data
def conta_tipo(table,var):
    tab_pers=group_by_skipass(table)
    return tab_pers.group_by(var).agg(pl.count(var).alias("numero")).sort("numero")

#tabella più facile da vedere
def fancy_table(table):
    columns_to_select = [col for col in table.columns if "ID_" not in col.upper()]
    return table.select(columns_to_select)

#commento sull'applicazione
def commento():
    with st.sidebar.popover("Lascia un commento"):
        st.write("funzione al momento disattivata")
        # user_input = st.text_area(f"Lascia una recensione")
        # user_stars = st.feedback("stars")
        # if st.button(f"Salva"):
        #     if user_input.strip():
        #         with open("others\commenti.txt", "a") as file:
        #             file.write("Commento: " + user_input + "\n" + str(user_stars+1) + "\n\n")
        #         st.success("Il tuo commento è stato salvato con successo!")
        #     else:
        #         st.warning("Il campo è vuoto. Per favore, inserisci del testo.")

#scrivi il testo lentamente
def stream_data(string):
    for word in string.split(" "):
        yield word + " "
        time.sleep(0.1)
    



