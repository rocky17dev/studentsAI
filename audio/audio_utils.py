import os
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
import noisereduce as nr
from utils import logger  # Importa solo il logger

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

# Funzione per inviare log all'utente Telegram
def send_log_to_user(user_id, message):
    from bot.main import bot  # Importa bot solo qui per evitare l'import circolare
    try:
        bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        logger.error(f"Errore durante l'invio del messaggio all'utente: {e}")

# Funzione per inviare l'audio temporaneo all'utente
def send_audio_to_user(user_id, audio_path, caption):
    from bot.main import bot  # Importa bot solo qui per evitare l'import circolare
    try:
        bot.send_audio(chat_id=user_id, audio=open(audio_path, 'rb'), caption=caption)
    except Exception as e:
        logger.error(f"Errore durante l'invio dell'audio all'utente: {e}")

# Funzione per pulire l'audio
def clean_audio(file_path, output_filename, user_id, step='final'):
    try:
        noise_factor = 0.2
        low_cutoff = 300.0
        high_cutoff = 3000.0

        send_log_to_user(user_id, f"Pulizia dell'audio iniziata per il file: {file_path}")

        # Carica il file audio
        audio = AudioSegment.from_file(file_path)
        send_log_to_user(user_id, f"Audio caricato con successo. Durata: {len(audio)} ms")

        if len(audio) == 0:
            send_log_to_user(user_id, "L'audio è vuoto.")
            return None

        # Step 1: Normalizzazione del volume
        if step == 'normalize':
            send_log_to_user(user_id, "Normalizzazione del volume in corso...")
            normalized_audio = audio.normalize()

            # Salva e invia il file audio dopo la normalizzazione
            temp_norm_audio_path = os.path.join("tmp", f"{output_filename}_normalized.mp3")
            normalized_audio.export(temp_norm_audio_path, format="mp3")
            send_audio_to_user(user_id, temp_norm_audio_path, "Audio dopo la normalizzazione")
            return temp_norm_audio_path

        # Step 2: Riduzione del rumore
        elif step == 'denoise':
            y = np.array(audio.get_array_of_samples(), dtype=np.float32)
            y /= np.max(np.abs(y))
            send_log_to_user(user_id, f"Riduzione del rumore in corso con fattore di riduzione: {noise_factor}")
            y_denoised = nr.reduce_noise(y=y, sr=audio.frame_rate, prop_decrease=noise_factor)

            temp_denoised_audio_path = os.path.join("tmp", f"{output_filename}_denoised.mp3")
            denoised_audio = AudioSegment(
                y_denoised.tobytes(), 
                frame_rate=audio.frame_rate, 
                sample_width=2, 
                channels=1
            )
            denoised_audio.export(temp_denoised_audio_path, format="mp3")
            send_audio_to_user(user_id, temp_denoised_audio_path, "Audio dopo la riduzione del rumore")
            return temp_denoised_audio_path

        # Step 3: Applicazione del filtro high-pass
        elif step == 'highpass':
            y_denoised = np.array(audio.get_array_of_samples(), dtype=np.float32)
            send_log_to_user(user_id, "Inizio applicazione del filtro high-pass.")
            y_filtered_hp = butter_filter(y_denoised, low_cutoff, high_cutoff, audio.frame_rate, btype='high')

            temp_hp_audio_path = os.path.join("tmp", f"{output_filename}_highpass.mp3")
            hp_audio = AudioSegment(
                y_filtered_hp.tobytes(), 
                frame_rate=audio.frame_rate, 
                sample_width=2, 
                channels=1
            )
            hp_audio.export(temp_hp_audio_path, format="mp3")
            send_audio_to_user(user_id, temp_hp_audio_path, "Audio dopo il filtro high-pass")
            return temp_hp_audio_path

        # Step 4: Applicazione del filtro low-pass
        elif step == 'lowpass':
            y_filtered_hp = np.array(audio.get_array_of_samples(), dtype=np.float32)
            send_log_to_user(user_id, "Inizio applicazione del filtro low-pass.")
            y_filtered_lp = butter_filter(y_filtered_hp, low_cutoff, high_cutoff, audio.frame_rate, btype='low')

            temp_lp_audio_path = os.path.join("tmp", f"{output_filename}_lowpass.mp3")
            lp_audio = AudioSegment(
                y_filtered_lp.tobytes(), 
                frame_rate=audio.frame_rate, 
                sample_width=2, 
                channels=1
            )
            lp_audio.export(temp_lp_audio_path, format="mp3")
            send_audio_to_user(user_id, temp_lp_audio_path, "Audio dopo il filtro low-pass")
            return temp_lp_audio_path

        # Step finale: Pulizia completa e invio dell'audio finale
        else:
            # Esegui tutte le fasi sopra in sequenza e salva il file finale
            # Restituisci il percorso del file finale
            return "Percorso del file finale"
    
    except Exception as e:
        send_log_to_user(user_id, f"Errore durante la pulizia dell'audio: {e}")
        logger.error(f"Errore durante la pulizia dell'audio: {e}")
        return None
