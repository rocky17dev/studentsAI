import openai
from bot.config import logger

# Configura OpenAI
def setup_openai(api_key):
    openai.api_key = api_key

# Funzione per trascrivere audio tramite Whisper
def transcribe_audio_with_whisper(file_path, language="it"):
    try:
        with open(file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language=language
            )
            return transcript.get('text', "").strip()
    except openai.OpenAIError as e:
        logger.error(f"Errore durante la trascrizione: {e}")
        return None
    except Exception as e:
        logger.error(f"Errore durante la trascrizione: {e}")
        return None
