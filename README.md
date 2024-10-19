# http-traffic-inspector

Questo repository è stato creato per un assignment del corso **Reti Geografiche** con l'obiettivo di monitorare il numero di chiamate HTTP/1, HTTP/2 e HTTP/3 per ogni sito web.

## Descrizione del Progetto

Lo script Python `selenium_config.py` ha il compito di accedere al file `website_classification_100.csv`, recuperare gli URL dei siti, Wireshark viene avviato in modo manuale per monitorare il traffico della rete. Per ogni sito aperto, viene eseguita un'automazione con Selenium. 

Una volta completata la raccolta dati, lo script `analisi_file.py` apre il file di log generato da Wireshark per analizzare il traffico HTTP, distinguendo tra le versioni HTTP/1, HTTP/2 e HTTP/3.

## Componenti del Progetto

- **`selenium_config.py`**: 
  - Recupera gli URL dal file CSV.
  - Avvia Wireshark per monitorare il traffico di rete.
  - Utilizza Selenium per automatizzare l'apertura dei siti e le interazioni su ogni pagina.

- **`analisi_file.py`**:
  - Analizza il file di log generato da Wireshark.
  - Conta il numero di richieste HTTP/1, HTTP/2 e HTTP/3 per ogni sito.

## Obiettivi

- Monitorare e analizzare il traffico HTTP generato da diversi siti web.
- Identificare il numero di richieste HTTP/1.x, HTTP/2 e HTTP/3.
- Automatizzare l'interazione con le pagine web e raccogliere dati di traffico con Wireshark.