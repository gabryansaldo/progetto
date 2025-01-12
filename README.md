## STRUTTURA

Il file principale, app.py, rappresenta il punto di ingresso dell'applicazione e gestisce la navigazione tra le diverse pagine. 
Le funzioni di utilità generali sono raccolte nel file utils.py, mentre i file relativi alle quattro pagine principali dell'app (daily_statistics, hourly_analysis, welcome e your_skipass) sono contenuti nella cartella functions. 
La cartella others, invece, contiene elementi accessori utili al funzionamento dell'applicazione.

Nella directory principale si trovano inoltre il dataset DatiPassaggi.csv.gz su cui si basa l'applicazione e un file chiamato START.py, che consente un avvio più rapido.

L'intero progetto è stato sviluppato utilizzando Git per il controllo di versione e un ambiente virtuale dedicato, creato per garantire la corretta gestione delle dipendenze.

---

## COME INIZIARE

L'applicazione può essere visualizzata e utilizzata in tre modi:

1. Da prompt dei comandi: Dopo aver impostato la directory del progetto come working directory, è sufficiente eseguire il comando seguente per avviare l'applicazione.
    ```bash
    uv run streamlit run app.py
    ```

2. Utilizzando il file START.py: Questo file automatizza l'esecuzione del comando sopra. Su Windows, è sufficiente fare doppio clic sul file per avviare rapidamente l'applicazione.

3. Attraverso Streamlit Cloud: Grazie all'integrazione con GitHub, l'applicazione è accessibile direttamente online tramite il link: [progetto.streamlit.app](progetto.streamlit.app.).


Appena si accede all'applicazione, in alto è presente un tab "Informazioni". 
Questo tab guida l'utente a una sezione dedicata, dove sono disponibili dettagli sull'applicazione e sul suo utilizzo.

---

## BIBLIOGRAFIA

Fonti utilizzate:

- https://docs.streamlit.io/
- https://streamlit.io/cloud
- https://altair-viz.github.io/
- https://chatgpt.com/
- https://stackoverflow.com/
- Moodle del corso