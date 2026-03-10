# PharmaManager Backend

Backend Django REST API pour la gestion de pharmacie - Architecture conforme aux spécifications SMARTHOLOL.

## Documentation

### Documentation complète disponible dans `/docs/`:
- **[docs/README.md](./docs/README.md)** - Index de la documentation
- **[docs/API.md](./docs/API.md)** - Documentation API complète avec exemples
- **[docs/SWAGGER_GUIDE.md](./docs/SWAGGER_GUIDE.md)** - Guide d'utilisation Swagger UI

### Accès rapide:
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **Schéma OpenAPI**: http://localhost:8000/api/schema/
- **Admin Django**: http://localhost:8000/admin/ (admin/admin123)

## Installation avec Docker

Le backend est conteneurisé et s'exécute automatiquement avec Docker Compose.

```bash
# Depuis la racine du projet
docker-compose up -d backend

# Voir les logs
docker-compose logs -f backend

# Exécuter des commandes Django
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json
```

## Structure du projet (Architecture SMARTHOLOL)

```
backend/
├── config/                    # Dossier de configuration du projet
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py           # Settings communs
│   │   └── local.py          # Settings de développement
│   ├── urls.py               # URLs racine + Swagger
│   ├── wsgi.py
│   └── asgi.py
├── apps/                      # Applications Django
│   ├── __init__.py
│   ├── categories/           # App catégories
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── medicaments/          # App médicaments
│   │   ├── models.py         # Modèle Medicament
│   │   ├── serializers.py    # Serializers avec validation
│   │   ├── views.py          # ViewSet avec actions
│   │   ├── urls.py
│   │   └── admin.py
│   └── ventes/               # App ventes
│       ├── models.py         # Modèles Vente et LigneVente
│       ├── serializers.py    # Logic métier de vente
│       ├── views.py          # ViewSet avec actions
│       ├── urls.py
│       └── admin.py
├── docs/                      # Documentation
│   ├── README.md             # Index documentation
│   ├── API.md                # Documentation API complète
│   └── SWAGGER_GUIDE.md      # Guide Swagger
├── fixtures/                  # Données de test
│   └── initial_data.json
├── Dockerfile                 # Configuration Docker
├── requirements.txt           # Dépendances Python
├── manage.py
└── .env.example
```

## API Endpoints

Base URL: `http://localhost:8000/api/v1/`

**Documentation complète**: Voir [docs/API.md](./docs/API.md) pour tous les détails, exemples et cas d'usage.

### Catégories
- `GET /api/v1/categories/` - Liste des catégories
- `POST /api/v1/categories/` - Créer une catégorie
- `GET /api/v1/categories/{id}/` - Détail d'une catégorie
- `PUT/PATCH /api/v1/categories/{id}/` - Modifier une catégorie
- `DELETE /api/v1/categories/{id}/` - Supprimer une catégorie

### Médicaments
- `GET /api/v1/medicaments/` - Liste paginée avec filtres
- `POST /api/v1/medicaments/` - Créer un médicament
- `GET /api/v1/medicaments/{id}/` - Détail d'un médicament
- `PUT/PATCH /api/v1/medicaments/{id}/` - Modifier un médicament
- `DELETE /api/v1/medicaments/{id}/` - Archiver (soft delete)
- `GET /api/v1/medicaments/alertes_stock/` - Médicaments en alerte
- `GET /api/v1/medicaments/expires/` - Médicaments expirés
- `GET /api/v1/medicaments/expiration_proche/` - Expiration < 30 jours
- `PATCH /api/v1/medicaments/{id}/ajuster_stock/` - Ajuster le stock
- `POST /api/v1/medicaments/{id}/archiver/` - Archiver

### Ventes
- `GET /api/v1/ventes/` - Historique des ventes
- `POST /api/v1/ventes/` - Créer une vente
- `GET /api/v1/ventes/{id}/` - Détail d'une vente
- `POST /api/v1/ventes/{id}/valider/` - Valider une vente
- `POST /api/v1/ventes/{id}/annuler/` - Annuler une vente
- `GET /api/v1/ventes/statistiques/` - Statistiques des ventes

## Documentation Swagger

**Interface interactive**: http://localhost:8000/api/schema/swagger-ui/

### Fonctionnalités
- Explorer tous les endpoints de l'API
- Tester les requêtes directement depuis le navigateur
- Consulter les schémas de données
- Télécharger le schéma OpenAPI (JSON/YAML)

**Guide complet**: Voir [docs/SWAGGER_GUIDE.md](./docs/SWAGGER_GUIDE.md) pour apprendre à utiliser Swagger UI.

## Variables d'environnement

Configurées automatiquement dans docker-compose.yml. Pour les modifier:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=pharma_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db                    # 'db' pour Docker, 'localhost' pour local
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Commandes Docker utiles

```bash
# Rebuild le backend
docker-compose build backend

# Redémarrer le backend
docker-compose restart backend

# Voir les logs en temps réel
docker-compose logs -f backend

# Créer des migrations
docker-compose exec backend python manage.py makemigrations

# Appliquer les migrations
docker-compose exec backend python manage.py migrate

# Créer un superuser
docker-compose exec backend python manage.py createsuperuser

# Charger les fixtures
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json

# Accéder au shell Django
docker-compose exec backend python manage.py shell

# Accéder au shell du conteneur
docker-compose exec backend sh
```

## Tests

```bash
# Avec Docker
docker-compose exec backend python manage.py test
```

