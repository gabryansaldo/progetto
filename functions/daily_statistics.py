import streamlit as st
import utils
import altair as alt
import polars as pl
import pandas as pd



def chart_top5(table, group_col, alias, value_col="DATAPASSAGGIO",):
    grouped = (
        table.rename({group_col:alias})
        .group_by(alias)
        .agg(pl.col(value_col).n_unique().alias("Totale"))
        .sort("Totale", descending=True)
    )
    
    top_10 = grouped[:5]
    
    chart = (
        alt.Chart(top_10)
        .mark_bar()
        .encode(
            alt.X("Totale", title="Passaggi Totali"),
            alt.Y(alias, sort="-x", title=""),
            alt.Color(alias, legend=None).scale(scheme="paired"), #viridis
            [alt.Tooltip(alias), alt.Tooltip("Totale", title="Passaggi")]
        )
    )
    return chart


def Daily_Statistics():
    utils.load_dataset()
    st.title("📅 **Analisi dei Passaggi Giornalieri**")
    st.write("Esplora i dati relativi ai passaggi giornalieri degli skipass. Puoi selezionare una data specifica per osservare i dettagli di quel giorno oppure visualizzare un'analisi complessiva di tutti i passaggi registrati.")
    
    tab=st.session_state.passaggi.select(["DATAPASSAGGIO","CODICEBIGLIETTO","NOME_TIPOPERSONA","NOME_TIPOBIGLIETTO"])

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
    col2.write(f"*{max_pers}*")
    col3.write("Registrato il:")
    col4.write(f"*{max_data_pers}*")

    spaz,col1,col2,col3,col4=st.columns([0.03,0.35,0.2,0.25,0.4])
    col1.write("**🏆 Record di passaggi:**")
    col2.write(f"*{max_pas}*")
    col3.write("Registrato il:")
    col4.write(f"*{max_data_pas}*")
    
    st.divider()
    st.write("Selezionare se visualizzare le analisi su tutti i giorni o su un giorno specifico")
    table=utils.filter_day(st.session_state.passaggi)

    top10=utils.group_by_skipass(table)[:10]
    st.dataframe(top10.select(["Data","CODICEBIGLIETTO","NOME_TIPOPERSONA","passaggi"]))

    utils.podio(top10[:3])

    # utils.chart_tipo(table,"NOME_TIPOPERSONA")
    # utils.chart_tipo(table,"NOME_TIPOBIGLIETTO")

    col1,col2=st.columns(2)
    col1.markdown(f"### Top 5 Valli con più passaggi")
    col1.altair_chart(chart_top5(table,"NOME_VALLEPOSIZIONEIMPIANTO", alias="Valli"),use_container_width=True)
    col2.markdown(f"### Top 5 Impianti con più passaggi")
    col2.altair_chart(chart_top5(table,"NOME_IMPIANTO", alias="Impianti"),use_container_width=True)