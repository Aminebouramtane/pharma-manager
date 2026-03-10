# PharmaManager Backend

Backend Django REST API pour la gestion de pharmacie.

## Installation locale

```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

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

## Structure du projet

```
backend/
├── config/              # Configuration Django
│   ├── settings.py      # Settings avec decouple
│   ├── urls.py          # URLs racine + Swagger
│   └── wsgi.py
├── categories/          # App catégories
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── medicaments/         # App médicaments
│   ├── models.py        # Modèle Medicament
│   ├── serializers.py   # Serializers avec validation
│   ├── views.py         # ViewSet avec action alertes
│   ├── urls.py
│   └── admin.py
├── ventes/              # App ventes
│   ├── models.py        # Modèles Vente et LigneVente
│   ├── serializers.py   # Logic métier de vente
│   ├── views.py         # ViewSet avec action annuler
│   ├── urls.py
│   └── admin.py
├── fixtures/            # Données de test
│   └── initial_data.json
├── requirements.txt
├── .env.example
└── manage.py
```

## API Endpoints

### Médicaments

- `GET /api/v1/medicaments/` - Liste paginée
- `POST /api/v1/medicaments/` - Créer
- `GET /api/v1/medicaments/{id}/` - Détail
- `PUT/PATCH /api/v1/medicaments/{id}/` - Modifier
- `DELETE /api/v1/medicaments/{id}/` - Soft delete
- `GET /api/v1/medicaments/alertes/` - Alertes de stock

### Catégories

- `GET /api/v1/categories/` - Liste
- `POST /api/v1/categories/` - Créer
- `GET /api/v1/categories/{id}/` - Détail
- `PUT/PATCH /api/v1/categories/{id}/` - Modifier
- `DELETE /api/v1/categories/{id}/` - Supprimer

### Ventes

- `GET /api/v1/ventes/` - Historique
- `POST /api/v1/ventes/` - Créer vente
- `GET /api/v1/ventes/{id}/` - Détail
- `POST /api/v1/ventes/{id}/annuler/` - Annuler

## Documentation Swagger

Accessible sur: http://localhost:8000/api/schema/swagger-ui/

## Tests

```bash
python manage.py test
```

## Variables d'environnement

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=pharma_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Commandes utiles

```bash
# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Charger les fixtures
python manage.py loaddata fixtures/initial_data.json

# Lancer le shell Django
python manage.py shell

# Collecter les fichiers statiques
python manage.py collectstatic
```
