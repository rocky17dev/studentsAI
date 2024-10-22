import logging
import os
from logging.handlers import RotatingFileHandler

# Definisci la configurazione del logger
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'bot.log')

# Definisci il formato del log
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Dimensione massima del file di log in byte (es. 5MB)
MAX_LOG_FILE_SIZE = 5 * 1024 * 1024  # 5MB
BACKUP_COUNT = 5  # Mantieni fino a 5 file di log di backup

def setup_logging(log_level=logging.INFO):
    """Configura il logger globale."""
    # Crea il logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Definisci l'handler per il file di log con rotazione
    file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=MAX_LOG_FILE_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Definisci l'handler per la console (stream)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Aggiungi gli handler al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Configura il logging quando il modulo viene importato
logger = setup_logging()

# Puoi usare il logger importando questo modulo
if __name__ == '__main__':
    logger.info("Il sistema di logging è stato configurato correttamente.")
