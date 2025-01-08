from datetime import datetime
from fastapi import HTTPException, WebSocket, WebSocketDisconnect, APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, oauth
from sqlalchemy.orm import Session
from ..schemas import request_schema
from ..database import get_db
from ..utils import check_rate_limit
import asyncio

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# Endpoint pour simuler les réponses enregistrées dans la base de données
# Endpoint pour récupérer les statistiques d'utilisation
@router.get("")
def get_analytics(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # Calculer les statistiques : requêtes par minute, taux d'erreur, distribution des temps de réponse
    metrics = db.query(models.Request).all()
    
    total_requests = len(metrics)
    error_requests = len([m for m in metrics if m.status_code >= 400])
    success_requests = total_requests - error_requests
    error_rate = error_requests / total_requests if total_requests > 0 else 0
    response_times = [m.response_time for m in metrics]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    return {
        "total_requests": total_requests,
        "error_rate": error_rate,
        "average_response_time": avg_response_time,
        "success_requests": success_requests
    }
    


# Fonction pour calculer le volume des requêtes
def get_request_volume(metrics):
    return len(metrics)

# Fonction pour calculer le taux d'erreur
def get_error_rate(metrics):
    error_requests = len([m for m in metrics if m.status_code >= 400])
    total_requests = len(metrics)
    return error_requests / total_requests if total_requests > 0 else 0

# Fonction pour calculer le temps de réponse moyen
def get_average_response_time(metrics):
    response_times = [m.response_time for m in metrics]
    return sum(response_times) / len(response_times) if response_times else 0

# Fonction pour récupérer les erreurs sur une période donnée
def get_error_trends(metrics, time_window=60):
    now = datetime.utcnow()
    recent_errors = [m for m in metrics if (now - m.timestamp).seconds <= time_window and m.status_code >= 400]
    return len(recent_errors)

# Fonction pour récupérer les 5 endpoints les plus utilisés
def get_top_endpoints(metrics):
    endpoint_counts = {}
    for m in metrics:
        endpoint_counts[m.endpoint] = endpoint_counts.get(m.endpoint, 0) + 1
    return sorted(endpoint_counts.items(), key=lambda x: x[1], reverse=True)[:5]

# WebSocket pour envoyer des données en temps réel
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):

    
    await websocket.accept()  # Accepter la connexion WebSocket

    while True:
        try:
            # Récupérer toutes les métriques de la base de données
            metrics = db.query(models.Request).all()

            # Calculer les différentes métriques
            total_requests = get_request_volume(metrics)
            error_rate = get_error_rate(metrics)
            avg_response_time = get_average_response_time(metrics)
            error_trends = get_error_trends(metrics)
            top_endpoints = get_top_endpoints(metrics)

            # Préparer les données à envoyer
            data = {
                "total_requests": total_requests,
                "error_rate": error_rate,
                "average_response_time": avg_response_time,
                "error_trends": error_trends,
                "top_endpoints": top_endpoints
            }

            # Envoyer les données au client
            await websocket.send_json(data)

            # Attendre 1 seconde avant de renvoyer les données suivantes
            await asyncio.sleep(1)

        except WebSocketDisconnect:
            print("Client déconnecté")
            break