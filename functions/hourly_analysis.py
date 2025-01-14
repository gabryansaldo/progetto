# hourly_analysis.py
# Questo file gestisce l'analisi oraria dei dati, visualizzando statistiche relative ai passaggi degli skipass su base oraria, con grafici interattivi e confronti tra giorni.


import polars as pl
import streamlit as st
import altair as alt
import utils


# Funzione che restituisce un dizionario con alias più leggibili per 2 colonne del dataset
def get_opzioni_map():
    return {
        "Valle": "NOME_VALLEPOSIZIONEIMPIANTO",
        "Impianto": "NOME_IMPIANTO",
    }

# Funzione che consente di selezionare se visualizzare il totale dei passaggi o solo quelli relativi a specifici impianti e valli. Gestisce la visualizzazione delle statistiche orarie.
def selezione_pass(table):
    st.title("🕓 Analisi dei Passaggi Orari")
    st.markdown("""
        Questa dashboard permette di analizzare i passaggi per ora, totali o filtrati per valli e impianti.  
        È possibile decidere se visulizzare un giorno o il totale, la scelta avrà effetto su tutta la pagina.
    """)

    table=utils.filter_day(table)

    st.markdown("""
        Si scelga tra le opzioni disponibili per esplorare i dati.
    """)
    dett_exp=st.expander(f"Mostra totali per ora")
    with dett_exp:
        hourly_pass_T(table.select(["DATAPASSAGGIO"]))
        
    st.divider()

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

# Funzione che calcola e visualizza il numero di passaggi totali per ogni ora, ordinati per ora. Mostra anche un grafico a linea interattivo.
def hourly_pass_T(table):
    result = utils.group_by_hour(table,"ora").sort("ora")
    if not result.is_empty():
        col1,col2=st.columns([0.25,0.75])
        col1.write(result)

        chart = (
            alt.Chart(result)
            .mark_line()
            .encode(
                alt.X("ora").scale(zero=False),
                alt.Y("Passaggi"),
            )
        )
        col2.altair_chart(chart, use_container_width=True)

# Funzione che raggruppa i passaggi per ora, con opzioni per visualizzare i dati per valle o impianto. Mostra un heatmap e un grafico a linee interattivo.
def hourly_pass_vi(table,opzioni_map):
    st.subheader("Raggruppamento per Valle o Impianto")
    st.markdown("""
    - **Valle**: Visualizzazione del numero di passaggi per ciascuna valle.  
    - **Impianto**: Visualizzazione del numero di passaggi per ogni impianto.  
    """)
    c_aka = st.segmented_control("Seleziona:",
        options=list(opzioni_map.keys()),
        default=list(opzioni_map.keys())[0],
        help=f"Si scelga raggruppamento da eseguire tra i seguenti"
    )
    if c_aka == None:
        c_aka=list(opzioni_map.keys())[0]
    c = opzioni_map[c_aka]

    lista_mod = utils.lista_modalita(table,c)
    
    form1 = st.form(key="vi_filter")
    mod_selezionate = form1.multiselect(
        f"Si inseriscano modalità di interesse e successivamente confermare",
        lista_mod,
        help=f"Si selezioni una o più opzioni per restringere l'analisi, si lasci vuota la selezione per includere tutti i valori."
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
            values="Passaggi",
            index="ora",
            on=c
        )
        .fill_null(0)
        .sort("ora")
    )


    if not result.is_empty():
        dett_exp=st.expander(f"Visualizza numero di passaggi dettagliati")
        with dett_exp:
            dett_exp.dataframe(result,use_container_width=True)

        st.divider()

        if len(mod_selezionate)!=0 or c_aka!=list(opzioni_map.keys())[1]:
            st.header("Grafici")
            #if c_aka==list(opzioni_map.keys())[0] and list(opzioni_map)[0]=="Valle":
            heatmap(raggr,c_aka)
            line_graph(raggr,c,c_aka)        
        else:
            st.info("Si selezionino degli impianti per visualizzare i grafici")

# Funzione che crea un grafico a linee interattivo per visualizzare il numero di passaggi orari per valle o impianto.
def line_graph(raggr,c,c_aka):
    highlight = alt.selection_point(fields=[c], bind="legend")
    #highlight = alt.selection_point(fields=[c], on="click", empty="none", name="Highlight")
    #selection = alt.selection_point(fields=[c], bind="legend")
    chart = (
        alt.Chart(raggr)
        .mark_line()
        .encode(
            alt.X("ora").scale(zero=False),
            alt.Y("Passaggi"),
            alt.Color(c,title=c_aka).scale(scheme="rainbow"),
            opacity=alt.condition(highlight, alt.value(1), alt.value(0.2)),
        )
        #.add_params(selection)
        .add_params(highlight)

    )
    contL=st.container(border=True)
    contL.write(f"#### Andamento dei Passaggi Giornalieri per {c_aka}")
    contL.write(f"Questo **grafico a linee** mostra l'andamento dei passaggi durante la giornata per ciascuna {c_aka}. L'asse orizzontale rappresenta l'ora, mentre l'asse verticale mostra il numero di passaggi. Le linee colorate indicano le diverse {c_aka}, consentendo di confrontare l'affluenza nel corso della giornata, si selezioni una {c_aka} dalla legenda per una visualizzazione più chiara.")
    contL.altair_chart(chart, use_container_width=True)

# Funzione che crea un heatmap per visualizzare la distribuzione percentuale dei passaggi orari tra diverse valli o impianti.
def heatmap(raggr,str):
    var=get_opzioni_map()[str]
    result = (
        raggr
        .pivot(
            values="Passaggi",
            index="ora",
            columns=var
        )
        .fill_null(0)
        .sort("ora")
    )

    raggr_ore = (
        result.unpivot(
            index=["ora"],
            variable_name=var,
            value_name="Passaggi"
        )
    )

    raggr_ore = raggr_ore.with_columns(
        pl.col("Passaggi").sum().over(var).alias("TotalePassaggi")
    )

    raggr_ore = raggr_ore.with_columns(
        ((pl.col("Passaggi") / pl.col("TotalePassaggi")) * 100).alias("Percentuale")
    )

    chart = (
        alt.Chart(raggr_ore)
        .mark_rect()
        .encode(
            alt.X("ora:O"),
            alt.Y(var + ":O", title=str),
            alt.Color("Percentuale",title="Passaggi %").scale(scheme="inferno"),
            tooltip=[
                alt.Tooltip("Passaggi:Q", title="Passaggi"),
                alt.Tooltip("ora:O", title="Ora"),
                alt.Tooltip(var + ":O", title=str)
            ],
        )
    )
    contH=st.container(border=True)
    contH.write("#### Orari più affollati")
    contH.write(f"Questa **heatmap** mostra le ore più affollate per ciascuna {str}, calcolate in percentuale rispetto al totale dei passaggi giornalieri della {str} (o totali se selezionato all'inizio di questa pagina). Le intensità dei colori rappresentano la densità di passaggi, con toni più chiari indicanti periodi più affollati.")
    contH.write("")
    contH.altair_chart(chart, use_container_width=True)
    if str=="Valle":
        contH.write("Dalle osservazioni della heatmap, emerge che in tutte le valli le ore più affollate si concentrano tra le 9:00 e le 11:00. Questo periodo rappresenta le fasce orarie in cui si registra il picco di passaggi, indicando un maggiore afflusso di visitatori durante le prime ore della giornata")
    st.write("")

# Funzione principale della pagina, che carica i dati e avvia l'analisi dei passaggi orari.
def Hourly_Analysis():
    utils.load_dataset()
    selezione_pass(st.session_state.passaggi)