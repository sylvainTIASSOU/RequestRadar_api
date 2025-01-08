# FastAPI Dashboard Project

## Description

Ce projet est une API FastAPI qui simule des requêtes API, recueille des métriques et les expose à une interface utilisateur (UI). Il inclut des fonctionnalités de gestion des limites de débit (rate-limiting), de suivi des erreurs, et d'analyse des performances des API. Le projet inclut également une interface frontend qui consomme les données de l'API pour visualiser les métriques sous forme de graphiques interactifs en utilisant shadcn chart.

## Fonctionnalités

- Simule des requêtes API (GET, POST, PUT, DELETE).
- Collecte des métriques telles que le temps de réponse, les tailles de requêtes et de réponses, et le taux d'erreur.
- Met en œuvre un système de rate-limiting pour chaque utilisateur.
- Expose une API pour récupérer les données de performance en temps réel.
- Visualisation des données sur un tableau de bord frontend avec des graphiques de type "line" et "pie".

## Prérequis

- Python 3.12.6 ou version ultérieure
- Node.js (pour le frontend)
- Une base de données PostgreSQL 

## Installation

### Backend (FastAPI)

1. Clonez ce projet depuis le dépôt GitHub :

   ```bash
   git clone https://github.com/sylvainTIASSOU/RequestRadar_api.git
   cd fastapi-dashboard
