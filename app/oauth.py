from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models
from .schemas import user_schema
from . database import get_db
import os
from dotenv import load_dotenv


load_dotenv()

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')
oauth2_schema2 = OAuth2PasswordBearer(tokenUrl='customer_authentification/login')


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

#secret_key
#algoritm
#expiration time

def create_customer_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        
        if id is None:
            raise credentials_exception
        token_data = user_schema.tokenData(id= id)
    except JWTError:
        raise credentials_exception

    return token_data

def verify_customer_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        customer_id: int = payload.get('customer_id')
        
        if customer_id is None:
            raise credentials_exception
        
        return customer_id
    except JWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"www-Authenticate": "Bearer"})
    
    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user 

def get_current_customer(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"www-Authenticate": "Bearer"}
    )
    
    # Récupérer l'ID du client depuis le token
    customer_id = verify_customer_access_token(token=token, credentials_exception=credentials_exception)
    
    # Rechercher le client dans la base de données avec cet ID
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    
    if customer is None:
        raise credentials_exception
    
    return customer