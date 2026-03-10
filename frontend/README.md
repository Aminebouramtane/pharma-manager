# PharmaManager Frontend

Frontend React + Vite pour l'application de gestion de pharmacie.

## Technologies

- React 18
- Vite 7.3
- React Router 6
- Axios
- React Icons
- React Toastify

## Installation avec Docker

Le frontend est conteneurisé et s'exécute automatiquement avec Docker Compose.

```bash
# Depuis la racine du projet
docker-compose up -d frontend

# Voir les logs
docker-compose logs -f frontend

# Rebuild après modifications
docker-compose build frontend
docker-compose up -d frontend
```

L'application sera accessible sur: http://localhost:5173

## Structure du projet

```
frontend/
├── src/
│   ├── api/              # Couche API
│   │   ├── categoriesApi.js
│   │   ├── medicamentsApi.js
│   │   └── ventesApi.js
│   ├── pages/            # Pages de l'application
│   │   ├── DashboardPage.jsx
│   │   ├── MedicamentsPage.jsx
│   │   └── VentesPage.jsx
│   ├── App.jsx           # Composant principal
│   ├── App.css           # Styles globaux
│   └── main.jsx          # Point d'entrée
├── Dockerfile            # Configuration Docker
├── package.json
└── vite.config.js
```

## Variables d'environnement

Configurées automatiquement dans docker-compose.yml:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Fonctionnalités

### Dashboard
- Statistiques en temps réel
- Alertes de stock bas
- Ventes du jour
- Médicaments proches de l'expiration

### Gestion des Médicaments
- Liste avec filtres et recherche
- Création de nouveaux médicaments
- Modification des informations
- Suppression avec confirmation toast
- Alertes visuelles pour stocks bas

### Gestion des Ventes
- Panier d'achat interactif
- Sélection de médicaments
- Calcul automatique du total
- Historique des ventes
- Annulation avec confirmation toast

## Commandes Docker utiles

```bash
# Rebuild après ajout de dépendances
docker-compose build frontend

# Redémarrer le service
docker-compose restart frontend

# Voir les logs en temps réel
docker-compose logs -f frontend

# Accéder au shell du conteneur
docker-compose exec frontend sh

# Installer une nouvelle dépendance (puis rebuild)
docker-compose exec frontend npm install <package>
```

## Développement

Le hot reload est activé dans Docker, les modifications du code sont reflétées automatiquement.

## API Backend

L'application communique avec le backend Django via Axios.
Base URL configurée: `http://localhost:8000/api/v1`

Documentation API complète: `backend/docs/API.md`

