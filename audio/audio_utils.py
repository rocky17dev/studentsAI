import os
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
import noisereduce as nr
from bot.config import logger

# Funzione per applicare filtri Butterworth
def butter_filter(data, lowcut, highcut, fs, btype='low'):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if btype == 'band':
        b, a = butter(4, [low, high], btype='band')
    else:
        b, a = butter(4, low if btype == 'low' else high, btype=btype)
    return filtfilt(b, a, data)

# Funzione per pulire l'audio
def clean_audio(file_path, output_filename, noise_factor=0.2, low_cutoff=300.0, high_cutoff=3400.0):
    try:
        # Carica il file audio
        audio = AudioSegment.from_file(file_path)

        if len(audio) == 0:
            logger.error("L'audio è vuoto.")
            return None

        # Normalizzazione del volume
        normalized_audio = audio.normalize()

        # Converti in un array NumPy
        y = np.array(normalized_audio.get_array_of_samples(), dtype=np.float32)
        y /= np.max(np.abs(y))  # Normalizza

        # Riduzione del rumore
        y_denoised = nr.reduce_noise(y=y, sr=normalized_audio.frame_rate, prop_decrease=noise_factor)

        # Equalizzazione del segnale
        y_filtered_hp = butter_filter(y_denoised, low_cutoff, high_cutoff, normalized_audio.frame_rate, btype='high')
        y_filtered_lp = butter_filter(y_filtered_hp, low_cutoff, high_cutoff, normalized_audio.frame_rate, btype='low')

        # Salva l'audio pulito in un file MP3
        output_path = os.path.join("tmp", output_filename)
        sf.write(output_path, y_filtered_lp, normalized_audio.frame_rate)
        logger.info(f"Audio pulito salvato: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Errore durante la pulizia dell'audio: {e}")
        return None
