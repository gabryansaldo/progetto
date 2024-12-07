import streamlit as st
import utils
import altair as alt
import polars as pl

def pies_chart(tab):
    base_pie = (
        alt.Chart(tab)
        .mark_arc(
            cornerRadius=8,
            radius=120,
            radius2=80
        )
        .encode(
            alt.Theta("numero"),
            alt.Color("NOME_TIPOPERSONA")
        )
    )

    text_pie = (
        alt.Chart(tab)
        .mark_text(radius=140, size=15)
        .encode(
            alt.Text("numero"),
            alt.Theta("numero").stack(True),
            alt.Order("NOME_TIPOPERSONA"),
            alt.Color("NOME_TIPOPERSONA")
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

def tipo_pers(table):
    tab_pers=utils.conta_tipo(table,"NOME_TIPOPERSONA")
    #st.dataframe(tab_pers)
    pies_chart(tab_pers)

def chart_top10(table, group_col, alias, value_col="DATAPASSAGGIO",):
    grouped = (
        table.rename({group_col:alias})
        .group_by(alias)
        .agg(pl.col(value_col).n_unique().alias("Totale"))
        .sort("Totale", descending=True)
    )
    
    top_10 = grouped[:10]
    
    chart = (
        alt.Chart(top_10)
        .mark_bar()
        .encode(
            x=alt.X("Totale", title="Passaggi Totali"),
            y=alt.Y(alias, sort="-x", title=""),
            color=alt.Color(alias, legend=None, scale=alt.Scale(scheme="tableau20")),
            tooltip=[alt.Tooltip(alias), alt.Tooltip("Totale", title="Passaggi")]
        )
        .properties(
            height=400,
            width=600
        )
    )

    st.markdown(f"## Top 10 {alias} con più passaggi")
    st.altair_chart(chart, use_container_width=True)

def Daily_Statistics():
    utils.load_dataset()
    st.dataframe(utils.units_per_day(st.session_state.passaggi))
    st.dataframe(utils.pass_per_day(st.session_state.passaggi))
    table=utils.filter_day(st.session_state.passaggi)
    st.dataframe(utils.group_by_skipass(table)[:10])
    tipo_pers(table)
    chart_top10(table,"NOME_VALLEPOSIZIONEIMPIANTO", alias="Valli")
    chart_top10(table,"NOME_IMPIANTO", alias="Impianti")