Ecco un esempio di file di documentazione che spiega come cambiare i parametri e fornisce una descrizione dettagliata di tutti i parametri disponibili:

---

# Documentazione - Configurazione dei parametri di pulizia audio

Questa documentazione ti guiderà attraverso il processo di configurazione dei parametri per la pulizia dell'audio. I parametri possono essere modificati direttamente nel file di configurazione `config.json`. Di seguito, trovi una spiegazione di ciascun parametro disponibile e come modificarlo per ottenere risultati diversi.

## File di configurazione: `config.json`

Il file `config.json` contiene tutti i parametri configurabili per la pulizia dell'audio. Ecco un esempio di come appare:

```json
{
    "noise_factor": 0.2,
    "low_cutoff": 300.0,
    "high_cutoff": 3400.0,
    "filter_type": "both"
}
```

### Parametri disponibili

#### 1. `noise_factor` (float)
- **Descrizione**: Questo parametro controlla il fattore di riduzione del rumore. Un valore più alto ridurrà più rumore, ma potrebbe anche influire sulla qualità dell'audio.
- **Valore predefinito**: `0.2`
- **Intervallo consigliato**: `0.05 - 0.5`
- **Modifica**: Per ridurre più rumore, aumenta il valore. Ad esempio:
  ```json
  "noise_factor": 0.3
  ```
  Questo aumenterà la riduzione del rumore.

#### 2. `low_cutoff` (float)
- **Descrizione**: Definisce la frequenza di taglio inferiore per il filtro passa-basso o passa-banda. Frequenze al di sotto di questo valore verranno attenuate.
- **Valore predefinito**: `300.0` (Hz)
- **Intervallo consigliato**: `20.0 - 1000.0` (Hz)
- **Modifica**: Se desideri mantenere più frequenze basse, puoi abbassare questo valore. Ad esempio:
  ```json
  "low_cutoff": 150.0
  ```
  In questo modo verranno mantenute più frequenze basse.

#### 3. `high_cutoff` (float)
- **Descrizione**: Definisce la frequenza di taglio superiore per il filtro passa-alto o passa-banda. Frequenze al di sopra di questo valore verranno attenuate.
- **Valore predefinito**: `3400.0` (Hz)
- **Intervallo consigliato**: `1000.0 - 8000.0` (Hz)
- **Modifica**: Se vuoi mantenere più frequenze alte, puoi aumentare questo valore. Ad esempio:
  ```json
  "high_cutoff": 5000.0
  ```
  Questo manterrà più frequenze alte nel segnale.

#### 4. `filter_type` (string)
- **Descrizione**: Questo parametro controlla quali filtri vengono applicati all'audio. Puoi scegliere tra tre opzioni:
  - `high`: Applica solo un filtro passa-alto.
  - `low`: Applica solo un filtro passa-basso.
  - `both`: Applica sia il filtro passa-alto che quello passa-basso (configurazione predefinita).
- **Valore predefinito**: `both`
- **Opzioni disponibili**: `high`, `low`, `both`
- **Modifica**: Se desideri applicare solo un filtro passa-alto, puoi cambiare il valore così:
  ```json
  "filter_type": "high"
  ```

### Come modificare i parametri

1. **Apertura del file di configurazione**:
   - Apri il file `config.json` con un editor di testo.
   - All'interno del file, troverai i parametri configurabili elencati sopra.

2. **Modifica dei valori**:
   - Cambia i valori come desiderato seguendo le linee guida sopra. Ad esempio, per aumentare la riduzione del rumore e cambiare il tipo di filtro, puoi modificare i parametri in questo modo:
     ```json
     {
         "noise_factor": 0.3,
         "low_cutoff": 200.0,
         "high_cutoff": 4500.0,
         "filter_type": "high"
     }
     ```

3. **Salvataggio del file**:
   - Dopo aver modificato i valori, salva il file `config.json`.

4. **Esecuzione del programma**:
   - Esegui il programma Python che utilizza il file di configurazione. Il programma leggerà automaticamente i nuovi valori dal file `config.json` e li applicherà durante il processo di pulizia dell'audio.

### Esempio di utilizzo

Dopo aver configurato i parametri, puoi eseguire il programma che utilizza queste impostazioni:

```bash
python3 clean_audio.py
```

Il programma applicherà la riduzione del rumore e i filtri all'audio in base ai parametri definiti nel file `config.json`, e salverà l'audio pulito in formato MP3.

### Note

- Assicurati di mantenere la struttura del file JSON corretta. Un errore nel formato JSON (ad esempio, una virgola mancante o una parentesi non chiusa) impedirà al programma di caricare correttamente i parametri.
- Il file di output sarà sempre salvato in formato MP3 nella directory `tmp` con il nome specificato.

---

Puoi utilizzare questa guida per modificare facilmente i parametri di pulizia dell'audio senza dover intervenire sul codice Python.