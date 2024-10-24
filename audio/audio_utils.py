import os
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils import logger  # Logger importato da utils
from bot.main import bot  # Assumendo che il bot sia istanziato qui
from audio.audio_utils import clean_audio
from openai_utils.openai_helper import transcribe_audio_with_whisper

# Stati delle conversazioni
TRANS_WAITING_FOR_AUDIO, TRANS_WAITING_FOR_FILENAME = range(2)
CLEAN_WAITING_FOR_AUDIO, CLEAN_WAITING_FOR_FILENAME = range(2)

##########################
# Funzioni per il comando #
##########################

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
    audio_file = update.message.audio or update.message.voice

    if not audio_file:
        await update.message.reply_text("Non ho ricevuto un file audio. Riprova.")
        return TRANS_WAITING_FOR_AUDIO

    file = await audio_file.get_file()
    file_path = await file.download_to_drive(custom_path="tmp/audio_to_transcribe.ogg")
    context.user_data['transcribe_audio_file_path'] = file_path
    logger.info(f"File audio salvato temporaneamente: {file_path}")

    await update.message.reply_text("Grazie! Ora per favore, inviami il nome che vuoi assegnare alla trascrizione.")
    return TRANS_WAITING_FOR_FILENAME

# Funzione per ricevere il nome del file e avviare la trascrizione
async def transcribe_receive_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ricevuto nome file per trascrizione da {update.effective_user.first_name}.")
    filename = update.message.text.strip()
    context.user_data['transcribe_filename'] = filename

    transcript = transcribe_audio_with_whisper(context.user_data['transcribe_audio_file_path'], language="it")
    
    if transcript:
        await update.message.reply_text(f"Trascrizione completata: {transcript}")
    else:
        await update.message.reply_text("Si è verificato un errore durante la trascrizione dell'audio.")
        logger.error("Errore durante la trascrizione dell'audio.")
    
    return ConversationHandler.END

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
    audio_file = update.message.audio or update.message.voice

    if not audio_file:
        await update.message.reply_text("Non ho ricevuto un file audio. Riprova.")
        return CLEAN_WAITING_FOR_AUDIO

    file = await audio_file.get_file()
    file_path = await file.download_to_drive(custom_path="tmp/audio_to_clean.ogg")
    context.user_data['clean_audio_file_path'] = file_path
    logger.info(f"File audio salvato temporaneamente: {file_path}")

    await update.message.reply_text("Grazie! Ora per favore, inviami il nome che vuoi assegnare al file pulito.")
    return CLEAN_WAITING_FOR_FILENAME

# Funzione per ricevere il nome del file e avviare la pulizia
async def clean_receive_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filename = update.message.text.strip()
    context.user_data['clean_filename'] = filename
    logger.info(f"Nome file ricevuto: {filename}")

    # Avvia la pulizia dell'audio e invia l'audio in fasi
    await update.message.reply_text("Inizio pulizia dell'audio...")
    
    # Prima fase: Normalizzazione
    cleaned_audio_path = clean_audio(context.user_data['clean_audio_file_path'], filename, step='normalize')
    if cleaned_audio_path:
        with open(cleaned_audio_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file, caption="Audio dopo la normalizzazione")
    
    # Seconda fase: Riduzione rumore
    cleaned_audio_path = clean_audio(context.user_data['clean_audio_file_path'], filename, step='denoise')
    if cleaned_audio_path:
        with open(cleaned_audio_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file, caption="Audio dopo la riduzione del rumore")
    
    # Terza fase: Filtro High-pass
    cleaned_audio_path = clean_audio(context.user_data['clean_audio_file_path'], filename, step='highpass')
    if cleaned_audio_path:
        with open(cleaned_audio_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file, caption="Audio dopo il filtro high-pass")
    
    # Quarta fase: Filtro Low-pass
    cleaned_audio_path = clean_audio(context.user_data['clean_audio_file_path'], filename, step='lowpass')
    if cleaned_audio_path:
        with open(cleaned_audio_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file, caption="Audio dopo il filtro low-pass")
    
    if cleaned_audio_path:
        logger.info(f"Pulizia dell'audio completata per {update.effective_user.first_name}. File salvato in {cleaned_audio_path}.")
        await update.message.reply_text("Pulizia dell'audio completata!")

        # Rimuovi i file temporanei
        os.remove(cleaned_audio_path)
        os.remove(context.user_data['clean_audio_file_path'])
        logger.info(f"File audio temporaneo {cleaned_audio_path} rimosso.")
    else:
        await update.message.reply_text("Si è verificato un errore durante la pulizia dell'audio.")
        logger.error("Errore durante la pulizia dell'audio.")
    
    return ConversationHandler.END

##########################
# Funzione di cancellazione #
##########################

# Funzione per annullare la conversazione
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Conversazione annullata da {update.effective_user.first_name}.")
    await update.message.reply_text('Operazione annullata.')
    return ConversationHandler.END
