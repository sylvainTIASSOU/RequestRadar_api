import asyncio
from dotenv import load_dotenv
from passlib.context import CryptContext
import locale
import base64
import hashlib
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import RateLimit
from threading import Event

# Charger les variables d'environnement
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # scpecifie le type de criptagaque 

def hash(password: str):
    return pwd_context.hash(password)

def verify (plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Fonction pour vérifier le rate limit
def check_rate_limit(user_id: str, endpoint: str, db: Session, threshold: int = 100, time_window: int = 60):
    """
    Vérifie si l'utilisateur a dépassé le seuil de requêtes par minute pour un endpoint donné.
    
    :param user_id: Identifiant de l'utilisateur.
    :param endpoint: Endpoint concerné.
    :param db: Session de la base de données.
    :param threshold: Limite maximale de requêtes (par défaut 100).
    :param time_window: Fenêtre de temps en secondes (par défaut 60 secondes).
    :return: True si la requête est autorisée, False sinon.
    """
    # Fenêtre de temps de limitation
    window_start = datetime.utcnow() - timedelta(seconds=time_window)

    # Compter les requêtes récentes de l'utilisateur pour cet endpoint
    recent_requests = (
        db.query(RateLimit)
        .filter(
            RateLimit.user_id == user_id,
            RateLimit.endpoint == endpoint,
            RateLimit.created_at >= window_start
        )
        .count()
    )

    # Si le nombre de requêtes dépasse le seuil, bloquer
    if recent_requests >= threshold:
        return False

    # Enregistrer la nouvelle requête
    new_limit = RateLimit(
        user_id=user_id,
        endpoint=endpoint,
        threshold=threshold,
        created_at=datetime.utcnow()
    )
    db.add(new_limit)
    db.commit()

    return True

def get_requests_last_minute(user_ip: str):
    # Simuler l'obtention des requêtes de la dernière minute (en production, vous pouvez utiliser Redis ou une autre solution)
    return random.randint(0, 200)  # Exemple simulé


def create_stop_event():
    """Crée un événement asyncio pour arrêter une tâche."""
    return asyncio.Event()

class StopEvent:
    events = {}

    @staticmethod
    def create(user_id: str):
        if user_id not in StopEvent.events:
            StopEvent.events[user_id] = Event()

    @staticmethod
    def get(user_id: str) -> Event:
        return StopEvent.events.get(user_id, None)

    @staticmethod
    def set(user_id: str):
        if user_id in StopEvent.events:
            StopEvent.events[user_id].set()

    @staticmethod
    def is_set(user_id: str) -> bool:
        event = StopEvent.get(user_id)
        return event.is_set() if event else True