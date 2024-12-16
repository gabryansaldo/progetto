import streamlit as st
import utils
import base64
import pandas as pd
import numpy as np
import time
import altair as alt
import polars as pl

def Test():
    #utils.load_dataset()
    # Esempio di dataset
    data = {
        "NOME_TIPOBIGLIETTO": ["1 Giorno", "2 Giorni", "7 Giorni", "10 Giorni", "20 Giorni", "Stagionale", "Pomeridiano"],
        "numero": [100, 150, 70, 50, 30, 20, 90]
    }

    # Creazione del DataFrame
    table = pl.DataFrame(data)

    # Creazione di una nuova colonna con la categorizzazione
    table = table.with_columns(
        pl.when(
            pl.col("NOME_TIPOBIGLIETTO")
            .str.extract(r"^(\d+)", 1)  # Estrai il numero dall'inizio della stringa
            .is_not_null()              # Controlla che l'estrazione abbia avuto successo
        ).then(pl.lit("7+ Giorni"))  # Se condizione vera, assegna "7+ Giorni"        
        # .otherwise(pl.col("NOME_TIPOBIGLIETTO"))  # Altrimenti, mantieni il nome originale
        .alias("NOME_TIPOBIGLIETTO_CATEGORIZZATO")  # Dai un nome alla nuova colonna
    )

    # Raggruppamento e aggregazione
    table_grouped = table.group_by("NOME_TIPOBIGLIETTO_CATEGORIZZATO").agg(
        pl.sum("numero").alias("totale_vendite")
    )

    # Output
    st.write(table_grouped)