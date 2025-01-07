from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schéma pour créer une règle
class RateLimitCreate(BaseModel):
    user_id: Optional[int] = None
    threshold: int
    endpoint: Optional[str] = None
    time_window: int = 60
    expires_at: Optional[datetime] = None

# Schéma pour mettre à jour une règle
class RateLimitUpdate(BaseModel):
    user_id: Optional[int] = None
    threshold: Optional[int] = None
    endpoint: Optional[str] = None
    time_window: Optional[int] = None
    expires_at: Optional[datetime] = None