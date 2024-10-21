# Usa un'immagine Python come base
FROM python:3.10-slim

# Installa ffmpeg direttamente nel container del bot
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Crea una directory di lavoro
WORKDIR /app

# Copia i file di dipendenze e installale
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice del progetto
COPY . .

# Esporta le variabili d'ambiente, che includeranno anche OpenAI API e Telegram Bot Token
ENV PYTHONUNBUFFERED=1

# Comando per avviare l'app
CMD ["python", "bot/main.py"]
