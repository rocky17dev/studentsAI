# bot/bot_utils.py

from utils import logger  # Usa il logger da utils

# Funzione per inviare un messaggio di testo generico all'utente Telegram
async def send_message(bot, user_id, message, parse_mode=None):
    """
    Invia un messaggio generico all'utente tramite il bot Telegram.
    """
    try:
        await bot.send_message(chat_id=user_id, text=message, parse_mode=parse_mode)
        logger.info(f"Messaggio inviato all'utente {user_id}: {message}")
    except Exception as e:
        logger.error(f"Errore durante l'invio del messaggio all'utente {user_id}: {e}")

# Funzione per inviare log all'utente Telegram
async def send_log_to_user(bot, user_id, message):
    """
    Invia un messaggio di log all'utente tramite il bot Telegram.
    """
    await send_message(bot, user_id, message)  # Usa await per inviare il log

# Funzione per inviare un file audio all'utente Telegram
async def send_audio_to_user(bot, user_id, audio_path, caption):
    """
    Invia un file audio all'utente tramite il bot Telegram.
    """
    try:
        with open(audio_path, 'rb') as audio_file:
            await bot.send_audio(chat_id=user_id, audio=audio_file, caption=caption)
        logger.info(f"File audio inviato all'utente {user_id}: {audio_path}")
    except Exception as e:
        logger.error(f"Errore durante l'invio dell'audio all'utente {user_id}: {e}")

# Funzione per inviare un documento all'utente Telegram
async def send_document_to_user(bot, user_id, document_path, caption):
    """
    Invia un documento all'utente tramite il bot Telegram.
    """
    try:
        with open(document_path, 'rb') as doc_file:
            await bot.send_document(chat_id=user_id, document=doc_file, caption=caption)
        logger.info(f"Documento inviato all'utente {user_id}: {document_path}")
    except Exception as e:
        logger.error(f"Errore durante l'invio del documento all'utente {user_id}: {e}")
