from fastapi import Depends, HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth
from ..schemas import user_schema
from ..database import get_db
from ..utils import hash


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOutput)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    if not new_user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {user.email}   exist already")
    return new_user


@router.get("", response_model=list[user_schema.UserOutput])
def get_user(current_user: int = Depends(oauth.get_current_user)
             , db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.is_active == True).all()
    if users:
        return users
    else:
        return []
    
    
