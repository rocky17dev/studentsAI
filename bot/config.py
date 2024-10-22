import os
import logging
from dotenv import load_dotenv
import subprocess

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configura il logging
def setup_logging():
    log_file_path = os.path.join(os.path.dirname(__file__), 'config.log')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler(log_file_path),  # Salva i log in un file
            logging.StreamHandler()  # Mostra i log sulla console
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# Recupera la chiave API da .env
def get_openai_api_key():
    logger.info("Tentativo di recuperare la chiave API di OpenAI.")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("La chiave API di OpenAI non è stata trovata nel file .env.")
        exit(1)
    logger.info("Chiave API di OpenAI trovata con successo.")
    return api_key

# Recupera il token del bot Telegram
def get_telegram_token():
    logger.info("Tentativo di recuperare il token del bot Telegram.")
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("Il token del bot Telegram non è stato trovato nel file .env.")
        exit(1)
    logger.info("Token del bot Telegram trovato con successo.")
    return token

# Verifica che ffmpeg sia installato correttamente
def verify_ffmpeg():
    try:
        logger.info("Verifica dell'installazione di ffmpeg in corso...")
        # Esegui il comando ffmpeg per verificare se è stato installato
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("ffmpeg è installato correttamente.")
        else:
            logger.error(f"Errore nell'esecuzione di ffmpeg: {result.stderr}")
    except FileNotFoundError:
        logger.error("ffmpeg non è stato trovato nell'ambiente.")
