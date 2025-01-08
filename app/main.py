from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .database import engine
from . import models
# import random
# import time

from .routes import (user, login, mock, analytics, rate_limit)

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="API FastAPI with JWT for RequestRadar project", 
    description="API description",
    version="0.0.1",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations about users",
        },
        {
            "name": "Login",
            "description": "Endpoint pour l'authentification des utilisateurs",
        },
        {
            "name": "Mock",
            "description": "Endpoint pour lancer la simulation et la recolte des requettes qui s'execute en arriere plan",
        },
        
        {
             "name": "metric",
            "description": "Operations about metrics",
        }
           
        
        
    ]
)
#desactier le docs en production
#app = FastAPI(docs_url=None, redoc_url=None)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Ajout du middleware pour gérer les hôtes de confiance
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(login.router)
app.include_router(user.router)
app.include_router(mock.router)
app.include_router(analytics.router)
app.include_router(rate_limit.router)





