# audio_utils.py

import os
import numpy as np
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
import noisereduce as nr
from utils import logger
from bot_utils import send_log_to_user, send_audio_to_user  # Importa solo bot_utils

def butter_filter(data, lowcut, highcut, fs, btype='low'):
    try:
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(4, [low, high], btype=btype if btype == 'band' else btype)
        return filtfilt(b, a, data)
    except Exception as e:
        logger.error(f"Errore durante l'applicazione del filtro Butterworth: {e}")
        return None

def clean_audio(bot, file_path, output_filename, user_id, step='final'):
    try:
        noise_factor = 0.2
        low_cutoff = 300.0
        high_cutoff = 3000.0

        send_log_to_user(bot, user_id, f"Pulizia dell'audio iniziata per il file: {file_path}")

        audio = AudioSegment.from_file(file_path)
        send_log_to_user(bot, user_id, f"Audio caricato con successo. Durata: {len(audio)} ms")

        if len(audio) == 0:
            send_log_to_user(bot, user_id, "L'audio è vuoto.")
            return None

        # Step 1: Normalizzazione del volume
        if step == 'normalize':
            normalized_audio = audio.normalize()
            temp_norm_audio_path = os.path.join("tmp", f"{output_filename}_normalized.mp3")
            normalized_audio.export(temp_norm_audio_path, format="mp3")
            send_audio_to_user(bot, user_id, temp_norm_audio_path, "Audio dopo la normalizzazione")
            return temp_norm_audio_path

        # Step 2: Riduzione del rumore
        elif step == 'denoise':
            y = np.array(audio.get_array_of_samples(), dtype=np.float32)
            y /= np.max(np.abs(y))
            y_denoised = nr.reduce_noise(y=y, sr=audio.frame_rate, prop_decrease=noise_factor)
            temp_denoised_audio_path = os.path.join("tmp", f"{output_filename}_denoised.mp3")
            denoised_audio = AudioSegment(y_denoised.tobytes(), frame_rate=audio.frame_rate, sample_width=2, channels=1)
            denoised_audio.export(temp_denoised_audio_path, format="mp3")
            send_audio_to_user(bot, user_id, temp_denoised_audio_path, "Audio dopo la riduzione del rumore")
            return temp_denoised_audio_path

        # Step 3: Filtro high-pass
        elif step == 'highpass':
            y_denoised = np.array(audio.get_array_of_samples(), dtype=np.float32)
            y_filtered_hp = butter_filter(y_denoised, low_cutoff, high_cutoff, audio.frame_rate, btype='high')
            temp_hp_audio_path = os.path.join("tmp", f"{output_filename}_highpass.mp3")
            hp_audio = AudioSegment(y_filtered_hp.tobytes(), frame_rate=audio.frame_rate, sample_width=2, channels=1)
            hp_audio.export(temp_hp_audio_path, format="mp3")
            send_audio_to_user(bot, user_id, temp_hp_audio_path, "Audio dopo il filtro high-pass")
            return temp_hp_audio_path

        # Step 4: Filtro low-pass
        elif step == 'lowpass':
            y_filtered_hp = np.array(audio.get_array_of_samples(), dtype=np.float32)
            y_filtered_lp = butter_filter(y_filtered_hp, low_cutoff, high_cutoff, audio.frame_rate, btype='low')
            temp_lp_audio_path = os.path.join("tmp", f"{output_filename}_lowpass.mp3")
            lp_audio = AudioSegment(y_filtered_lp.tobytes(), frame_rate=audio.frame_rate, sample_width=2, channels=1)
            lp_audio.export(temp_lp_audio_path, format="mp3")
            send_audio_to_user(bot, user_id, temp_lp_audio_path, "Audio dopo il filtro low-pass")
            return temp_lp_audio_path

        # Step finale
        else:
            send_log_to_user(bot, user_id, "Pulizia dell'audio completata.")
            return "Percorso del file finale"
    
    except Exception as e:
        send_log_to_user(bot, user_id, f"Errore durante la pulizia dell'audio: {e}")
        logger.error(f"Errore durante la pulizia dell'audio: {e}")
        return None
