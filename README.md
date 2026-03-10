# PharmaManager

Application de gestion de pharmacie — Développé dans le cadre du test technique SMARTHOLOL

## 🚀 Stack Technique

- **Backend** : Django 4.x + Django REST Framework + PostgreSQL
- **Frontend** : React.js (Vite) + React Router + Axios
- **Documentation API** : Swagger (drf-spectacular)
- **Containerisation** : Docker + Docker Compose

## 📁 Structure du Projet

```
farmacie/
├── backend/              # Application Django
│   ├── categories/       # App catégories
│   ├── medicaments/      # App médicaments
│   ├── ventes/          # App ventes
│   ├── config/          # Configuration Django
│   ├── fixtures/        # Données de test
│   ├── Dockerfile       # Docker backend
│   └── requirements.txt
├── frontend/            # Application React
│   ├── src/
│   │   ├── api/         # Couche API
│   │   ├── pages/       # Pages de l'application
│   │   └── App.jsx      # Composant principal
│   ├── Dockerfile       # Docker frontend
│   └── package.json
├── docker-compose.yml   # Orchestration Docker
└── README.md

```

## 🐳 Installation avec Docker (Recommandé)

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

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes (données)
docker-compose down -v

# Redémarrer un service spécifique
docker-compose restart backend

# Exécuter des commandes dans un conteneur
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py createsuperuser
```

## 💻 Installation Manuelle (sans Docker)

### Backend

```bash
cd backend

# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres PostgreSQL

# Créer la base de données PostgreSQL
createdb pharma_db

# Effectuer les migrations
python manage.py makemigrations
python manage.py migrate

# Charger les données de test
python manage.py loaddata fixtures/initial_data.json

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Configurer les variables d'environnement
cp .env.example .env

# Lancer le serveur de développement
npm run dev
```

## 🔧 Variables d'Environnement

### Backend (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=pharma_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost         # ou 'db' avec Docker
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 📚 Documentation API

La documentation Swagger est disponible sur : **http://localhost:8000/api/schema/swagger-ui/**

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

## ✨ Fonctionnalités

### Gestion des Médicaments
- ✅ CRUD complet des médicaments
- ✅ Gestion du stock avec alertes automatiques
- ✅ Catégorisation des médicaments
- ✅ Soft delete
- ✅ Recherche et filtrage
- ✅ Suivi des dates d'expiration

### Gestion des Ventes
- ✅ Création de ventes multi-lignes
- ✅ Déduction automatique du stock
- ✅ Annulation de vente avec réintégration du stock
- ✅ Historique des ventes avec filtres
- ✅ Génération automatique de références

### Dashboard
- ✅ Statistiques en temps réel
- ✅ Alertes de stock bas
- ✅ Ventes du jour
- ✅ Vue d'ensemble de l'activité

## 🏗️ Architecture

### Backend - Clean Code Practices

- **Modèles** : Docstrings complets, propriétés calculées, validations
- **Serializers** : Validation métier, nested serializers
- **ViewSets** : DRF ViewSets avec actions personnalisées
- **Admin** : Interface admin configurée avec inlines
- **Swagger** : Documentation complète avec @extend_schema

### Frontend - Structure claire

- **API Layer** : Séparation claire dans `src/api/`
- **Pages** : Composants de page dans `src/pages/`
- **Gestion d'état** : React hooks (useState, useEffect)
- **Gestion d'erreurs** : Try/catch avec messages utilisateur

## 🧪 Données de Test

Les fixtures incluent:
- 4 catégories de médicaments
- 5 médicaments avec différents stocks (dont 2 en alerte)

Pour charger les données:
```bash
python manage.py loaddata fixtures/initial_data.json
```

## 📝 Commits Git

Le projet suit les conventions Conventional Commits:

```bash
feat: add medicament list endpoint
fix: correct stock update on sale cancellation
docs: add swagger schemas
refactor: extract stock validation
chore: update gitignore
```

## 🔐 Accès Admin

Avec Docker, un superuser est créé automatiquement:
- **Username**: admin
- **Password**: admin123

Sans Docker, créez-le avec:
```bash
python manage.py createsuperuser
```

## 🛠️ Technologies Utilisées

### Backend
- Django 6.0
- Django REST Framework
- PostgreSQL
- drf-spectacular (Swagger)
- python-decouple
- django-cors-headers

### Frontend
- React 18
- Vite
- Axios
- React Router 6

### DevOps
- Docker
- Docker Compose
- PostgreSQL (Alpine)

## 📧 Support

Développé par **SMARTHOLOL** — Équipe Technique  
AI Solutions | Automation | Custom Development

---

© 2026 SMARTHOLOL — Tous droits réservés
