import polars as pl
import streamlit as st
import icecream as ic

# cambio formato di DATAPASSAGGIO da str a Datetime
@st.cache_data
def CambiaFormatoData(_table):
    return _table.with_columns(
        pl.col("DATAPASSAGGIO").str.strptime(pl.Datetime, "%d-%m-%Y %H:%M:%S")
    )

# funzione che ritorna una lista contenente le modalità di una data variabile (colonna)
def lista_modalità(table,variabile):
    return table.select(variabile).unique().sort(variabile)

# scelgo se vedere totale o solo delle cose selezionate
def selezione_pass(table):
    st.title("Analisi dei Passaggi Orari")
    st.markdown("""
        Questa dashboard consente di:
        - Analizzare il numero di passaggi per ora su base totale o filtrando per valli e impianti specifici.
        - Visualizzare i dati aggregati in modo semplice e interattivo.

        Utilizza le opzioni disponibili per esplorare i dati e ottenere insights utili.
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
        table = table.select(["DATAPASSAGGIO"])
        return hourly_pass_T(table)
    else:
        opzioni_map = {
            "Valle": "NOME_VALLEPOSIZIONEIMPIANTO",
            "Impianto": "NOME_IMPIANTO"
        }
        lista_colonne_utili = ["DATAPASSAGGIO"]

        for key in opzioni_map:
            lista_colonne_utili.append(opzioni_map[key])

        table = table.select(lista_colonne_utili)
        return hourly_pass_vi(table,opzioni_map)

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
    #c_aka=list(opzioni_map.keys())[0]
    c_aka = st.segmented_control(
        "Raggruppamento:",
        options=list(opzioni_map.keys()),
        default=list(opzioni_map.keys())[0],
        help=f"Scegli raggruppamento da eseguire tra i seguenti"
    )
    c = opzioni_map[c_aka]

    lista_mod = lista_modalità(table,c)

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

#main
def main():
    # carico il dataset
    url = "../progetto/Gabry.csv"
    passaggi = CambiaFormatoData(pl.read_csv(url,separator=","))

    selezione_pass(passaggi)
    sidebar(passaggi)

if __name__ == "__main__":
    main()

# IDEE
#
# specificare che il dataset si riferisce ad un giorno solo ed eseguire una verica a schermo
# in hourly_pass_vi migliorare la selezione tra valle e impianto
# grafico per ora e minuti per impianto... (forse non ha senso)

# st.feedback("stars")