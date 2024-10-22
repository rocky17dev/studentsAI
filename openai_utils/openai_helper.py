import openai
from bot.config import logger

# Configura OpenAI
def setup_openai(api_key):
    try:
        openai.api_key = api_key
        logger.info("Chiave API di OpenAI configurata con successo.")
    except Exception as e:
        logger.error(f"Errore durante la configurazione della chiave API di OpenAI: {e}")
        raise

# Funzione per trascrivere audio tramite Whisper
def transcribe_audio_with_whisper(file_path, language="it"):
    try:
        logger.info(f"Inizio trascrizione del file audio: {file_path} con Whisper, lingua: {language}.")
        with open(file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language=language
            )
        logger.info(f"Trascrizione completata per il file: {file_path}.")
        return transcript.get('text', "").strip()

    except openai.OpenAIError as e:
        logger.error(f"Errore OpenAI durante la trascrizione del file {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Errore generale durante la trascrizione del file {file_path}: {e}")
        return None
