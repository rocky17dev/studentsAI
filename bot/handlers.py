from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from audio.audio_utils import clean_audio
from openai_utils.openai_helper import transcribe_audio_with_whisper
from bot.config import logger

TRANS_WAITING_FOR_AUDIO, TRANS_WAITING_FOR_FILENAME = range(2)
CLEAN_WAITING_FOR_AUDIO, CLEAN_WAITING_FOR_FILENAME = range(2)

# Funzione per il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Comando /start ricevuto da {update.effective_user.first_name}.")
    try:
        with open('welcome.txt', 'r', encoding='utf-8') as f:
            welcome_message = f.read()
        logger.info("Messaggio di benvenuto caricato con successo.")
    except Exception as e:
        logger.error(f"Errore durante la lettura del messaggio di benvenuto: {e}")
        welcome_message = "Benvenuto nel bot multifunzionale! Si è verificato un errore nel caricamento del messaggio di benvenuto."

    await update.message.reply_text(welcome_message, parse_mode='Markdown')

######################
# Trascrizione Audio #
######################

# Funzione per il comando /transcribe
async def transcribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Comando /transcribe ricevuto da {update.effective_user.first_name}.")
    await update.message.reply_text("Per favore, inviami il file audio che desideri trascrivere.")
    return TRANS_WAITING_FOR_AUDIO

# Funzione per ricevere il file audio nella trascrizione
async def transcribe_handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ricevuto file audio da {update.effective_user.first_name} per la trascrizione.")
    # Simile alla versione originale con logica per la gestione del file
    # Una volta ricevuto il file, salva il percorso e passa allo stato successivo
    ...

# Funzione per ricevere il nome del file e avviare la trascrizione
async def transcribe_receive_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ricevuto nome file per trascrizione da {update.effective_user.first_name}.")
    # Gestisce la ricezione del nome del file e chiama la funzione di trascrizione
    ...

# Funzione asincrona per gestire la trascrizione
async def transcribe_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Avvio della trascrizione dell'audio per {update.effective_user.first_name}.")
    # Gestisce la trascrizione usando la funzione di OpenAI e invia i file all'utente
    ...

##################
# Pulizia Audio  #
##################

# Funzione per il comando /clean
async def clean_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Comando /clean ricevuto da {update.effective_user.first_name}.")
    await update.message.reply_text("Per favore, inviami il file audio che desideri pulire.")
    return CLEAN_WAITING_FOR_AUDIO

# Funzione per ricevere il file audio nella pulizia
async def clean_handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ricevuto file audio da {update.effective_user.first_name} per la pulizia.")
    # Logica per ricevere e salvare l'audio da pulire
    ...

# Funzione per ricevere il nome del file e avviare la pulizia
async def clean_receive_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ricevuto nome file per la pulizia da {update.effective_user.first_name}.")
    # Gestisce la ricezione del nome del file e chiama la funzione di pulizia
    ...

# Funzione per pulire l'audio e inviare il file all'utente
async def clean_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Avvio della pulizia dell'audio per {update.effective_user.first_name}.")
    file_path = context.user_data['clean_audio_file_path']
    filename = context.user_data['clean_filename']
    cleaned_audio_path = clean_audio(file_path, filename)

    if cleaned_audio_path:
        logger.info(f"Pulizia dell'audio completata per {update.effective_user.first_name}. File salvato in {cleaned_audio_path}.")
        # Invia il file audio pulito
        with open(cleaned_audio_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file)
        os.remove(cleaned_audio_path)
        os.remove(file_path)
        logger.info(f"File audio temporaneo {cleaned_audio_path} rimosso.")

##########################
# Funzione di cancellazione #
##########################

# Funzione per annullare la conversazione
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Conversazione annullata da {update.effective_user.first_name}.")
    await update.message.reply_text('Operazione annullata.')
    return ConversationHandler.END
