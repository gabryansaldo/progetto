import polars as pl
import streamlit as st
import altair as alt
import utils

# scelgo se vedere totale o solo delle cose selezionate
def selezione_pass(table):
    st.title("🕓 Analisi dei Passaggi Orari")
    st.markdown("""
        Questa dashboard permette di analizzare i passaggi per ora, totali o filtrati per valli e impianti.  
        È possibile decidere se visulizzare un giorno o il totale
    """)

    table=utils.filter_day(table)

    st.markdown("""
        Scegli tra le opzioni disponibili per esplorare i dati.
    """)

    show_totals = st.checkbox(f"Mostra totali per ora")
    if show_totals:
        hourly_pass_T(table.select(["DATAPASSAGGIO"]))

    opzioni_map = utils.get_opzioni_map()
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
    result = utils.group_by_hour(table,"ora").sort("ora")
    if not result.is_empty():
        col1,col2=st.columns([0.2,0.8])
        col1.write(result)

        chart = (
            alt.Chart(result)
            .mark_line()
            .encode(
                alt.X("ora").scale(zero=False),
                alt.Y("PASSAGGI"),
            )
        )
        col2.altair_chart(chart, use_container_width=True)

#divido per orario e valle/impianto
def hourly_pass_vi(table,opzioni_map):
    st.subheader("Raggruppa per Valle o Impianto")
    st.markdown("""
    - **Valle**: Visualizza il numero di passaggi per ciascuna valle.  
    - **Impianto**: Mostra il numero di passaggi per ogni impianto.  
    """)
    c_aka = st.segmented_control("Seleziona:",
        options=list(opzioni_map.keys()),
        default=list(opzioni_map.keys())[0],
        help=f"Scegli raggruppamento da eseguire tra i seguenti"
    )
    if c_aka == None:
        c_aka=list(opzioni_map.keys())[0]
    c = opzioni_map[c_aka]

    lista_mod = utils.lista_modalita(table,c)
    
    form1 = st.form(key="vi_filter")
    mod_selezionate = form1.multiselect(
        f"Inserisci {c_aka.lower()} di interesse",
        lista_mod,
        help=f"Seleziona una o più opzioni per restringere l'analisi. Può lasciare vuota la selezione per includere tutti i valori."
    )
    form1.form_submit_button("Submit")

    filtered_table = (
        table.filter(pl.col(c).is_in(mod_selezionate))
        if mod_selezionate
        else table
    )

    if filtered_table.is_empty():
        form1.warning("Nessun dato corrisponde ai filtri selezionati.")
    
    raggr=utils.group_by_hour(filtered_table,["ora", c])
    result = (
        raggr
        .sort(c)
        .pivot(
            values="PASSAGGI",
            index="ora",
            on=c
        )
        .fill_null(0)
        .sort("ora")
    )

    if not result.is_empty():
        st.write(result)

        chart = (
            alt.Chart(raggr)
            .mark_line()
            .encode(
                alt.X("ora").scale(zero=False),
                alt.Y("PASSAGGI"),
                alt.Color(c)
            )
        )
        st.altair_chart(chart, use_container_width=True)

#funzione pagina
def Hourly_Analysis():
    utils.load_dataset()
    selezione_pass(st.session_state.passaggi)