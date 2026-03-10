# PharmaManager

Application de gestion de pharmacie — Développé dans le cadre du test technique SMARTHOLOL

## Stack Technique

- **Backend** : Django 4.x + Django REST Framework + PostgreSQL
- **Frontend** : React.js (Vite)
- **Documentation API** : Swagger (drf-spectacular)

## Structure du Projet

```
farmacie/
├── backend/          # Application Django
├── frontend/         # Application React
└── README.md
```

## Installation Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configurer les variables
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json  # Données de test
python manage.py runserver
```

## Variables d'Environnement (.env)

```
DEBUG=True
SECRET_KEY=votre-secret-key
DB_NAME=pharma_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

## Installation Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Documentation API

Swagger UI disponible sur : http://localhost:8000/api/schema/swagger-ui/

## Fonctionnalités

### Gestion des Médicaments
- ✅ CRUD complet des médicaments
- ✅ Gestion du stock avec alertes automatiques
- ✅ Catégorisation des médicaments
- ✅ Soft delete

### Gestion des Ventes
- ✅ Création de ventes multi-lignes
- ✅ Déduction automatique du stock
- ✅ Annulation de vente avec réintégration du stock
- ✅ Historique des ventes

### Dashboard
- ✅ Statistiques en temps réel
- ✅ Alertes de stock bas
- ✅ Ventes du jour

## Technologies Utilisées

### Backend
- Django 4.x
- Django REST Framework
- PostgreSQL
- drf-spectacular (Swagger)
- python-decouple

### Frontend
- React 18
- Vite
- Axios
- React Router
- Tailwind CSS (ou autre framework CSS)

## Développé par

SMARTHOLOL — Équipe Technique  
AI Solutions | Automation | Custom Development

---

© 2026 SMARTHOLOL — Tous droits réservés
