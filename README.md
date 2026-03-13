# PharmaManager 

Application de gestion de pharmacie - Développé dans le cadre du test technique SMARTHOLOL

## Stack Technique

- **Backend** : Django 4.x + Django REST Framework + PostgreSQL
- **Frontend** : React.js (Vite) + React Router + Axios
- **Documentation API** : Swagger (drf-spectacular)
- **Containerisation** : Docker + Docker Compose

## Structure du Projet

```
farmacie/
├── backend/                    # Application Django
│   ├── apps/                  # Applications Django
│   │   ├── __init__.py
│   │   ├── categories/        # Gestion des catégories
│   │   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── medicaments/       # Gestion des médicaments
│   │   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   └── ventes/            # Gestion des ventes
│   │       ├── migrations/
│   │       ├── __init__.py
│   │       ├── admin.py
│   │       ├── apps.py
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       └── views.py
│   ├── config/                # Configuration Django
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py       # Settings communs
│   │   │   └── local.py      # Settings développement
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── docs/                  # Documentation API
│   │   ├── API.md            # Documentation endpoints
│   │   ├── SWAGGER_GUIDE.md  # Guide Swagger
│   │   └── README.md         # Index documentation
│   ├── fixtures/              # Données de test
│   │   └── initial_data.json
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
├── frontend/                   # Application React
│   ├── public/
│   ├── src/
│   │   ├── api/               # Services API
│   │   │   ├── categoriesApi.js
│   │   │   ├── medicamentsApi.js
│   │   │   └── ventesApi.js
│   │   ├── pages/             # Pages React
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── MedicamentsPage.jsx
│   │   │   └── VentesPage.jsx
│   │   ├── App.css            # Styles globaux
│   │   ├── App.jsx            # Composant principal
│   │   └── main.jsx           # Point d'entrée
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── docker-compose.yml         # Orchestration Docker
└── README.md                  # Ce fichier

```

## Installation avec Docker

### Prérequis

- Docker et Docker Compose installés
- Ports 5432 (PostgreSQL), 8000 (Backend), 5173 (Frontend) disponibles

### Démarrage rapide

```bash
# Cloner le projet
git clone <url-du-repo>
cd farmacie

# Lancer tous les services avec Docker Compose
docker-compose up --build

# En arrière-plan:
docker-compose up -d --build
```

Attendez quelques secondes, puis accédez à:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/v1/
- **Swagger**: http://localhost:8000/api/schema/swagger-ui/
- **Admin Django**: http://localhost:8000/admin (admin/admin123)

### Commandes Docker utiles

```bash
# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f backend

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes (données)
docker-compose down -v

# Redémarrer un service spécifique
docker-compose restart backend

# Exécuter des commandes dans un conteneur
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json

# Rebuild un service spécifique
docker-compose build backend
docker-compose up -d backend
```

## Variables d'Environnement

Les variables d'environnement sont déjà configurées dans docker-compose.yml. 
Si vous voulez les modifier:

### Backend (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=pharma_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db                # 'db' pour Docker, 'localhost' pour local
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Documentation API

La documentation complète de l'API est disponible dans le dossier `backend/docs/`:
- **API Reference**: `backend/docs/API.md` - Documentation complète de tous les endpoints
- **Swagger Guide**: `backend/docs/SWAGGER_GUIDE.md` - Guide d'utilisation de Swagger UI
- **Swagger UI Live**: http://localhost:8000/api/schema/swagger-ui/

### Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/medicaments/` | Liste des médicaments |
| POST | `/api/v1/medicaments/` | Créer un médicament |
| GET | `/api/v1/medicaments/{id}/` | Détail d'un médicament |
| PUT/PATCH | `/api/v1/medicaments/{id}/` | Modifier un médicament |
| DELETE | `/api/v1/medicaments/{id}/` | Supprimer (soft delete) |
| GET | `/api/v1/medicaments/alertes/` | Médicaments en alerte |
| GET | `/api/v1/categories/` | Liste des catégories |
| POST | `/api/v1/categories/` | Créer une catégorie |
| GET | `/api/v1/ventes/` | Historique des ventes |
| POST | `/api/v1/ventes/` | Créer une vente |
| GET | `/api/v1/ventes/{id}/` | Détail d'une vente |
| POST | `/api/v1/ventes/{id}/annuler/` | Annuler une vente |

## Fonctionnalités

### Gestion des Médicaments
- CRUD complet des médicaments
- Gestion du stock avec alertes automatiques
- Catégorisation des médicaments
- Soft delete
- Recherche et filtrage
- Suivi des dates d'expiration

### Gestion des Ventes
- Création de ventes multi-lignes
- Déduction automatique du stock
- Annulation de vente avec réintégration du stock
- Historique des ventes avec filtres
- Génération automatique de références

### Dashboard
- Statistiques en temps réel
- Alertes de stock bas
- Ventes du jour
- Vue d'ensemble de l'activité

## Architecture

### Backend - Clean Code Practices

- **Modèles** : Docstrings complets, propriétés calculées, validations
- **Serializers** : Validation métier, nested serializers
- **ViewSets** : DRF ViewSets avec actions personnalisées
- **Admin** : Interface admin configurée avec inlines
- **Swagger** : Documentation complète avec @extend_schema
- **Structure** : Séparation config/ et apps/ selon best practices Django

### Frontend - Structure claire

- **API Layer** : Séparation claire dans `src/api/`
- **Pages** : Composants de page dans `src/pages/`
- **Gestion d'état** : React hooks (useState, useEffect)
- **Gestion d'erreurs** : Try/catch avec messages utilisateur
- **Notifications** : Toast notifications pour les actions importantes

## Données de Test

Les fixtures incluent:
- 4 catégories de médicaments
- 7 médicaments avec différents stocks (dont 2 en alerte)

Avec Docker, les données sont chargées automatiquement au démarrage.

Pour recharger les données manuellement:
```bash
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json
```

## Accès Admin

Avec Docker, un superuser est créé automatiquement:
- **Username**: admin
- **Password**: admin123

Pour créer un nouveau superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

## Technologies Utilisées

### Backend
- Django 6.0
- Django REST Framework 3.16
- PostgreSQL 15
- drf-spectacular (Swagger)
- python-decouple
- django-cors-headers

### Frontend
- React 18
- Vite 7.3
- Axios
- React Router 6
- React Icons
- React Toastify

### DevOps
- Docker
- Docker Compose
- PostgreSQL (Alpine)
- Python 3.13-slim
- Node 20-alpine

## Support

Développé par **SMARTHOLOL** - Équipe Technique  
AI Solutions | Automation | Custom Development

---

© 2026 SMARTHOLOL - Tous droits réservés

