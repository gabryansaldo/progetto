import streamlit as st
import utils
import base64
import pandas as pd
import numpy as np
import time
import altair as alt
import polars as pl

def Test():
    a=1
    b=[2,4]
    b.append(a)
    st.write(b)


#######################################

def summary_with_chart(table, group_col, value_col="CODICEBIGLIETTO"):
    """
    Crea un riepilogo con grafico a barre interattivo che mostra i passaggi totali per valle o impianto.
    
    Args:
        table (pl.DataFrame): Il dataset.
        group_col (str): Colonna per il raggruppamento (es. "NOME_VALLEPOSIZIONEIMPIANTO").
        value_col (str): Colonna da contare (default: "CODICEBIGLIETTO").
    """
    # Raggruppa e conta i valori
    grouped = (
        table.lazy()
        .group_by(group_col)
        .agg(pl.col(value_col).n_unique().alias("Totale"))
        .collect()
        .sort("Totale", reverse=True)
    )
    
    # Seleziona il top 10 per una visualizzazione più chiara
    top_10 = grouped[:10]
    
    # Grafico con Altair
    chart = (
        alt.Chart(top_10.to_pandas())
        .mark_bar()
        .encode(
            x=alt.X("Totale:Q", title="Passaggi Totali"),
            y=alt.Y(f"{group_col}:N", sort="-x", title=""),
            color=alt.Color(f"{group_col}:N", legend=None),
            tooltip=[alt.Tooltip(f"{group_col}:N", title="Valle/Impianto"), alt.Tooltip("Totale:Q", title="Passaggi")]
        )
        .properties(
            title=f"Top 10 per {group_col.replace('_', ' ').title()}",
            height=400,
            width=600
        )
    )

    # Mostra il riepilogo in Streamlit
    st.markdown(f"### Top 10 {group_col.replace('_', ' ').title()} con più passaggi")
    st.altair_chart(chart, use_container_width=True)

def summary_card(title, value, icon, color="blue"):
    """
    Crea una card con un'icona e un valore per mostrare statistiche in modo elegante.

    Args:
        title (str): Il titolo della card (es. "Totale Skipass").
        value (str/int): Il valore numerico o stringa da visualizzare.
        icon (str): Il nome di un'icona FontAwesome (es. "fas fa-skiing").
        color (str): Il colore della card (es. "blue", "green").
    """
    st.markdown(
        f"""
        <div style="
            border-radius: 8px; 
            padding: 16px; 
            background-color: #f9f9f9; 
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); 
            margin-bottom: 16px;">
            <div style="display: flex; align-items: center;">
                <i class="{icon}" style="font-size: 36px; color: {color}; margin-right: 16px;"></i>
                <div>
                    <h4 style="margin: 0; color: {color};">{title}</h4>
                    <p style="margin: 0; font-size: 20px; font-weight: bold;">{value}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def Home():
    st.title("Benvenuto nel Sistema Skipass 🎿")
    st.subheader("Statistiche principali:")

    # Esempio di utilizzo
    skipass_data = st.session_state.passaggi
    totale_skipass = skipass_data.select(pl.col("CODICEBIGLIETTO").unique()).height
    totale_passaggi = skipass_data.height

    # Usa la funzione summary_card
    summary_card("Totale Skipass Unici", totale_skipass, "fas fa-id-card", "green")
    summary_card("Totale Passaggi", totale_passaggi, "fas fa-users", "blue")
    summary_card("Valle più visitata", "Gardena - Alpe di Siusi", "fas fa-mountain", "purple")

    st.markdown("---")
    st.write("Usa il menu a sinistra per esplorare analisi orarie e informazioni sul tuo skipass!")



