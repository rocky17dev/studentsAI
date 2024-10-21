import os
import logging
from dotenv import load_dotenv
import subprocess

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configura il logging
def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# Recupera la chiave API da .env
def get_openai_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("La chiave API di OpenAI non è stata trovata nel file .env.")
        exit(1)
    return api_key

# Recupera il token del bot Telegram
def get_telegram_token():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("Il token del bot Telegram non è stato trovato nel file .env.")
        exit(1)
    return token

# Verifica che ffmpeg sia installato correttamente
def verify_ffmpeg():
    try:
        # Esegui il comando ffmpeg per verificare se è stato installato
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("ffmpeg è installato correttamente.")
        else:
            logger.error(f"Errore nell'esecuzione di ffmpeg: {result.stderr}")
    except FileNotFoundError:
        logger.error("ffmpeg non è stato trovato nell'ambiente.")
