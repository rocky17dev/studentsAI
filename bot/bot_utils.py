from utils import logger  # Assumiamo che `utils` contenga il logger

# Funzione per inviare log all'utente Telegram
def send_log_to_user(bot, user_id, message):
    """
    Invia un messaggio di log all'utente tramite il bot Telegram.
    """
    try:
        bot.send_message(chat_id=user_id, text=message)
        logger.info(f"Messaggio inviato all'utente {user_id}: {message}")
    except Exception as e:
        logger.error(f"Errore durante l'invio del messaggio all'utente {user_id}: {e}")

# Funzione per inviare un file audio all'utente Telegram
def send_audio_to_user(bot, user_id, audio_path, caption):
    """
    Invia un file audio all'utente tramite il bot Telegram.
    """
    try:
        with open(audio_path, 'rb') as audio_file:
            bot.send_audio(chat_id=user_id, audio=audio_file, caption=caption)
        logger.info(f"File audio inviato all'utente {user_id}: {audio_path}")
    except Exception as e:
        logger.error(f"Errore durante l'invio dell'audio all'utente {user_id}: {e}")
