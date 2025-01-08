from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth
import random
import time
from datetime import datetime

router = APIRouter(
    prefix="/mock",
    tags=["Mock"]
)

# Fonction pour simuler les requêtes en arrière-plan
def generate_mock_requests(user_id: str, db: Session, stop_event: utils.StopEvent):
    while not stop_event.is_set():
        # Vérifier la limite de taux
        if not utils.check_rate_limit(user_id, "/mock", db):
            stop_event.set()  # Arrêter la tâche si la limite est atteinte
            print(f"Rate limit reached for user {user_id}")
            break

        # Simuler une requête
        method = random.choice(["GET", "POST", "PUT", "DELETE"])
        endpoint = random.choice(["/endpoint1", "/endpoint2", "/endpoint3"])
        status_code = random.choice([200, 404, 500])
        response_time = random.randint(50, 500)
        request_size = random.randint(100, 2000)
        response_size = random.randint(100, 2000)

        # Simuler le temps de réponse
        time.sleep(response_time / 1000)

        # Enregistrer les métriques de la requête
        metric = models.Request(
            timestamp=datetime.utcnow(),
            endpoint=endpoint,
            http_method=method,
            status_code=status_code,
            response_time=response_time,
            request_size=request_size,
            response_size=response_size
        )
        db.add(metric)
        db.commit()
        print(f"Mock request generated: {method} {endpoint}, Status: {status_code}")

# Endpoint principal pour lancer la simulation
@router.post("/start")
def start_mock_requests(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    user_id = str(current_user.id)

    # Créer un événement d'arrêt partagé
    stop_event = utils.create_stop_event()

    # Ajouter la tâche en arrière-plan
    background_tasks.add_task(generate_mock_requests, user_id, db, stop_event)

    return {"message": "Mock requests started in background"}


# endpoint pour arrêter la simulation
@router.get("/stop")
def stop_mock_requests(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    user_id = str(current_user.id)
    stop_event = utils.create_stop_event()
    if stop_event:
        stop_event.set()
        return {"message": "Mock requests stopped"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mock requests not found")
    
    
# endpoint pour obtenir les métriques
@router.get("/metrics")
def get_mock_metrics(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
   
    metrics = db.query(models.Request).all()
    if not metrics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mock metrics not found")
    return metrics