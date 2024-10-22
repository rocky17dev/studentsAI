import os
import json
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
import noisereduce as nr
from bot.config import logger

# Funzione per caricare la configurazione dal file JSON
def load_config(config_file="config.json"):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            logger.info(f"Configurazione caricata correttamente da {config_file}.")
            return config
    except Exception as e:
        logger.error(f"Errore durante il caricamento della configurazione: {e}")
        return None

# Funzione per applicare filtri Butterworth
def butter_filter(data, lowcut, highcut, fs, btype='low'):
    try:
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        if btype == 'band':
            logger.info(f"Applicazione filtro Butterworth a banda con cutoff {lowcut}-{highcut} Hz.")
            b, a = butter(4, [low, high], btype='band')
        else:
            logger.info(f"Applicazione filtro Butterworth {btype} con cutoff {lowcut if btype == 'low' else highcut} Hz.")
            b, a = butter(4, low if btype == 'low' else high, btype=btype)
        filtered_data = filtfilt(b, a, data)
        logger.info(f"Filtro {btype} applicato con successo.")
        return filtered_data
    except Exception as e:
        logger.error(f"Errore durante l'applicazione del filtro Butterworth: {e}")
        return None

# Funzione per pulire l'audio
def clean_audio(file_path, output_filename, config):
    try:
        noise_factor = config['noise_factor']
        low_cutoff = config['low_cutoff']
        high_cutoff = config['high_cutoff']
        filter_type = config['filter_type']

        logger.info(f"Pulizia dell'audio iniziata per il file: {file_path}")

        # Carica il file audio
        audio = AudioSegment.from_file(file_path)
        logger.info(f"Audio caricato con successo. Durata: {len(audio)} ms")

        if len(audio) == 0:
            logger.error("L'audio è vuoto.")
            return None

        # Normalizzazione del volume
        logger.info("Normalizzazione del volume in corso...")
        normalized_audio = audio.normalize()

        # Converti in un array NumPy
        y = np.array(normalized_audio.get_array_of_samples(), dtype=np.float32)
        y /= np.max(np.abs(y))  # Normalizza
        logger.info(f"Audio convertito in formato NumPy e normalizzato. Valore massimo: {np.max(y)}")

        # Riduzione del rumore
        logger.info(f"Riduzione del rumore con fattore di riduzione: {noise_factor}")
        y_denoised = nr.reduce_noise(y=y, sr=normalized_audio.frame_rate, prop_decrease=noise_factor)
        logger.info(f"Riduzione del rumore completata. Valore massimo: {np.max(y_denoised)}")

        # Equalizzazione del segnale (filtri Butterworth)
        if filter_type in ['high', 'both']:
            logger.info("Inizio applicazione del filtro high-pass.")
            y_filtered_hp = butter_filter(y_denoised, low_cutoff, high_cutoff, normalized_audio.frame_rate, btype='high')
            logger.info(f"Filtro high-pass applicato. Valore massimo: {np.max(y_filtered_hp)}")
        else:
            y_filtered_hp = y_denoised

        if filter_type in ['low', 'both']:
            logger.info("Inizio applicazione del filtro low-pass.")
            y_filtered_lp = butter_filter(y_filtered_hp, low_cutoff, high_cutoff, normalized_audio.frame_rate, btype='low')
            logger.info(f"Filtro low-pass applicato. Valore massimo: {np.max(y_filtered_lp)}")
        else:
            y_filtered_lp = y_filtered_hp

        # Controlla se l'audio è silenzioso
        if np.max(np.abs(y_filtered_lp)) == 0:
            logger.error("Il segnale audio è completamente silenzioso, possibile problema nel processo.")
            return None

        # Aggiungi un'estensione MP3 al nome del file
        output_path = os.path.join("tmp", f"{output_filename}.mp3")

        # Salva l'audio pulito in un file MP3
        cleaned_audio = AudioSegment.from_raw(file_path, sample_width=2, frame_rate=normalized_audio.frame_rate, channels=1)
        cleaned_audio.export(output_path, format="mp3")
        logger.info(f"Audio pulito salvato correttamente come MP3: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Errore durante la pulizia dell'audio: {e}")
        return None

# Esempio di utilizzo
if __name__ == "__main__":
    # Carica la configurazione dal file JSON
    config = load_config("config.json")
    
    if config:
        # Esegui la pulizia dell'audio con i parametri dalla configurazione
        cleaned_audio_path = clean_audio('input_audio.wav', 'output_audio', config)