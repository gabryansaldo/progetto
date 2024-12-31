import streamlit as st
import utils
import altair as alt
import polars as pl


# grafico a barre per migliori 5 per passaggi
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
            alt.Color(group_col, legend=None).scale(scheme="rainbow"), #viridis
            [alt.Tooltip(group_col), alt.Tooltip("Totale", title="Passaggi", format=",.0f")]
        )
    )
    return chart

# prima parte della pagina (introduzione)
def Intro(table):
    st.title("📅 **Analisi dei Passaggi Giornalieri**")
    st.write("Esplora i dati relativi ai passaggi giornalieri degli skipass. Si può selezionare una data specifica per osservare i dettagli di quel giorno oppure visualizzare un'analisi complessiva di tutti i passaggi registrati.")
    
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
    
# paragrafo statische del giorno/totale selzionato
def Statistic(table):
    st.header("Statistiche")

    spaz,col1,col2,col3,col4=st.columns([0.03,0.35,0.15,0.45,0.1])
    col1.write("**- Numero di persone:**")
    persone=len(utils.lista_modalita(table,"CODICEBIGLIETTO"))
    col2.write(f"*{persone:,}*")

    col3.write("**- Numero di impianti aperti:**")
    col4.write(f"*{len(utils.lista_modalita(table,"NOME_IMPIANTO")):,}*")


    spaz,col1,col2,col3,col4=st.columns([0.03,0.35,0.15,0.45,0.1])
    col1.write("**- Numero di passaggi:**")
    passaggi=len(table)
    col2.write(f"*{passaggi:,}*")

    col3.write("**- Passaggi medi per persona:**")
    col4.write(f"*{round(passaggi/persone,2):,}*")

    st.write("\n")
    st.write("#### 🔍 Interazione tra Tipologia di Biglietto e Tipo di Persona")
    spaz,col=st.columns([0.03,0.97])
    col.write(f"""Questo grafico interattivo è composto da due sezioni:
              \n- 🍰**Grafico a Torta** (a sinistra): Mostra la distribuzione delle tipologie di biglietto, con le modalità da 7 giorni in su (7 Giorni, 8 Giorni...) raggruppate nella categoria "7+ Giorni".
              \n- 📊**Grafico a Barre** (a destra): Visualizza la distribuzione delle tipologie di persona in base alla selezione effettuata nel grafico a torta.
              \n**Interagendo**🖱️ con il grafico:
              \n- Cliccando una sezione del grafico a torta, il grafico a barre si aggiorna per mostrare solo i dati relativi alla tipologia di biglietto scelta.
              \n- Cliccando al centro del grafico a torta, si torna alla visualizzazione generica senza alcun filtraggio, permettendo di osservare la distribuzione complessiva.
              """)
    st.altair_chart(utils.chart_tipo_interatt(table),use_container_width=True)
    spaz,col=st.columns([0.03,0.97])
    col.write("Si osserva che la proporzione delle tipologie di persone che acquistano un determinato tipo di biglietto rimane generalmente costante. Tuttavia, i Kid e i Senior mostrano una preferenza maggiore per il biglietto stagionale rispetto ad altre categorie, che invece non presentano variazioni significative in base al tipo di biglietto scelto.")

# clasifica persone con più passaggi con dataframe e podio
def Top(table):
    st.header("Skipass con più passaggi")
    st.write("Classifica dei 10 skipass che hanno registrato il maggior numero di passaggi in un giorno nel periodo selezionato.")

    top10=utils.group_by_skipass(table)[:10]
    col1,col2=st.columns([0.52,0.48])
    col1.dataframe(utils.change_columns_title(top10).select(["Data","Codice biglietto","Tipo persona","passaggi"]))
    col2.write("\n")
    col2.write("\n")
    col2.altair_chart(utils.podio(top10[:3]),use_container_width=True)

    st.divider()

    st.header("Valli e Impianti con più passaggi")
    st.write("Nel grafico a barre a sinistra, vengono mostrate le 5 valli con il maggior numero di passaggi per il periodo selezionato. A destra, il grafico a barre illustra gli impianti con i 5 valori più alti di passaggi, offrendo una panoramica chiara delle località con la maggiore affluenza.")
    col1,col2=st.columns(2)
    col1.altair_chart(chart_top5(utils.change_columns_title(table),"Valle","Data passaggio"),use_container_width=True)
    col2.altair_chart(chart_top5(utils.change_columns_title(table),"Impianto","Data passaggio"),use_container_width=True)

# main della pagina, richiamo altre funzioni
def Daily_Statistics():
    utils.load_dataset()
    Intro(st.session_state.passaggi)
    st.divider()
    st.write("Selezionare se visualizzare le analisi su tutti i giorni o su un giorno specifico, la scelta avrà effetto su tutta la pagina")
    table=utils.filter_day(st.session_state.passaggi)
    st.divider()
    Statistic(table)
    st.divider()
    Top(table)

