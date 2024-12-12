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
    codice = form1.text_input("Inserisci il codice dello skipass:","161-166-84544", placeholder="Es. 161-166-84544")
    form1.markdown("*Altri esempi: &nbsp;&nbsp;&nbsp; 161-122-7872 &nbsp;&nbsp;&nbsp; 161-247-49204*", unsafe_allow_html=True)
    form1.form_submit_button("Submit")   # 161-122-7872   161-247-49204
    
    skipass_data = utils.fancy_table(table.filter(
            pl.col("CODICEBIGLIETTO") == codice
        )
    )

    if skipass_data.is_empty():
        form1.warning("Nessun dato trovato per questo codice skipass.")
    else:
        st.divider()

        st.subheader("Statistiche principali")
        st.write("")

        spaz,testo=st.columns([0.03,0.97])

        skipass_data=utils.tab_day_hour(skipass_data)

        ggsciati=utils.lista_modalita(skipass_data,"Data")
        testo.write(f"**Numero di giorni diversi sciati:** {len(ggsciati)}")

        tab_days=[skipass_data]
        if len(ggsciati) > 1:   
            day_options=ggsciati
            day_options.insert(0,"Totale")
            col1,col2,col3=testo.columns([0.4,0.3,0.3])
            selected_day=col1.selectbox("Seleziona giorno da visulizzare o il totale:  ",options=day_options, index=len(day_options)-1)
            selected_index = day_options.index(selected_day)
            for i in range(1,len(ggsciati)):
                tab_days.append(skipass_data.filter(pl.col("Data")==ggsciati[i]))
        else:
            selected_index = 0
            selected_day=ggsciati[0]

        st.write("")
        primo_passaggio = tab_days[selected_index]["DATAPASSAGGIO"].min()
        ultimo_passaggio = tab_days[selected_index]["DATAPASSAGGIO"].max()
        col1,col2=testo.columns(2)
        col1.write(f"""**Primo passaggio:**\n\n{primo_passaggio}""")
        col2.write(f"""**Ultimo passaggio:**\n\n{ultimo_passaggio}""")
        st.write("")

        col1, col2, col3 = testo.columns(3)

        npas=len(tab_days[selected_index])
        nvalli=utils.conta_mod(tab_days[selected_index],"NOME_VALLEPOSIZIONEIMPIANTO")
        nimp=utils.conta_mod(tab_days[selected_index],"NOME_IMPIANTO")

        
        if selected_index in [0, 1]:
            delta_pas,delta_valli,delta_imp="","",""
            label_vis="hidden"
        else:
            delta_pas=npas-len(tab_days[selected_index-1])
            delta_valli=nvalli-utils.conta_mod(tab_days[selected_index-1],"NOME_VALLEPOSIZIONEIMPIANTO")
            delta_imp=nimp-utils.conta_mod(tab_days[selected_index-1],"NOME_IMPIANTO")
            label_vis="visible"
            testo.info("Dati paragonati a quelli del giorno precedente")
        
        col1.metric("**Numero di passaggi totali:**", npas, delta_pas,label_visibility=label_vis) 
        col2.metric("**Numero valli:**", nvalli, delta_valli)
        col3.metric("**Numero impianti diversi:**", nimp, delta_imp)

        st.divider()
        
        st.subheader("Dettagli biglietto")
        st.write("")
        spaz,col0,col1,col2=st.columns([0.03,0.02,0.3,0.65])
        col0.write("-")
        col1.write(f"**Tipo biglietto:**")
        col2.write(utils.lista_modalita(tab_days[selected_index],"NOME_TIPOBIGLIETTO")[0])
        
        spaz,col0,col1,col2=st.columns([0.03,0.02,0.3,0.65])
        col0.write("-")        
        col1.write(f"**Tipo persona:**")
        col2.write(utils.lista_modalita(tab_days[selected_index],"NOME_TIPOPERSONA")[0])
        
        spaz,col0,col1,col2=st.columns([0.03,0.02,0.3,0.65])
        col0.write("-")        
        col1.write(f"**Validità Skipass:**")
        col2.write(utils.lista_modalita(tab_days[selected_index],"NOME_VALLEVALIDITABIGLIETTO")[0])
        
        spaz,col0,col1,col2=st.columns([0.03,0.02,0.3,0.65])
        col0.write("-")        
        col1.write(f"**Cassa di acquisto:**")
        col2.write(utils.lista_modalita(tab_days[selected_index],"NOME_CASSA")[0])


        st.divider()

        dett_exp=st.expander(f"Visualizza passaggi dettagliati di: {selected_day}")
        with dett_exp:
            dett_exp.dataframe(utils.minimal_table(tab_days[selected_index]),use_container_width=True)


def Your_SkipassPage():
    utils.load_dataset()
    Your_Skipass(st.session_state.passaggi)