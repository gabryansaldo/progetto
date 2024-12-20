import polars as pl
import streamlit as st
import base64
import pandas as pd
import altair as alt
from pathlib import Path


#se il dataset non è ancora caricato richiama read_dataset
def load_dataset():
    if "passaggi" not in st.session_state:
        st.session_state.passaggi = read_dataset("DatiPassaggi.csv.gz")
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
        pl.col("DATAPASSAGGIO").str.strptime(pl.Datetime)
    )

# funzione che ritorna una lista contenente le modalità di una data variabile (colonna)
def lista_modalita(table,variabile):
    if variabile not in table.columns:
        st.warning(f"La colonna '{variabile}' non esiste nel dataset.")
        return []
    return table.select(variabile).unique().sort(variabile).to_series().to_list()

# definisci stile per "scatole" nella sidebar
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

#sidebar con info utili
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

#raggruppa per skipass
def group_by_skipass(table):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.strftime("%Y-%m-%d").alias("Data"))
        .group_by(["Data", "CODICEBIGLIETTO","NOME_TIPOPERSONA","NOME_TIPOBIGLIETTO"])
        .agg([pl.count("CODICEBIGLIETTO").alias("passaggi")])
        .sort(["passaggi"], descending=[True])   
    )

#persone per ciascun giorno
def units_per_day(table):
    groupskipass=group_by_skipass(table)
    return groupskipass.group_by("Data").agg(pl.count("CODICEBIGLIETTO").alias("persone"))

#passaggi per ciascun giorno
def pass_per_day(table):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.strftime("%Y-%m-%d").alias("Data"))
        .group_by("Data").agg(pl.count("CODICEBIGLIETTO").alias("passaggi"))
        .sort("Data")
    )

#tiene solo ora e poi raggruppa per le colonne passate
def group_by_hour(table, groupby):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.hour().alias("ora"))
        .group_by(groupby).agg(pl.len().alias("Passaggi"))
    )

#conta numero modalità diverse di una variabile
def conta_mod(table,var):
    return len(lista_modalita(table,var))

#conta skipass per modalità (es. tipo skipass) di una variabile data
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
    
#cambio formato immagine
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

#tabella solo nome impianto e valle
def minimal_table(table):
    tab = table.sort("DATAPASSAGGIO"
    ).with_columns(pl.Series("index", range(1,len(table)+1))
    ).select(["index","NOME_IMPIANTO","NOME_VALLEPOSIZIONEIMPIANTO","DATAPASSAGGIO"])
    return change_columns_title(tab)

#divido colonna 
def tab_day_hour(table):
    return (
        table
        .with_columns(pl.col("DATAPASSAGGIO").dt.strftime("%Y-%m-%d").alias("Data"))
        .sort("DATAPASSAGGIO")
    )

#metti sfondo con url
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

#chiedi giorno e filtra tabella per giorno o totale
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

# grafico tipo persone
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
            alt.Color(raggr+":N",title=f"{alias}").scale(scheme="rainbow")
        )
    )

    text_pie = (
        alt.Chart(tab)
        .mark_text(radius=140, size=15)
        .encode(
            alt.Text("numero:Q"),
            alt.Theta("numero:Q").stack(True),
            alt.Order(raggr+":N"),
            alt.Color(raggr+":N")
        )
    )
    
    total_text = (
        alt.Chart(tab)
        .mark_text(radius=0, size=30)
        .encode(
            alt.Text("sum(numero):Q"),
            color=alt.value("red")
        )
    )

    return base_pie + text_pie + total_text

# raggruppa giorni da 7 in poi
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

    table = table.group_by("NOME_TIPOBIGLIETTO_RAGGR").agg(
        pl.sum("numero")
    )
    return table.rename({"NOME_TIPOBIGLIETTO_RAGGR": "NOME_TIPOBIGLIETTO"})
    
# tabella tipo persone grafico tipo persone
def chart_tipo(table,raggr):
    table=conta_tipo(table,raggr)
    if raggr == "NOME_TIPOBIGLIETTO":
        table=raggr_7GG(table)
    return pies_chart(table,raggr)

# grafico per podio passaggi
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

# dizionario con alias delle colonne
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

# cambia il nome delle colonne della tabella passata in quello definito nella funzione create_col_map
def change_columns_title(table):
    map=create_col_map()
    columns = {}
    for k, v in map.items():
        if k in table.columns:
            columns[k] = v
    return table.rename(columns)
