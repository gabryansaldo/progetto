3 modi per aprirlo
 start solo windows
 cmd
 progetto.streamlit.app

appena si apre informazioni in alto tabs

modalità chiara o scura indifferente

origine dataset



############

	
    Buongiorno,
    alcune informazioni aggiuntive sul progetto, raccogliendo un po' di input delle ultime settimane. Se avete ulteriori domande fatemele qui sul forum, così siamo tuttə aggiornatə.


    Consegna del progetto
    Se volete sostenere l'esame al primo appello (giovedì 23 gennaio), il progetto va consegnato al più tardi entro giovedì 16 gennaio❗. La consegna avverrà tramite moodle con due possibili modalità: tramite url di un repository github pubblico con il vostro codice (preferibile) oppure tramite un file zip contenente tutto il vostro progetto.

    Cosa deve contenere il progetto?
        - Il codice della vostra applicazione streamlit, commentato appropriatamente❗
        - Un file README❗ che descrive la struttura e lo scopo del progetto
        - Una descrizione❗ dei dati che avete usato, della fonte e del preprocessing applicato. Questa descrizione può essere nel README, nell'applicazione o in un file a parte: l'importante è che sia facile trovarla
        - I dati necessari a eseguire il vostro progetto. Eventualmente potete automatizzarne il download: in questo caso sinceratevi che funzioni.
        - I file generati da `uv`❗ per gesitre le dipendenze (opzionale ma fortemente raccomandato)

    È obbligatorio usare `uv`?
    No, non è obbligatorio. Un progetto che non usa `uv` può certamente essere sufficiente o buono, difficilmente però sarà valutato come ottimo.

    Quanto testo devo scrivere nell'applicazione?
    L'applicazione deve essere "parlante" e "autodescrittiva": le figure devono essere corredate da chiare descrizioni❗ testuali che indichino come leggerle e quali informazioni presentano, eventuali interazioni❗ devono essere descritte chiaramente.

    Come viene valutato il progetto?
    La rubrica di valutazione considera principalmente i seguenti aspetti:
        - L'analisi e le conclusioni❗ sono presentate chiaramente?
        - L'ampiezza dell'analisi è adeguata?
        - I grafici supportano adeguatamente le conclusioni?
        - Le scelte nella creazione dei grafici sono appropriate❗ (utilizzo dei colori, scelta degli encoding ecc...)?
        - Il preprocessing (quando presente) è appropriato?
        - Quanto semplice è eseguire l'applicazione? Idealmente dovrebbe essere sufficiente fare `uv run streamlit run app.py` senza altri passaggi.
        
    So che i vostri progetti sono molto variegati (ad esempio c'è chi ha più analisi e chi più preprocessing) e che alcuni punti della rubrica (specialmente il secondo) sono un po' vaghi. Per questo vi invito a confrontarvi con me prima dell'esame per eventualmente aggiustare il tiro. Ovviamente non posso dirvi che voto prenderete, però posso eventualmente suggerirvi di approfondire e estendere l'analisi. A tal proposito fisserò dei ricevimenti ad-hoc. Se non potete venire a quei ricevimenti scrivetemi via mail

    Un paio di questioni tecniche

    - Se usate windows e quando eseguite `uv add` ricevete un errore riguardo gli "hard link" il problema è dovuto a OneDrive e al fatto che uv cerca di creare una cache in una cartella gestita da OneDrive. La soluzione più semplice è eseguire `uv add` sempre con l'opzione `--no-cache`. Ad esempio: `uv add --no-cache streamlit polars`

    - Quando nel vostro programma vi riferite a un file, non utilizzate il percorso assoluto. Ovvero, non scrivete `file = "C:\\User\matteo\progetto\dati\data.csv"`. Non riuscirò mai a eseguire senza problemi il vostro programma sul mio computer, semplicemente perchè la mia gerarchia di cartelle è diversa dalla vostra (e perchè uso Linux). Usate invece percorsi relativi alla radice del progetto, ovvero alla cartella che contiene il README.md e il pyproject.toml. Nell'esempio precedente, se la cartella radice del progetto è `C:\\User\matteo\progetto` allora nel codice riferitevi semplicemente a `file = "dati\data.csv"`. Questo però non risolve il problema che io eseguirò il mio codice su Linux e non su windows: la differenza è che Windows usa `\` per separare le cartelle nei percorsi, mentre Linux e MacOS usano `/`. Ci sono due soluzioni:

    Mettete tutti i file nella cartella radice del progetto, così non ci sono sottocartelle da gestire su piattaforme diverse. Soluzione semplice.
    Usate il modulo [pathlib❗](https://docs.python.org/3/library/pathlib.html#module-pathlib) della libreria standard. Nell'esempio precedente, avendo prima eseguito `from pathlib import Path` potete scrivere `file = Path("dati") / "data.csv"`. Soluzione generale che vi potrebbe tornare utile in futuro.
    Un suggerimento
    Un buon test che potete fare per verificare che il vostro codice sia robusto è provare a eseguirlo sul computer di qualche collega. In questo modo scoprite immediatamente se avete dimenticato di registrare delle dipendenze con `uv` o se ci sono dei percorsi di file assoluti.


    Scrivetemi se avete altre domande.

    Cordialmente,
    Matteo Ceccarello