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
def clean_audio(file_path, output_filename):
    try:
        # Parametri predefiniti (si possono modificare per ottimizzare il risultato)
        noise_factor = 0.2  # Fattore di riduzione del rumore
        low_cutoff = 300.0  # Taglio frequenze basse
        high_cutoff = 3000.0  # Taglio frequenze alte

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
        logger.info(f"Riduzione del rumore in corso con fattore di riduzione: {noise_factor}")
        y_denoised = nr.reduce_noise(y=y, sr=normalized_audio.frame_rate, prop_decrease=noise_factor)
        logger.info(f"Riduzione del rumore completata. Valore massimo: {np.max(y_denoised)}")

        # Applicazione dei filtri Butterworth per migliorare la qualità della voce
        logger.info("Inizio applicazione del filtro high-pass.")
        y_filtered_hp = butter_filter(y_denoised, low_cutoff, high_cutoff, normalized_audio.frame_rate, btype='high')
        logger.info(f"Filtro high-pass applicato. Valore massimo: {np.max(y_filtered_hp)}")

        logger.info("Inizio applicazione del filtro low-pass.")
        y_filtered_lp = butter_filter(y_filtered_hp, low_cutoff, high_cutoff, normalized_audio.frame_rate, btype='low')
        logger.info(f"Filtro low-pass applicato. Valore massimo: {np.max(y_filtered_lp)}")

        # Controlla se l'audio è silenzioso
        if np.max(np.abs(y_filtered_lp)) == 0:
            logger.error("Il segnale audio è completamente silenzioso, possibile problema nel processo.")
            return None

        # Converti di nuovo in formato AudioSegment per l'esportazione
        cleaned_audio = AudioSegment(
            y_filtered_lp.tobytes(), 
            frame_rate=normalized_audio.frame_rate, 
            sample_width=2, 
            channels=1
        )

        # Aggiungi un'estensione MP3 al nome del file
        output_path = os.path.join("tmp", f"{output_filename}.mp3")

        # Salva l'audio pulito in un file MP3
        cleaned_audio.export(output_path, format="mp3")
        logger.info(f"Audio pulito salvato correttamente come MP3: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Errore durante la pulizia dell'audio: {e}")
        return None

# Esempio di utilizzo
if __name__ == "__main__":
    # Esegui la pulizia dell'audio senza file di configurazione
    cleaned_audio_path = clean_audio('input_audio.wav', 'output_audio')
