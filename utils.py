# utils.py
# Contiene funzioni di supporto utilizzate in altre parti dell'applicazione
# per gestire dati, creare grafici e semplificare operazioni come la modifica 
# dei nomi delle colonne e l'applicazione di filtri.


import polars as pl
import streamlit as st
import base64
import pandas as pd
import altair as alt
from pathlib import Path


# Carica il dataset nella sessione se non è già presente e verifica che non sia vuoto
def load_dataset():
    if "passaggi" not in st.session_state:
        st.session_state.passaggi = read_dataset("DatiPassaggi.csv.gz")
    if st.session_state.passaggi.is_empty():
        st.error("Errore nel caricamento del dataset.")
        return False
    return True

# Importa il dataset da un URL, lo processa e lo salva
@st.cache_data
def read_dataset(url):
    try:
        passaggi = pl.read_csv(url, separator=",")
        st.session_state.passaggi = fancy_table(CambiaFormatoData(passaggi))
    except Exception as e:
        st.error(f"Errore durante il caricamento del dataset: {e}")
        return pl.DataFrame()
    return st.session_state.passaggi

# Cambio formato di DATAPASSAGGIO da str a Datetime
def CambiaFormatoData(table):
    return table.with_columns(
        pl.col("DATAPASSAGGIO").str.strptime(pl.Datetime)
    )

# Ritorna una lista con le modalità uniche ordinate di una colonna specifica del dataset
def lista_modalita(table,variabile):
    if variabile not in table.columns:
        st.warning(f"La colonna '{variabile}' non esiste nel dataset.")
        return []
    return table.select(variabile).unique().sort(variabile).to_series().to_list()

# Definizione stile per "scatole" nella sidebar
def sidebar_box_style(text, value, background_color="rgba(213,228,224,255)", text_color="#2C3E50", value_color="rgb(42, 31, 165)"):
    return f"""
    <div style="
        font-size: 18px; 
        font-weight: bold; 
        color: {text_color}; 
        text-align: center; 
        border-radius: 10px; 
        background-color: {background_color};">
        {text}
        <p style="
        color: {value_color};
        font-size: 18px; 
        font-weight: bold;">
        {value}
        </p>
    </div>
    """

# Crea una sidebar con informazioni utili sul dataset, come date e conteggi
def sidebar(table):
    if table.is_empty():
        st.sidebar.warning("Nessun dato disponibile nel dataset.")
        return
    npass=len(table)
    npers=len(lista_modalita(table,"CODICEBIGLIETTO"))

    st.sidebar.header("Informazioni sul Dataset")

    data_min = table["DATAPASSAGGIO"].min().strftime("%d/%m/%Y")
    data_min
    data_max = table["DATAPASSAGGIO"].max().strftime("%d/%m/%Y")

    if data_min == data_max:
        st.sidebar.markdown(sidebar_box_style("Data disponibili:", data_min), unsafe_allow_html=True)

    else:
        st.sidebar.markdown(sidebar_box_style("Date disponibili:", f"{data_min} - {data_max}"), unsafe_allow_html=True)
    
    st.sidebar.markdown(sidebar_box_style("Totale Persone:", f"{npers:,}", value_color="#16A085"), unsafe_allow_html=True)

    st.sidebar.markdown(sidebar_box_style("Totale Passaggi:", f"{npass:,}", value_color="#16A085"), unsafe_allow_html=True)

    #commento()

# Raggruppa il dataset per skipass e calcola il numero di passaggi per ogni combinazione di attributi
def group_by_skipass(table):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.strftime("%Y-%m-%d").alias("Data"))
        .group_by(["Data", "CODICEBIGLIETTO","NOME_TIPOPERSONA","NOME_TIPOBIGLIETTO"])
        .agg([pl.count("CODICEBIGLIETTO").alias("passaggi")])
        .sort(["passaggi"], descending=[True])   
    )

# Raggruppa il dataset per skipass senza considerare la data e calcola il totale dei passaggi
def group_skipass_wo_date(table):
    tab=group_by_skipass(table)
    return (
        tab
        .group_by(["CODICEBIGLIETTO", "NOME_TIPOPERSONA", "NOME_TIPOBIGLIETTO"])
        .agg([
            pl.sum("passaggi").alias("total_passaggi"),
        ])
    )

# Calcola il numero di persone per ciascun giorno
def units_per_day(table):
    groupskipass=group_by_skipass(table)
    return groupskipass.group_by("Data").agg(pl.count("CODICEBIGLIETTO").alias("persone"))

# Calcola il numero di passaggi per ciascun giorno
def pass_per_day(table):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.strftime("%Y-%m-%d").alias("Data"))
        .group_by("Data").agg(pl.count("CODICEBIGLIETTO").alias("passaggi"))
        .sort("Data")
    )

# Estrae l'ora da una colonna e raggruppa per le colonne specificate, calcolando il numero di passaggi
def group_by_hour(table, groupby):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.hour().alias("ora"))
        .group_by(groupby).agg(pl.len().alias("Passaggi"))
    )

# Conta il numero di modalità uniche di una variabile (colonna) nel dataset
def conta_mod(table,var):
    return len(lista_modalita(table,var))

# Conta il numero di skipass per ciascuna modalità di una variabile (o lista di variabili) specificata
def conta_tipo(table, var):
    tab_pers = group_skipass_wo_date(table)
    
    if isinstance(var, str):
        var = [var]
    
    return (
        tab_pers
        .group_by(var)
        .agg(pl.count(var[0]).alias("numero"))
        .sort("numero")
    )

# Ritorna la tabella senza le colonne ID, utilizzata in read_dataset per il preprocessing
def fancy_table(table):
    columns_to_select = [col for col in table.columns if "ID_" not in col.upper()]
    return table.select(columns_to_select)

# Permette agli utenti di lasciare un commento e una valutazione tramite la sidebar
## Funzione inutilizzata
def commento():
    with st.sidebar.popover("Lascia un commento"):
        # st.write("funzione al momento disattivata")
        user_input = st.text_area(f"Lascia una recensione")
        user_stars = st.feedback("stars")
        if st.button(f"Salva"):
            if user_input.strip():
                file_path = Path("others") / "commenti.txt"
                with open(file_path, "a") as file:
                    file.write("Commento: " + user_input + "\n" + str(user_stars+1) + "\n\n")
                st.success("Il tuo commento è stato salvato con successo!")
            else:
                st.warning("Il campo è vuoto. Per favore, inserisci del testo.")
    
# Converte un'immagine in formato base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Crea una tabella con solo il nome dell'impianto e della valle, aggiungendo un indice
def minimal_table(table):
    tab = table.sort("DATAPASSAGGIO"
    ).with_columns(pl.Series("index", range(1,len(table)+1))
    ).select(["index","NOME_IMPIANTO","NOME_VALLEPOSIZIONEIMPIANTO","DATAPASSAGGIO"])
    return change_columns_title(tab)

# Crea la colonna data (anno-mese-giorno) da "DATAPASSAGGIO"
def tab_day_hour(table):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.strftime("%Y-%m-%d").alias("Data"))
        .sort("DATAPASSAGGIO")
    )

# Imposta uno sfondo personalizzato per l'app utilizzando un'immagine da URL
def background(url):
    bg_image = get_base64(url)

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

# Chiede all'utente di selezionare un giorno e filtra la tabella in base alla selezione o restituisce il totale
def filter_day(table):
    tab=tab_day_hour(table)
    day_list=lista_modalita(tab,"Data")
    day_list.insert(0,"Totale")
    col1,col2=st.columns([0.25,0.75])
    selected_day=col1.selectbox("Selezionare:  ",options=day_list)
    if selected_day=="Totale": 
        return tab
    else:
        return tab.filter(pl.col("Data")==selected_day)

# Crea un grafico a torta per visualizzare la distribuzione delle persone in base a una variabile
def pies_chart(tab,raggr):
    alias=create_col_map()[raggr]

    base_pie = (
        alt.Chart(tab)
        .mark_arc(
            cornerRadius=8,
            radius=120,
            radius2=80
        )
        .encode(
            alt.Theta("numero:Q"),
            alt.Color(raggr+":N",title=f"{alias}").scale(scheme="rainbow"),
            tooltip=[alt.Tooltip(raggr,title=f"{alias}"),alt.Tooltip("numero",title="numero", format=",.0f"),]
        )
    )

    text_pie = (
        alt.Chart(tab)
        .mark_text(radius=145, size=15)
        .encode(
            alt.Text("numero:Q", format=",.0f"),
            alt.Theta("numero:Q").stack(True),
            alt.Order(raggr+":N"),
            alt.Color(raggr+":N")
        )
    )
    
    total_text = (
        alt.Chart(tab)
        .mark_text(radius=0, size=30)
        .encode(
            alt.Text("sum(numero):Q", format=",.0f"),
            color=alt.value("red")
        )
    )

    return base_pie + text_pie + total_text

# Crea un grafico a torta interattivo per visualizzare la distribuzione delle persone per tipo di biglietto, con un grafico a barre interattivo
def pies_chart_interactive(tab):
    alias=create_col_map()["NOME_TIPOBIGLIETTO"]

    selection = alt.selection_point(fields=["NOME_TIPOBIGLIETTO"], bind="scales")
    table=tab.group_by("NOME_TIPOBIGLIETTO").agg(pl.sum("numero"))

    base_pie = (
        alt.Chart(table)
        .mark_arc(
            cornerRadius=8,
            radius=120,
            radius2=80
        )
        .encode(
            alt.Theta("numero:Q"),
            alt.Color("NOME_TIPOBIGLIETTO"+":N",title=f"{alias}").scale(scheme="rainbow"),
            tooltip=[alt.Tooltip("NOME_TIPOBIGLIETTO",title=f"{alias}"),alt.Tooltip("numero",title="Persone", format=",.0f"),],
            opacity=alt.condition(selection, alt.value(1), alt.value(0.4)),
        )
        .add_params(selection)
    )

    text_pie = (
        alt.Chart(table)
        .mark_text(radius=145, size=15)
        .encode(
            alt.Text("numero:Q", format=",.0f"),
            alt.Theta("numero:Q").stack(True),
            alt.Order("NOME_TIPOBIGLIETTO"+":N"),
            alt.Color("NOME_TIPOBIGLIETTO"+":N"),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.4)),
        )
    )
    
    total_text = (
        alt.Chart(table)
        .mark_text(radius=0, size=30)
        .encode(
            alt.Text("sum(numero):Q", format=",.0f"),
            color=alt.value("gray")
        )
    )
    

    bar_chart = (
        alt.Chart(tab)
        .mark_bar()
        .encode(
            alt.X("NOME_TIPOPERSONA" + ":N", title=None),
            alt.Y("numero",title=None),
            alt.Color("NOME_TIPOBIGLIETTO"+":N"),
            tooltip=alt.value(None),
        )
        .transform_filter(selection)
        .properties(
            width=120,
            height=300 )
    )

    return base_pie + text_pie + total_text | bar_chart

# Raggruppa i giorni superiori o uguali a 7 nella colonna "NOME_TIPOBIGLIETTO" e aggrega per tipo di biglietto e persona
def raggr_7GG(table):
    table = table.with_columns(
        pl.when(
            pl.col("NOME_TIPOBIGLIETTO")
            .str.extract(r"^(\d+)", 1)
            .cast(pl.Int64)
            .is_not_null()
            & (pl.col("NOME_TIPOBIGLIETTO")
            .str.extract(r"^(\d+)", 1)
            .cast(pl.Int64) >= 7)
        ).then(pl.lit("7+ Giorni"))
        .otherwise(pl.col("NOME_TIPOBIGLIETTO"))
        .alias("NOME_TIPOBIGLIETTO_RAGGR")
    )

    table = table.group_by(["NOME_TIPOBIGLIETTO_RAGGR", "NOME_TIPOPERSONA"]).agg(
        pl.sum("numero")#.alias("totale_numero")
    )

    return table.rename({"NOME_TIPOBIGLIETTO_RAGGR": "NOME_TIPOBIGLIETTO"})
    
# Fornisce un grafico a torta e a barre interattivo per visualizzare la distribuzione dei tipi di persone e biglietti
def chart_tipo_interatt(table):
    raggr=["NOME_TIPOPERSONA","NOME_TIPOBIGLIETTO"]
    table=raggr_7GG(conta_tipo(table,raggr))
    return pies_chart_interactive(table)

# Fornisce un grafico a torta per visualizzare la distribuzione di una variabile specificata
def chart_tipo(table,raggr):
    table=conta_tipo(table,raggr)
    return pies_chart(table,raggr)

# Crea un grafico a barre che raffiugura un podio e informazioni aggiuntive per i top 3 in base ai passaggi
def podio(tab):
    podio = {
    "altezza": [3,2,1],
    "emoji": ["🥇","🥈","🥉"],
    "posizione":[2,1,3],
    "colore": ["#ffb900", "#cccccc", "#f7894a"]}

    podio = pd.DataFrame(podio)
    top3=pd.DataFrame(tab[:3])
    top3["posizione"]=[2,1,3]

    podio=top3.merge(podio,on="posizione")
    podio=pl.DataFrame(podio)

    podium_chart = (
        alt.Chart(podio)
        .mark_bar(size=115)
        .encode(
            alt.X("posizione:O", title="",axis=alt.Axis(labels=False)),
            alt.Y("altezza:Q", title="",axis=alt.Axis(labels=False, grid=False)),
            alt.Color("colore:N",scale=None),
            tooltip=alt.value(None)
        )
        .properties(
            #width=400,
            height=250 
        )
    )   
    
    pass_chart = (
        alt.Chart(podio)
        .mark_text(fontSize=24,baseline="bottom", dy=0)
        .encode(
            alt.X("posizione:O"),
            alt.Y("altezza:Q"),
            alt.Text("4:N"),
            color=alt.value("gray"),
            tooltip=alt.value(None)

        )
    )

    emoji_chart = (
        alt.Chart(podio)
        .mark_text(fontSize=24,baseline="top", dy=15)
        .encode(
            alt.X("posizione:O"),
            alt.Y("altezza:Q"),
            alt.Text("emoji:N"),
            tooltip=alt.value(None)
        )
    )

    skipass_chart = (
        alt.Chart(podio)
        .mark_text(fontSize=16,baseline="top", dy=45)
        .encode(
            alt.X("posizione:O"),
            alt.Y("altezza:Q"),
            alt.Text("1:N"),
            tooltip=alt.value(None)
        )
    )

    return podium_chart + pass_chart + emoji_chart + skipass_chart

# Crea un dizionario con alias più leggibili per le colonne del dataset
def create_col_map():
    return {
        "CODICEBIGLIETTO": "Codice biglietto",
        "ID_CASSA": "ID cassa",
        "NOME_CASSA": "Cassa",
        "ID_VALLEPOSIZIONECASSA": "ID valle cassa",
        "NOME_VALLEPOSIZIONECASSA": "Valle cassa",
        "DATAPASSAGGIO": "Data passaggio",
        "ID_IMPIANTO": "ID impianto",
        "NOME_IMPIANTO": "Impianto",
        "ID_VALLEPOSIZIONEIMPIANTO": "ID valle impianto",
        "NOME_VALLEPOSIZIONEIMPIANTO": "Valle",
        "ID_VALLEVALIDITABIGLIETTO": "ID valle validità biglietto",
        "NOME_VALLEVALIDITABIGLIETTO": "Valle validità biglietto",
        "ID_TIPOBIGLIETTO": "ID tipo biglietto",
        "NOME_TIPOBIGLIETTO": "Tipo biglietto",
        "ID_TIPOPERSONA": "ID tipo persona",
        "NOME_TIPOPERSONA": "Tipo persona"
    }

# Cambia i nomi delle colonne della tabella in base agli alias definiti nella funzione create_col_map
def change_columns_title(table):
    map=create_col_map()
    columns = {}
    for k, v in map.items():
        if k in table.columns:
            columns[k] = v
    return table.rename(columns)
