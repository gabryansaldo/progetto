import polars as pl
import streamlit as st
import time
import base64
import pandas as pd
import altair as alt

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

#dizionario opzioni scelta
def get_opzioni_map():
    return {
        "Valle": "NOME_VALLEPOSIZIONEIMPIANTO",
        "Impianto": "NOME_IMPIANTO",
    }

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
        .group_by(groupby).agg(pl.len().alias("PASSAGGI"))
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
                with open("others\commenti.txt", "a") as file:
                    file.write("Commento: " + user_input + "\n" + str(user_stars+1) + "\n\n")
                st.success("Il tuo commento è stato salvato con successo!")
            else:
                st.warning("Il campo è vuoto. Per favore, inserisci del testo.")

#scrivi il testo lentamente
def stream_data(string):
    for word in string.split(" "):
        yield word + " "
        time.sleep(0.1)
    
#cambio formato immagine
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

#tabella solo nome impianto e valle
def minimal_table(table):
    return table.with_columns(pl.col("NOME_IMPIANTO").alias("Nome Impianto")
    ).with_columns(pl.col("NOME_VALLEPOSIZIONEIMPIANTO").alias("Valle")
    ).with_columns(pl.col("DATAPASSAGGIO").alias("Data e Ora")
    ).sort("Data e Ora"
    ).with_columns(pl.Series("index", range(1,len(table)+1))
    ).select(["index","Nome Impianto","Valle","Data e Ora"])

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
    selected_day=st.selectbox("Selezionare:  ",options=day_list)
    if selected_day=="Totale": 
        return tab
    else:
        return tab.filter(pl.col("Data")==selected_day)

# grafico tipo persone
def pies_chart(tab,raggr):
    base_pie = (
        alt.Chart(tab)
        .mark_arc(
            cornerRadius=8,
            radius=120,
            radius2=80
        )
        .encode(
            alt.Theta("numero"),
            alt.Color(raggr).scale(scheme="paired")
        )
    )

    text_pie = (
        alt.Chart(tab)
        .mark_text(radius=140, size=15)
        .encode(
            alt.Text("numero"),
            alt.Theta("numero").stack(True),
            alt.Order(raggr),
            alt.Color(raggr)
        )
    )
    
    total_text = (
        alt.Chart(tab)
        .mark_text(radius=0, size=30)
        .encode(
            alt.Text("sum(numero)"),
            color=alt.value("red")
        )
    )

    st.altair_chart(
        base_pie + text_pie + total_text,
        use_container_width=True
    )

# tabella tipo persone grafico tipo persone
def chart_tipo(table,raggr):
    tab=conta_tipo(table,raggr)
    pies_chart(tab,raggr)