# Usa un'immagine Python come base
FROM python:3.10-slim

# Installa ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Crea una directory di lavoro
WORKDIR /app

# Copia i file di dipendenze e installale
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice del progetto
COPY . .

# Aggiungi la directory di lavoro al PYTHONPATH
ENV PYTHONPATH=/app

# Esporta le variabili d'ambiente
ENV PYTHONUNBUFFERED=1

# Comando per avviare l'app
CMD ["python", "bot/main.py"]
