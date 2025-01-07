from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import get_db
from .. import models, oauth
from ..schemas import rate_limits_schema as schemas

router = APIRouter(
    prefix="/rate-limit",
    tags=["Rate Limit"],
)

# Ajouter une règle
@router.post("", status_code=status.HTTP_201_CREATED)
def add_rate_limit(rule: schemas.RateLimitCreate, db: Session = Depends(get_db)):
    new_rule = models.RateLimit(
        user_id=rule.user_id,
        threshold=rule.threshold,
        endpoint=rule.endpoint,
        time_window=rule.time_window,
        expires_at=rule.expires_at,
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule

# Obtenir toutes les règles
@router.get("")
def get_all_rate_limits(db: Session = Depends(get_db)):
    rules = db.query(models.RateLimit).all()
    return rules

# Obtenir une règle par ID
@router.get("/{rule_id}")
def get_rate_limit(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(models.RateLimit).filter(models.RateLimit.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rate limit rule not found")
    return rule

# Mettre à jour une règle
@router.put("/{rule_id}")
def update_rate_limit(rule_id: int, updated_rule: schemas.RateLimitUpdate, db: Session = Depends(get_db)):
    rule = db.query(models.RateLimit).filter(models.RateLimit.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rate limit rule not found")

    rule.user_id = updated_rule.user_id or rule.user_id
    rule.threshold = updated_rule.threshold or rule.threshold
    rule.endpoint = updated_rule.endpoint or rule.endpoint
    rule.time_window = updated_rule.time_window or rule.time_window
    rule.expires_at = updated_rule.expires_at or rule.expires_at

    db.commit()
    db.refresh(rule)
    return rule



# Supprimer une règle
@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rate_limit(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(models.RateLimit).filter(models.RateLimit.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rate limit rule not found")

    db.delete(rule)
    db.commit()
    return {"message": "Rate limit rule deleted successfully"}



# Vérifier une requête
@router.post("/check")
def check_request(endpoint: str, user_id: int = None, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    current_user_id = str(current_user.id)
    now = datetime.utcnow()
    rules = db.query(models.RateLimit).filter(
        (models.RateLimit.user_id == user_id) | (models.RateLimit.user_id == None),
        (models.RateLimit.endpoint == endpoint) | (models.RateLimit.endpoint == None),
        (models.RateLimit.expires_at == None) | (models.RateLimit.expires_at > now)
    ).all()

    for rule in rules:
        start_time = now - timedelta(seconds=rule.time_window)
        request_count = db.query(models.Request).filter(
            current_user_id == user_id,
            models.Request.endpoint == endpoint,
            models.Request.timestamp >= start_time
        ).count()

        if request_count >= rule.threshold:
            raise HTTPException(status_code=429, detail="Too many requests")

    return {"message": "Request allowed"}
