from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, oauth, utils
from ..database import get_db

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("", status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Vérification de l'utilisateur dans la base de données
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    
    # Vérification du mot de passe
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")
    
    # Créer le token d'accès
    access_token = oauth.create_access_token(data={"user_id": user.id})
    
    return {
        "access_token": access_token,
        "ok": True,
        "status": status.HTTP_200_OK,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }
