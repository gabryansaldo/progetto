import polars as pl
import streamlit as st
import altair as alt
import utils

#dizionario opzioni scelta
def get_opzioni_map():
    return {
        "Valle": "NOME_VALLEPOSIZIONEIMPIANTO",
        "Impianto": "NOME_IMPIANTO",
    }

# scelgo se vedere totale o solo delle cose selezionate
def selezione_pass(table):
    st.title("🕓 Analisi dei Passaggi Orari")
    st.markdown("""
        Questa dashboard permette di analizzare i passaggi per ora, totali o filtrati per valli e impianti.  
        È possibile decidere se visulizzare un giorno o il totale, la scelta avrà effetto su tutta la pagina.
    """)

    table=utils.filter_day(table)

    st.markdown("""
        Scegli tra le opzioni disponibili per esplorare i dati.
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

# divido per orario
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
        help=f"Si scelga raggruppamento da eseguire tra i seguenti"
    )
    if c_aka == None:
        c_aka=list(opzioni_map.keys())[0]
    c = opzioni_map[c_aka]

    lista_mod = utils.lista_modalita(table,c)
    
    form1 = st.form(key="vi_filter")
    mod_selezionate = form1.multiselect(
        f"Si inserisca {c_aka.lower()} di interesse e successivamente confermare",
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

        if c_aka==list(opzioni_map.keys())[0] and list(opzioni_map)[0]=="Valle":
            heatmap(raggr)

        if len(mod_selezionate)!=0 or c_aka!=list(opzioni_map.keys())[1]:
            chart = (
                alt.Chart(raggr)
                .mark_line()
                .encode(
                    alt.X("ora").scale(zero=False),
                    alt.Y("Passaggi"),
                    alt.Color(c,title=c_aka).scale(scheme="paired")
                )
            )
            contL=st.container(border=True)
            contL.write("#### Grafico a linee")
            contL.write(f"Questo **grafico a linee** mostra l'andamento dei passaggi durante la giornata per ciascuna {c_aka}. L'asse orizzontale rappresenta l'ora, mentre l'asse verticale mostra il numero di passaggi. Le linee colorate indicano le diverse valli, consentendo di confrontare l'affluenza nel corso della giornata.")
            contL.altair_chart(chart, use_container_width=True)


def heatmap(raggr):
    result = (
        raggr
        .pivot(
            values="Passaggi",
            index="ora",
            columns="NOME_VALLEPOSIZIONEIMPIANTO"
        )
        .fill_null(0)
        .sort("ora")
    )

    raggr_ore = (
        result.unpivot(
            index=["ora"],
            variable_name="NOME_VALLEPOSIZIONEIMPIANTO",
            value_name="Passaggi"
        )
    )

    raggr_ore = raggr_ore.with_columns(
        pl.col("Passaggi").sum().over("NOME_VALLEPOSIZIONEIMPIANTO").alias("TotalePassaggi")
    )

    raggr_ore = raggr_ore.with_columns(
        ((pl.col("Passaggi") / pl.col("TotalePassaggi")) * 100).alias("Percentuale")
    )

    chart = (
        alt.Chart(raggr_ore)
        .mark_rect()
        .encode(
            alt.X("ora:O"),#.scale(zero=False),
            alt.Y("NOME_VALLEPOSIZIONEIMPIANTO:O", title="Valle"),
            alt.Color("Percentuale",title="Passaggi %").scale(scheme="inferno"),
            tooltip=[
                alt.Tooltip("Passaggi:Q", title="Passaggi"),
                alt.Tooltip("ora:O", title="Ora"),
                alt.Tooltip("NOME_VALLEPOSIZIONEIMPIANTO:O", title="Valle")
            ],
        )
    )
    contH=st.container(border=True)
    contH.write("#### Heatmap")
    contH.write(f"Questa **heatmap** mostra le ore più affollate per ciascuna valle, calcolate in percentuale rispetto al totale dei passaggi giornalieri (o totali se selezionato all'inizio di questa pagina). Le intensità dei colori rappresentano la densità di passaggi, con toni più chiari indicanti periodi più affollati.")
    contH.write("")
    contH.altair_chart(chart, use_container_width=True)
    contH.write("Dalle osservazioni della heatmap, emerge che in tutte le valli le ore più affollate si concentrano tra le 9:00 e le 11:00. Questo periodo rappresenta le fasce orarie in cui si registra il picco di passaggi, indicando un maggiore afflusso di visitatori durante le prime ore della giornata")
    st.write("")

#funzione pagina
def Hourly_Analysis():
    utils.load_dataset()
    selezione_pass(st.session_state.passaggi)