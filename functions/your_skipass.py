import streamlit as st
import polars as pl
import utils

def Your_Skipass(table):
    st.title("🎟️ Cerca il tuo Skipass")

    st.write("""
    In questa pagina puoi cercare il tuo skipass utilizzando il suo codice.
    Una volta trovato, visualizzerai i dettagli e le statistiche delle tue attività.
    """)

    form1=st.form(key="your_skipass")
    codice = form1.text_input("Inserisci il codice dello skipass:","161-389-25165", placeholder="Es. 161-389-25165")
    form1.form_submit_button("Submit")
    
    skipass_data = table.filter(
        pl.col("CODICEBIGLIETTO") == codice
    )

    if skipass_data.is_empty():
        form1.warning("Nessun dato trovato per questo codice skipass.")
    else:
        form1.subheader("Dettagli del tuo Skipass")
        form1_exp=form1.expander("Visualizza passaggi dettagliati")
        with form1_exp:
            form1_exp.write(utils.fancy_table(skipass_data))

        form1.subheader("Statistiche principali")
        n_passaggi = len(skipass_data)
        primo_passaggio = skipass_data["DATAPASSAGGIO"].min()
        ultimo_passaggio = skipass_data["DATAPASSAGGIO"].max()

        form1.write(f"**Numero di passaggi totali:** {n_passaggi}")
        form1.write(f"**Primo passaggio:** {primo_passaggio.strftime('%d-%m-%Y %H:%M:%S')}")
        form1.write(f"**Ultimo passaggio:** {ultimo_passaggio.strftime('%d-%m-%Y %H:%M:%S')}")
        form1.write(f"**Numero valli:** {utils.conta_mod(skipass_data,"ID_VALLEPOSIZIONEIMPIANTO")}")
        form1.write(f"**Numero impianti diversi:** {utils.conta_mod(skipass_data,"ID_IMPIANTO")}")
        form1.write(f"**Tipo biglietto:** {utils.lista_modalita(skipass_data,"NOME_TIPOBIGLIETTO").to_series()[0]}")
        form1.write(f"**Tipo persona:** {utils.lista_modalita(skipass_data,"NOME_TIPOPERSONA").to_series()[0]}")
        form1.write(f"**Validità Skipass:** {utils.lista_modalita(skipass_data,"NOME_VALLEVALIDITABIGLIETTO").to_series()[0]}")


def Your_SkipassPage():
    utils.load_dataset()
    Your_Skipass(st.session_state.passaggi)