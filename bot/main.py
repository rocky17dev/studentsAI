from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from bot.config import logger, get_openai_api_key, get_telegram_token, verify_ffmpeg
from openai_utils.openai_helper import setup_openai
from bot.handlers import (
    TRANS_WAITING_FOR_AUDIO,
    TRANS_WAITING_FOR_FILENAME,
    CLEAN_WAITING_FOR_AUDIO,
    CLEAN_WAITING_FOR_FILENAME,
    start,
    transcribe_command,
    clean_command,
    cancel,
    transcribe_handle_audio,
    transcribe_receive_filename,
    clean_handle_audio,
    clean_receive_filename
)

def main():
    try:
        logger.info("Configurazione di OpenAI in corso...")
        # Configura OpenAI
        setup_openai(get_openai_api_key())
        logger.info("OpenAI configurato correttamente.")
    except Exception as e:
        logger.error(f"Errore durante la configurazione di OpenAI: {e}")
        return

    try:
        # Verifica la corretta configurazione di ffmpeg
        logger.info("Verifica dell'installazione di ffmpeg in corso...")
        verify_ffmpeg()
    except Exception as e:
        logger.error(f"Errore durante la verifica di ffmpeg: {e}")
        return

    try:
        # Crea l'applicazione Telegram
        logger.info("Creazione dell'applicazione Telegram...")
        application = Application.builder().token(get_telegram_token()).build()
        logger.info("Applicazione Telegram creata con successo.")
    except Exception as e:
        logger.error(f"Errore durante la creazione dell'applicazione Telegram: {e}")
        return

    try:
        # Handler per la trascrizione
        logger.info("Registrazione dell'handler per la trascrizione...")
        transcribe_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("transcribe", transcribe_command)],
            states={
                TRANS_WAITING_FOR_AUDIO: [MessageHandler(filters.AUDIO | filters.VOICE, transcribe_handle_audio)],
                TRANS_WAITING_FOR_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, transcribe_receive_filename)],
            },
            fallbacks=[CommandHandler("cancel", cancel)]
        )

        # Handler per la pulizia
        logger.info("Registrazione dell'handler per la pulizia...")
        clean_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("clean", clean_command)],
            states={
                CLEAN_WAITING_FOR_AUDIO: [MessageHandler(filters.AUDIO | filters.VOICE, clean_handle_audio)],
                CLEAN_WAITING_FOR_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, clean_receive_filename)],
            },
            fallbacks=[CommandHandler("cancel", cancel)]
        )

        # Aggiungi gli handler per le conversazioni
        application.add_handler(transcribe_conv_handler)
        application.add_handler(clean_conv_handler)

        # Aggiungi l'handler per il comando /start
        logger.info("Registrazione dell'handler per il comando /start...")
        application.add_handler(CommandHandler("start", start))

        # Avvia l'applicazione
        logger.info("Avvio del bot in corso...")
        application.run_polling()
        logger.info("Bot avviato e in esecuzione.")
        
    except Exception as e:
        logger.error(f"Errore durante la configurazione e l'avvio del bot: {e}")

if __name__ == '__main__':
    main()
