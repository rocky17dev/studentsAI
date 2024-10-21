# studentsAI

Struttura:

project/
│
├── audio/                        # Directory per la logica di gestione audio
│   ├── __init__.py               # Indica che questa è un package
│   ├── audio_utils.py            # Funzioni di trascrizione e pulizia dell'audio
│
├── bot/                          # Directory per la logica del bot
│   ├── __init__.py               # Indica che questa è un package
│   ├── main.py                   # Codice principale del bot
│   ├── handlers.py               # Logica delle conversazioni
│   ├── config.py                 # Configurazione e logging
│
├── openai_utils/                 # Directory per le interfacce con OpenAI
│   ├── __init__.py               # Indica che questa è un package
│   ├── openai_helper.py          # Interfaccia per le API di OpenAI
│
├── tests/                        # Directory per i file di test
│   ├── test_audio.mp3            # File di test per l'audio
│   ├── test_audio_clean.mp3      # File di test per l'audio pulito
│
├── tmp/                          # Directory temporanea per file generati dinamicamente
│   └── ...                       # File audio temporanei
│
├── welcome.txt                   # Messaggio di benvenuto
├── README.md                     # Documentazione del progetto
├── requirements.txt              # Dipendenze Python
├── Procfile                      # Comando per lanciare l'applicazione su Railway
├── nixpacks.toml                 # Configurazione per l'ambiente di Railway
└── .env                          # Variabili d'ambiente, incluso OpenAI API e Telegram Bot Token
