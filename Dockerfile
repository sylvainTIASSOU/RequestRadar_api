# Utilisez une image légère spécifique à Python
FROM python:3.12-slim-bullseye

# Configurez des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    DOTENV_PATH=/app/.env

# Installez les dépendances système nécessaires pour dlib et face-recognition
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-python-dev \
    libboost-thread-dev \
    locales \
    && echo "fr_FR.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen fr_FR.UTF-8 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Définissez les variables d'environnement pour la locale
ENV LANG=fr_FR.UTF-8 \
    LANGUAGE=fr_FR:fr \
    LC_ALL=fr_FR.UTF-8

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer uniquement les dépendances pour optimiser le cache Docker
COPY requirements.txt .

# Assurez-vous d'utiliser la dernière version de pip
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposez le port de l'application
EXPOSE 8001

# Commande pour exécuter l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
