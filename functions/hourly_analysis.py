import polars as pl
import streamlit as st
from utils import lista_modalita
from utils import load_dataset
from utils import get_opzioni_map

# scelgo se vedere totale o solo delle cose selezionate
def selezione_pass(table):
    st.title("Analisi dei Passaggi Orari")
    st.markdown("""
        Questa dashboard permette di analizzare i passaggi per ora, totali o filtrati per valli e impianti.  
        Scegli tra le opzioni disponibili per esplorare i dati.
    """)
    
    st.subheader("Seleziona Modalità di Analisi")
    st.markdown("""
    Scegli se visualizzare il numero totale dei passaggi per ora o filtrare i dati 
    in base alle valli o agli impianti di interesse.  
    - **Mostra totali per ora**: Mostra un'aggregazione complessiva.  
    - **Filtra per valle o impianto**: Permette di analizzare dati specifici.
    """)
    
    show_totals = st.checkbox(f"Mostra totali per ora")
    if show_totals:
        hourly_pass_T(table.select(["DATAPASSAGGIO"]))

    opzioni_map = get_opzioni_map()
    lista_colonne_utili = ["DATAPASSAGGIO"]

    for key in opzioni_map:
        lista_colonne_utili.append(opzioni_map[key])
    
    missing_columns = [col for col in lista_colonne_utili if col not in table.columns]
    if missing_columns:
        st.error(f"Mancano le seguenti colonne nel dataset: {', '.join(missing_columns)}")
        return False

    table = table.select(lista_colonne_utili)
    hourly_pass_vi(table,opzioni_map)

# divido per orario
def hourly_pass_T(table):
    result = table.with_columns(pl.col("DATAPASSAGGIO").dt.hour().alias("ora")
        ).group_by("ora").agg(pl.len().alias("PASSAGGI")
        ).sort("ora")
    if not result.is_empty():
        st.write(result)

#divido per orario e valle/impianto
def hourly_pass_vi(table,opzioni_map):
    st.subheader("Raggruppa per Valle o Impianto")
    st.markdown("""
    Decidi come raggruppare i dati:
    - **Valle**: Visualizza il numero di passaggi per ciascuna valle.  
    - **Impianto**: Mostra il numero di passaggi per ogni impianto.  
    """)
    c_aka = st.segmented_control(
        "Raggruppamento:",
        options=list(opzioni_map.keys()),
        default=list(opzioni_map.keys())[0],
        help=f"Scegli raggruppamento da eseguire tra i seguenti"
    )
    c = opzioni_map[c_aka]

    lista_mod = lista_modalita(table,c)

    st.subheader("Filtra i Dati")
    st.markdown(f"""
    Seleziona una o più valli o impianti per restringere l'analisi ai soli dati di tuo interesse.  
    Puoi lasciare vuota la selezione per includere tutti i valori.
    """)
    
    mod_selezionate = st.multiselect(
        f"Inserisci {c_aka.lower()} di interesse",
        lista_mod,
        help="Seleziona uno o più valori per filtrare i dati"
    )

    filtered_table = (
        table.filter(pl.col(c).is_in(mod_selezionate))
        if mod_selezionate
        else table
    )

    if filtered_table.is_empty():
        st.warning("Nessun dato corrisponde ai filtri selezionati.")
    
    result = (
        filtered_table
        .with_columns(pl.col("DATAPASSAGGIO").dt.hour().alias("ora"))
        .group_by(["ora", c])  # Raggruppa per ora e valle/impianto
        .agg(pl.len().alias("PASSAGGI"))  # Conta i passaggi
        .sort(c)
        .pivot(
            values="PASSAGGI",  # I valori da mostrare nelle celle
            index="ora",  # Righe
            on=c  # Colonne
        )
        .fill_null(0)  # Riempi i valori nulli con 0
        .sort("ora")
    )

    if not result.is_empty():
        st.write(result)

#funzione pagina
def Hourly_Analysis():
    load_dataset()
    selezione_pass(st.session_state.passaggi)