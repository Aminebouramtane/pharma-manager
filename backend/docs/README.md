# Documentation PharmaManager Backend

Bienvenue dans la documentation technique du backend PharmaManager.

## Structure de la documentation

### [API.md](./API.md)
Documentation complète de l'API REST:
- Exigences et standards API
- Liste des endpoints disponibles
- Formats de requête/réponse
- Gestion des erreurs
- Exemples de code (cURL, JavaScript, Python)
- Bonnes pratiques

### [SWAGGER_GUIDE.md](./SWAGGER_GUIDE.md)
Guide d'utilisation de Swagger UI:
- Accès à l'interface Swagger
- Tester les endpoints interactivement
- Comprendre les schémas de données
- Workflows recommandés
- Dépannage

## Démarrage rapide

### 1. Accéder à l'API
```
Base URL: http://localhost:8000/api/v1/
```

### 2. Explorer avec Swagger
```
Swagger UI: http://localhost:8000/api/schema/swagger-ui/
```

### 3. Premier test
```bash
# Récupérer la liste des catégories
curl http://localhost:8000/api/v1/categories/
```

## Endpoints principaux

| Ressource | Endpoint | Description |
|-----------|----------|-------------|
| Catégories | `/api/v1/categories/` | Gestion des catégories de médicaments |
| Médicaments | `/api/v1/medicaments/` | Gestion de l'inventaire |
| Ventes | `/api/v1/ventes/` | Gestion des transactions |

## Authentification

**Statut actuel**: Aucune authentification requise (environnement de développement)

**À venir**: 
- Token-based authentication (JWT)
- Permissions par rôle (admin, pharmacien, caissier)

## Technologies utilisées

- **Framework**: Django 6.0.3
- **API**: Django REST Framework 3.16.1
- **Documentation**: drf-spectacular 0.28.0
- **Base de données**: PostgreSQL 15
- **Conteneurisation**: Docker

## Structure du projet

```
backend/
├── config/                 # Configuration Django
│   ├── settings/
│   │   ├── base.py        # Settings communs
│   │   └── local.py       # Settings de développement
│   ├── urls.py            # URLs racine
│   └── wsgi.py
├── apps/                  # Applications Django
│   ├── categories/        # App catégories
│   ├── medicaments/       # App médicaments
│   └── ventes/           # App ventes
├── docs/                  # Documentation
├── fixtures/              # Données initiales
└── requirements.txt
```

## Support

### Documentation en ligne
- [API.md](./API.md) - Documentation API complète
- [SWAGGER_GUIDE.md](./SWAGGER_GUIDE.md) - Guide Swagger UI

### Liens utiles
- **Django**: https://docs.djangoproject.com/
- **DRF**: https://www.django-rest-framework.org/
- **PostgreSQL**: https://www.postgresql.org/docs/

### Contact
Pour toute question ou problème:
- Ouvrir une issue sur le repository
- Contacter l'équipe SMARTHOLOL

---

**Dernière mise à jour**: Mars 2026  
**Version API**: 1.0.0
