import os
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
import noisereduce as nr
from bot.config import logger, bot  # Assumendo che il bot sia istanziato qui


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
    try:
        bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        logger.error(f"Errore durante l'invio del messaggio all'utente: {e}")

# Funzione per inviare l'audio temporaneo all'utente
def send_audio_to_user(user_id, audio_path, caption):
    try:
        bot.send_audio(chat_id=user_id, audio=open(audio_path, 'rb'), caption=caption)
    except Exception as e:
        logger.error(f"Errore durante l'invio dell'audio all'utente: {e}")


# Funzione per pulire l'audio
def clean_audio(file_path, output_filename, user_id):
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

        # Normalizzazione del volume
        send_log_to_user(user_id, "Normalizzazione del volume in corso...")
        normalized_audio = audio.normalize()

        # Salva e invia il file audio dopo la normalizzazione
        temp_norm_audio_path = os.path.join("tmp", f"{output_filename}_normalized.mp3")
        normalized_audio.export(temp_norm_audio_path, format="mp3")
        send_audio_to_user(user_id, temp_norm_audio_path, "Audio dopo la normalizzazione")

        # Converti in un array NumPy
        y = np.array(normalized_audio.get_array_of_samples(), dtype=np.float32)
        y /= np.max(np.abs(y))
        send_log_to_user(user_id, f"Audio convertito in formato NumPy e normalizzato. Valore massimo: {np.max(y)}")

        # Riduzione del rumore
        send_log_to_user(user_id, f"Riduzione del rumore in corso con fattore di riduzione: {noise_factor}")
        y_denoised = nr.reduce_noise(y=y, sr=normalized_audio.frame_rate, prop_decrease=noise_factor)
        send_log_to_user(user_id, f"Riduzione del rumore completata. Valore massimo: {np.max(y_denoised)}")

        # Salva e invia il file audio dopo la riduzione del rumore
        temp_denoised_audio_path = os.path.join("tmp", f"{output_filename}_denoised.mp3")
        denoised_audio = AudioSegment(
            y_denoised.tobytes(), 
            frame_rate=normalized_audio.frame_rate, 
            sample_width=2, 
            channels=1
        )
        denoised_audio.export(temp_denoised_audio_path, format="mp3")
        send_audio_to_user(user_id, temp_denoised_audio_path, "Audio dopo la riduzione del rumore")

        # Applicazione dei filtri Butterworth
        send_log_to_user(user_id, "Inizio applicazione del filtro high-pass.")
        y_filtered_hp = butter_filter(y_denoised, low_cutoff, high_cutoff, normalized_audio.frame_rate, btype='high')
        send_log_to_user(user_id, f"Filtro high-pass applicato. Valore massimo: {np.max(y_filtered_hp)}")

        # Salva e invia il file audio dopo il filtro high-pass
        temp_hp_audio_path = os.path.join("tmp", f"{output_filename}_highpass.mp3")
        hp_audio = AudioSegment(
            y_filtered_hp.tobytes(), 
            frame_rate=normalized_audio.frame_rate, 
            sample_width=2, 
            channels=1
        )
        hp_audio.export(temp_hp_audio_path, format="mp3")
        send_audio_to_user(user_id, temp_hp_audio_path, "Audio dopo il filtro high-pass")

        send_log_to_user(user_id, "Inizio applicazione del filtro low-pass.")
        y_filtered_lp = butter_filter(y_filtered_hp, low_cutoff, high_cutoff, normalized_audio.frame_rate, btype='low')
        send_log_to_user(user_id, f"Filtro low-pass applicato. Valore massimo: {np.max(y_filtered_lp)}")

        # Salva e invia il file audio dopo il filtro low-pass
        temp_lp_audio_path = os.path.join("tmp", f"{output_filename}_lowpass.mp3")
        lp_audio = AudioSegment(
            y_filtered_lp.tobytes(), 
            frame_rate=normalized_audio.frame_rate, 
            sample_width=2, 
            channels=1
        )
        lp_audio.export(temp_lp_audio_path, format="mp3")
        send_audio_to_user(user_id, temp_lp_audio_path, "Audio dopo il filtro low-pass")

        # Controlla se l'audio è silenzioso
        if np.max(np.abs(y_filtered_lp)) == 0:
            send_log_to_user(user_id, "Il segnale audio è completamente silenzioso, possibile problema nel processo.")
            return None

        # Salva l'audio pulito finale
        output_path = os.path.join("tmp", f"{output_filename}.mp3")
        cleaned_audio = AudioSegment(
            y_filtered_lp.tobytes(), 
            frame_rate=normalized_audio.frame_rate, 
            sample_width=2, 
            channels=1
        )
        cleaned_audio.export(output_path, format="mp3")
        send_log_to_user(user_id, f"Audio pulito salvato correttamente come MP3: {output_path}")
        send_audio_to_user(user_id, output_path, "Audio pulito finale")

        return output_path

    except Exception as e:
        send_log_to_user(user_id, f"Errore durante la pulizia dell'audio: {e}")
        logger.error(f"Errore durante la pulizia dell'audio: {e}")
        return None

# Esempio di utilizzo
if __name__ == "__main__":
    user_id = 'USER_TELEGRAM_ID'  # Identificatore dell'utente Telegram
    cleaned_audio_path = clean_audio('input_audio.wav', 'output_audio', user_id)
