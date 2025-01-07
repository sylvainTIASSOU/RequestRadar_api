
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text, Date, Double, JSON
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from datetime import  timedelta

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    username = Column(String, unique=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    rate_limits = relationship("RateLimit", back_populates="users")
    
    
# table to save request
class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    timestamp = Column(DateTime, default=func.now()) # Horodatage de la requête. type timestamp
    endpoint = Column(String, unique=False) # Endpoint de la requête.
    http_method = Column(String, unique=False)  # Méthode HTTP (GET, POST, etc.).
    status_code = Column(Integer, unique=False) # Code de statut HTTP de la requête.
    response_time = Column(Double, unique=False) # Temps de réponse (ms).
    request_size = Column(Integer, unique=False) # Taille de la requête (en octets).
    response_size = Column(Integer, unique=False) # Taille de la réponse (en octets).
    
    

# table to save rate limite
class RateLimit(Base):
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="rate_limits")
    threshold = Column(Integer, unique=False)  # Limite de requêtes par minute.
    endpoint = Column(String, unique=False)  # Endpoint concerné (ou global).
    created_at = Column(DateTime, default=func.now())  # Date de création.
    time_window = Column(Integer, default=60)  # Fenêtre en secondes.
    expires_at = Column(DateTime)  #  colonne pour gérer l'expiration.

    # Calcul automatique de l'expiration si `expires_at` n'est pas défini.
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.expires_at:
    #         self.expires_at = self.created_at + timedelta(seconds=self.time_window)