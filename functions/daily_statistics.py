import streamlit as st
import utils
import altair as alt
import polars as pl



def chart_top5(table, group_col, value_col,):
    grouped = (
        table
        .group_by(group_col)
        .agg(pl.col(value_col).n_unique().alias("Totale"))
        .sort("Totale", descending=True)
    )
    
    top_5 = grouped[:5]
    
    chart = (
        alt.Chart(top_5)
        .mark_bar()
        .encode(
            alt.X("Totale", title="Passaggi Totali"),
            alt.Y(group_col, sort="-x", title=""),
            alt.Color(group_col, legend=None).scale(scheme="paired"), #viridis
            [alt.Tooltip(group_col), alt.Tooltip("Totale", title="Passaggi", format=",.0f")]
        )
    )
    return chart


def Intro(table):
    st.title("📅 **Analisi dei Passaggi Giornalieri**")
    st.write("Esplora i dati relativi ai passaggi giornalieri degli skipass. Puoi selezionare una data specifica per osservare i dettagli di quel giorno oppure visualizzare un'analisi complessiva di tutti i passaggi registrati.")
    
    tab=table.select(["DATAPASSAGGIO","CODICEBIGLIETTO","NOME_TIPOPERSONA","NOME_TIPOBIGLIETTO"])

    pers=utils.units_per_day(tab)
    max_row_pers = pers.sort("persone", descending=True).head(1)
    max_data_pers = max_row_pers["Data"][0]
    max_pers = max_row_pers["persone"][0]

    pas=utils.pass_per_day(tab)
    max_row_pas = pas.sort("passaggi", descending=True).head(1)
    max_data_pas = max_row_pas["Data"][0]
    max_pas = max_row_pas["passaggi"][0]

    spaz,col1,col2,col3,col4=st.columns([0.03,0.35,0.2,0.25,0.4])
    col1.write("**🏆 Record di persone:**")
    col2.write(f"*{max_pers:,}*")
    col3.write("Registrato il:")
    col4.write(f"*{max_data_pers}*")

    spaz,col1,col2,col3,col4=st.columns([0.03,0.35,0.2,0.25,0.4])
    col1.write("**🏆 Record di passaggi:**")
    col2.write(f"*{max_pas:,}*")
    col3.write("Registrato il:")
    col4.write(f"*{max_data_pas}*")
    

def Statistic(table):
    st.header("Statistiche")

    spaz,col1,col2,col3,col4=st.columns([0.03,0.35,0.2,0.25,0.4])
    col1.write("**Numero di persone:**")
    col2.write(f"*{len(utils.lista_modalita(table,"CODICEBIGLIETTO")):,}*")

    spaz,col1,col2,col3,col4=st.columns([0.03,0.35,0.2,0.25,0.4])
    col1.write("**Numero di passaggi:**")
    col2.write(f"*{len(table):,}*")

    st.write("### Tipo persona e Tipo Biglietto")
    st.write("i biglietti da 7 a 20 giorni sono stati raggruppati in una modalità unica, clicca sulle sezioni per filtrare")
    st.altair_chart(utils.chart_tipo_interatt(table),use_container_width=True)


def Top(table):
    st.header("Classifica")

    top10=utils.group_by_skipass(table)[:10]
    col1,col2=st.columns([0.52,0.48])
    col1.dataframe(utils.change_columns_title(top10).select(["Data","Codice biglietto","Tipo persona","passaggi"]))
    col2.write("\n")
    col2.write("\n")
    col2.altair_chart(utils.podio(top10[:3]),use_container_width=True)

    col1,col2=st.columns(2)
    col1.markdown(f"### Top 5 Valli con più passaggi")
    col1.altair_chart(chart_top5(utils.change_columns_title(table),"Valle","Data passaggio"),use_container_width=True)
    col2.markdown(f"### Top 5 Impianti con più passaggi")
    col2.altair_chart(chart_top5(utils.change_columns_title(table),"Impianto","Data passaggio"),use_container_width=True)


def Daily_Statistics():
    utils.load_dataset()
    st.header("PAGINA CON I TESTI ANCORA DA DEFINIRE")
    Intro(st.session_state.passaggi)
    st.divider()
    st.write("Selezionare se visualizzare le analisi su tutti i giorni o su un giorno specifico")
    table=utils.filter_day(st.session_state.passaggi)
    st.divider()
    Statistic(table)
    st.divider()
    Top(table)

