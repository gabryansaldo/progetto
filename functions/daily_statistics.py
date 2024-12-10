import streamlit as st
import utils
import altair as alt
import polars as pl



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
    #st.dataframe(utils.units_per_day(st.session_state.passaggi))
    #st.dataframe(utils.pass_per_day(st.session_state.passaggi))
    
    table=utils.filter_day(st.session_state.passaggi)
    cont=st.container(border=True)

    pers=utils.units_per_day(table)
    max_row_pers = pers.sort("persone", descending=True).head(1)
    max_data_pers = max_row_pers["Data"][0]
    max_pers = max_row_pers["persone"][0]

    pas=utils.pass_per_day(table)
    max_row_pas = pas.sort("passaggi", descending=True).head(1)
    max_data_pas = max_row_pas["Data"][0]
    max_pas = max_row_pas["passaggi"][0]

    
    if len(pers)>1:
        totpers=pers["persone"].sum()
        totpas=pas["passaggi"].sum()
        cont.markdown(f"""
            <div style="
                font-size: 24px; 
                font-weight: bold; 
                color: #2C3E50; 
                text-align: center; 
                padding: 10px; 
                margin: 10px 0; 
                border-radius: 10px; 
                background-color: #ECF0F1;">
                Totale persone: <span style="color: #16A085;">{totpers}</span>
            </div>
        """, unsafe_allow_html=True)
        
        cont.markdown(f"""
            <div style="
                font-size: 24px; 
                font-weight: bold; 
                color: #2C3E50; 
                text-align: center; 
                padding: 10px; 
                margin: 10px 0; 
                border-radius: 10px; 
                background-color: #ECF0F1;">
                Totale passaggi: <span style="color: #16A085;">{totpas}</span>
            </div>
        """, unsafe_allow_html=True)
        cont.markdown(f"""
            <div style="
                font-size: 24px; 
                font-weight: bold; 
                color: #2C3E50;
                text-align: center;">
                Massimo passaggi:
                <div style="font-size: 20px; margin-top: 10px;">
                    Data: <span style="color: #E74C3C;">{max_data_pers}</span>
                </div>
                <div style="font-size: 20px; margin-top: 10px;">
                    Numero di persone: <span style="color: #E74C3C;">{max_pers}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        cont.write(f"Totale passaggi: {totpas}")
        cont.write(f"Massimo delle persone: {max_pers} registrato il {max_data_pers}")
        cont.write(f"Massimo dei passaggi: {max_pas} registrato il {max_data_pas}")
    else:
        cont.write(f"Numero delle persone registrato: {max_pers}")
        cont.write(f"Numero dei passaggi registrato: {max_pas}")
    


    st.dataframe(utils.group_by_skipass(table)[:10])
    #utils.chart_tipo(table,"NOME_TIPOPERSONA")
    #utils.chart_tipo(table,"NOME_TIPOBIGLIETTO")

    col1,col2=st.columns(2)
    col1.markdown(f"### Top 5 Valli con più passaggi")
    col1.altair_chart(chart_top5(table,"NOME_VALLEPOSIZIONEIMPIANTO", alias="Valli"),use_container_width=True)
    col2.markdown(f"### Top 5 Impianti con più passaggi")
    col2.altair_chart(chart_top5(table,"NOME_IMPIANTO", alias="Impianti"),use_container_width=True)