## STRUTTURA

### Files
Il file principale app.py gestisce la navigazione tra le pagine dell'app. Le funzioni generali sono in utils.py, mentre i file delle quattro pagine si trovano nella cartella functions. La cartella others contiene elementi accessori. Nella directory principale ci sono anche il dataset DatiPassaggi.csv.gz e il file START.py per un avvio più rapido.

---

### Sviluppo e Gestione del Progetto
L'intero progetto è stato sviluppato utilizzando Git per il controllo di versione e un ambiente virtuale dedicato, creato per garantire la corretta gestione delle dipendenze.

---

## COME INIZIARE

### Avvio
L'applicazione può essere visualizzata e utilizzata in tre modi:

1. Da prompt dei comandi: Dopo aver clonato la repository e impostato la directory del progetto come working directory, è sufficiente eseguire il comando seguente per avviare l'applicazione.
    ```bash
    uv run streamlit run app.py
    ```

2. Utilizzando il file START.py: Questo file automatizza l'esecuzione del comando sopra. Su Windows, è sufficiente fare doppio clic sul file per avviare rapidamente l'applicazione.

3. Attraverso Streamlit Cloud: Grazie all'integrazione con GitHub, l'applicazione è accessibile direttamente online tramite il link: [progetto.streamlit.app](https://progetto.streamlit.app/). All'avvio dell'applicazione, potrebbe essere richiesto di riavviarla, poiché, dopo un certo periodo di inattività, va in stand-by. Il "risveglio" avviene in meno di un minuto.

---

### Navigazione nell'App
Appena si accede all'applicazione, in alto è presente un tab "Informazioni". 
Questo tab guida l'utente a una sezione dedicata, dove sono disponibili dettagli sull'applicazione e sul suo utilizzo.

---

## INFORMAZIONI

Il dataset, le funzionalità dell'app e il preprocessing applicato sono descritti all'interno dell'app stessa, nelle sezioni (tabs) accessibili dalla parte superiore della pagina iniziale.

---

## BIBLIOGRAFIA

Fonti utilizzate:

- https://docs.streamlit.io/
- https://streamlit.io/cloud
- https://altair-viz.github.io/
- https://chatgpt.com/
- https://stackoverflow.com/
- Moodle del corso