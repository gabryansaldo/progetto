import polars as pl
import streamlit as st
import icecream as ic
import gzip

#cd 

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

# divido per orario
def hourly_pass(table):
    return table.with_columns(pl.col("DATAPASSAGGIO").dt.hour().alias("ora")
        ).group_by("ora").agg(pl.count().alias("PASSAGGI")
        ).sort("ora")
#print(hourly_pass(table))

# divido per orario e valle
def hourly_pass_valli(table):
    lista_valli = lista_modalità(table,"NOME_VALLEPOSIZIONEIMPIANTO")

    # seleziona valli
    valli_selezionate = st.multiselect(
        "Inserisci valle di interesse",
        lista_valli,
        default="Gardena - Alpe di Siusi"
    )

def hourly_pass(table):
    opzioni_map = {
        "valle": "NOME_VALLEPOSIZIONEIMPIANTO",
        "impianto": "NOME_IMPIANTO"
    }
    
    c_aka = st.selectbox("Raggruppamento:", options=list(opzioni_map.keys()), index=0)
    c = opzioni_map[c_aka]

    lista_mod = lista_modalità(table,c)

    show_totals = st.checkbox(f"Mostra totali per ora per {c_aka}")

    mod_selezionate = st.multiselect(
        f"Inserisci {c_aka} di interesse",
        lista_mod,
        help="Seleziona uno o più valori per filtrare i dati"
    )

    show_totals = st.checkbox(f"Mostra totali per ora per {c_aka}")

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
            columns=c  # Colonne
        )
        .fill_null(0)  # Riempi i valori nulli con 0
        .sort("ora")
    )

    if show_totals:
        # Se "Mostra totali" è selezionato, somma tutti gli impianti o valli per ciascuna ora
        result = result.with_columns(
            pl.col(result.columns).exclude("ora").sum().alias("Totale")
        )
        st.write("Totali per tutte le valli/impianti selezionati:")
    else:
        st.write(f"Dati raggruppati per {c_aka}:")

    return result

result = hourly_pass(table)

if not result.is_empty():
    st.write(result)


# st.line_chart(hourly_pass_valli_selezionate(table),
#     x="NOME_VALLEPOSIZIONEIMPIANTO",
#     y="T_HAB",
#     color="geo"
# )
#print(table)

