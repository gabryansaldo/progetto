import streamlit as st
import utils
import altair as alt

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
    

def Daily_Statistics():
    utils.load_dataset()
    st.dataframe(utils.units_per_day(st.session_state.passaggi))
    st.dataframe(utils.pass_per_day(st.session_state.passaggi))
    st.dataframe(utils.group_by_skipass(st.session_state.passaggi))
    tipo_pers(st.session_state.passaggi)