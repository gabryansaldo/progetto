import polars as pl
import streamlit as st
import icecream as ic

# carico il dataset
url = "../progetto/Gabry.csv"
table = pl.read_csv(url,separator=",")
n=len(table)

# cambio formato di DATAPASSAGGIO da str a Datetime
table = table.with_columns(
    pl.col("DATAPASSAGGIO").str.strptime(pl.Datetime, "%d-%m-%Y %H:%M:%S")
)  #print(table.select(pl.col("DATAPASSAGGIO")))

# funzione che ritorna una lista contenente le modalità di una data variabile (colonna)
def lista_modalità(table,variabile):
    return table.select(variabile).unique().sort(variabile)

# scelgo se vedere totale o solo delle cose selezionate
def selezione_pass(table):
    show_totals = st.checkbox(f"Mostra totali per ora")
    if show_totals:
        return hourly_pass_T(table)
    else:
        return hourly_pass_vi(table)

# divido per orario
def hourly_pass_T(table):
    return table.with_columns(pl.col("DATAPASSAGGIO").dt.hour().alias("ora")
        ).group_by("ora").agg(pl.len().alias("PASSAGGI")
        ).sort("ora")

#divido per orario e valle/impianto
def hourly_pass_vi(table):
    opzioni_map = {
        "valle": "NOME_VALLEPOSIZIONEIMPIANTO",
        "impianto": "NOME_IMPIANTO"
    }
    
    c_aka = st.selectbox("Raggruppamento:", options=list(opzioni_map.keys()), index=0)
    c = opzioni_map[c_aka]

    lista_mod = lista_modalità(table,c)

    mod_selezionate = st.multiselect(
        f"Inserisci {c_aka} di interesse",
        lista_mod,
        help="Seleziona uno o più valori per filtrare i dati"
    )

    filtered_table = (
        table.filter(pl.col(c).is_in(mod_selezionate))
        if mod_selezionate
        else table
    )

    if filtered_table.is_empty():
        st.warning("Nessun dato corrisponde ai filtri selezionati.")
        return pl.DataFrame()
    
    result = (
        filtered_table
        .with_columns(pl.col("DATAPASSAGGIO").dt.hour().alias("ora"))
        .group_by(["ora", c])  # Raggruppa per ora e valle/impianto
        .agg(pl.len().alias("PASSAGGI"))  # Conta i passaggi
        .pivot(
            values="PASSAGGI",  # I valori da mostrare nelle celle
            index="ora",  # Righe
            on=c  # Colonne
        )
        .fill_null(0)  # Riempi i valori nulli con 0
        .sort("ora")
    )
    return result

result = selezione_pass(table)

if not result.is_empty():
    st.write(result)

# IDEE
#
# specificare che il dataset si riferisce ad un giorno solo ed eseguire una verica a schermo
# in hourly_pass_vi migliorare la selezione tra valle e impianto
# grafico per ora e minuti per impianto... (forse non ha senso)