# Guide d'utilisation Swagger UI - PharmaManager

## Introduction

Swagger UI est une interface interactive qui permet d'explorer, tester et comprendre l'API PharmaManager sans écrire de code. Cette documentation vous guide dans l'utilisation de Swagger pour tester l'API.

---

## Accès à Swagger UI

### URL d'accès
```
http://localhost:8000/api/schema/swagger-ui/
```

### Première visite
1. Ouvrez votre navigateur web
2. Accédez à l'URL ci-dessus
3. L'interface Swagger UI s'affiche avec tous les endpoints disponibles

---

## Interface Swagger UI

### Structure de l'interface

```
┌─────────────────────────────────────────────────┐
│  PharmaManager API - Version 1.0.0              │
│  API de gestion de pharmacie                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  ▼ categories                                   │
│     GET    /api/v1/categories/                  │
│     POST   /api/v1/categories/                  │
│     GET    /api/v1/categories/{id}/             │
│     PUT    /api/v1/categories/{id}/             │
│     PATCH  /api/v1/categories/{id}/             │
│     DELETE /api/v1/categories/{id}/             │
│                                                 │
│  ▼ medicaments                                  │
│     GET    /api/v1/medicaments/                 │
│     POST   /api/v1/medicaments/                 │
│     ...                                         │
│                                                 │
│  ▼ ventes                                       │
│     ...                                         │
│                                                 │
│  ▼ Schemas                                      │
│     Categorie                                   │
│     Medicament                                  │
│     Vente                                       │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Éléments de l'interface

1. **En-tête**: Titre et description de l'API
2. **Groupes d'endpoints**: Organisés par ressource (categories, medicaments, ventes)
3. **Méthodes HTTP**: GET (bleu), POST (vert), PUT (orange), PATCH (violet), DELETE (rouge)
4. **Schémas**: Modèles de données au bas de la page

---

## Tester un endpoint GET

### Exemple: Récupérer la liste des médicaments

#### Étape 1: Localiser l'endpoint
1. Faites défiler jusqu'à la section `medicaments`
2. Trouvez `GET /api/v1/medicaments/`

#### Étape 2: Ouvrir l'endpoint
1. Cliquez sur la ligne pour déplier les détails
2. Vous verrez:
   - Description de l'endpoint
   - Paramètres disponibles
   - Exemple de réponse

#### Étape 3: Tester l'endpoint
1. Cliquez sur le bouton **"Try it out"** (en haut à droite)
2. Les paramètres deviennent éditables
3. Ajoutez des paramètres optionnels si nécessaire:
   ```
   search: paracetamol
   ordering: -date_creation
   page: 1
   ```
4. Cliquez sur **"Execute"**

#### Étape 4: Voir les résultats
La page affiche:
- **Request URL**: L'URL complète de la requête
  ```
  http://localhost:8000/api/v1/medicaments/?search=paracetamol&ordering=-date_creation
  ```
- **Server response**: Le code de statut (200 OK)
- **Response body**: Les données JSON retournées
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "nom": "Paracétamol 500mg",
        "prix_vente": "8.00",
        ...
      }
    ]
  }
  ```
- **Response headers**: Les en-têtes HTTP

---

## Tester un endpoint POST

### Exemple: Créer un nouveau médicament

#### Étape 1: Ouvrir l'endpoint POST
1. Localisez `POST /api/v1/medicaments/`
2. Cliquez pour déplier

#### Étape 2: Activer le mode test
1. Cliquez sur **"Try it out"**
2. Un éditeur JSON apparaît avec un exemple de données

#### Étape 3: Remplir les données
Modifiez le JSON dans l'éditeur:
```json
{
  "nom": "Aspirine 500mg",
  "dci": "Acide acétylsalicylique",
  "categorie": 1,
  "forme": "comprime",
  "dosage": "500mg",
  "prix_achat": "4.50",
  "prix_vente": "7.50",
  "stock_actuel": 150,
  "stock_minimum": 50,
  "date_expiration": "2027-12-31",
  "ordonnance_requise": false
}
```

#### Étape 4: Envoyer la requête
1. Cliquez sur **"Execute"**
2. Vérifiez la réponse:
   - **201 Created**: Succès
   - Le corps de la réponse contient le médicament créé avec son ID

#### Étape 5: Gérer les erreurs
Si vous recevez **400 Bad Request**, le corps de la réponse indique les erreurs:
```json
{
  "nom": ["Ce champ est obligatoire."],
  "prix_achat": ["Assurez-vous que cette valeur est supérieure ou égale à 0."]
}
```

---

## Tester un endpoint avec paramètres d'URL

### Exemple: Récupérer un médicament spécifique

#### Étape 1: Ouvrir l'endpoint
1. Localisez `GET /api/v1/medicaments/{id}/`
2. Cliquez pour déplier

#### Étape 2: Spécifier l'ID
1. Cliquez sur **"Try it out"**
2. Dans le champ `id`, entrez: `1`

#### Étape 3: Exécuter
1. Cliquez sur **"Execute"**
2. Vous obtenez les détails complets du médicament ID 1

---

## Tester des actions personnalisées

### Exemple 1: Médicaments en alerte de stock

```
GET /api/v1/medicaments/alertes_stock/
```

1. Ouvrir l'endpoint
2. Cliquer sur "Try it out"
3. Cliquer sur "Execute"
4. Voir la liste des médicaments dont le stock est inférieur au minimum

### Exemple 2: Valider une vente

```
POST /api/v1/ventes/{id}/valider/
```

1. Ouvrir l'endpoint
2. Entrer l'ID d'une vente en cours: `1`
3. Cliquer sur "Try it out"
4. Cliquer sur "Execute"
5. La vente passe au statut "completee"

### Exemple 3: Ajuster le stock d'un médicament

```
PATCH /api/v1/medicaments/{id}/ajuster_stock/
```

1. Ouvrir l'endpoint
2. Entrer l'ID du médicament: `1`
3. Dans le corps de la requête:
   ```json
   {
     "quantite": -5,
     "operation": "vente"
   }
   ```
4. Exécuter
5. Le stock est diminué de 5 unités

---

## Utiliser les filtres

### Exemple: Filtrer les médicaments

Pour `GET /api/v1/medicaments/`, plusieurs paramètres sont disponibles:

| Paramètre | Type | Description | Exemple |
|-----------|------|-------------|---------|
| search | string | Recherche dans nom et DCI | `paracetamol` |
| categorie | integer | ID de catégorie | `1` |
| forme | string | Forme galénique | `comprime` |
| stock_alerte | boolean | Médicaments en alerte | `true` |
| ordonnance_requise | boolean | Nécessite ordonnance | `true` |
| ordering | string | Champ de tri | `-prix_vente` |
| page | integer | Numéro de page | `2` |

**Test combiné:**
```
search: para
categorie: 1
stock_alerte: true
ordering: stock_actuel
```

Résultat: Tous les médicaments antalgiques contenant "para" en alerte de stock, triés par stock croissant.

---

## Comprendre les schémas

### Accéder aux schémas
1. Faites défiler jusqu'à la section **"Schemas"** en bas de la page
2. Cliquez sur un schéma (ex: `Medicament`)

### Informations du schéma
- **Propriétés**: Liste de tous les champs
- **Type**: Type de données (string, integer, boolean, etc.)
- **Format**: Format spécifique (date, decimal, etc.)
- **Required**: Champs obligatoires marqués avec *
- **Validations**: Min/max, pattern, etc.

### Exemple de schéma Medicament
```
Medicament {
  id*            integer($int64)         readOnly: true
  nom*           string                  maxLength: 200
  dci*           string                  maxLength: 200
  categorie*     integer                 
  forme*         string                  enum: [comprime, sirop, ...]
  dosage*        string                  maxLength: 50
  prix_achat*    string($decimal)        format: decimal
  prix_vente*    string($decimal)        format: decimal
  stock_actuel*  integer                 minimum: 0
  stock_minimum* integer                 minimum: 0
  date_expiration* string($date)        format: date
  ordonnance_requise boolean            default: false
  est_actif      boolean                 default: true
  date_creation  string($date-time)      readOnly: true
}
```

---

## Télécharger le schéma OpenAPI

### Format JSON
```
http://localhost:8000/api/schema/?format=json
```

### Format YAML
```
http://localhost:8000/api/schema/?format=yaml
```

### Utilisation
- Import dans Postman
- Génération de clients API
- Documentation externe
- Tests automatisés

---

## Cas d'usage pratiques

### 1. Vérifier les médicaments à réapprovisionner

**Endpoint:** `GET /api/v1/medicaments/alertes_stock/`

1. Ouvrir l'endpoint
2. Exécuter
3. Obtenir la liste des médicaments à commander

### 2. Créer une vente complète

**Endpoint:** `POST /api/v1/ventes/`

```json
{
  "notes": "Client régulier - Remise appliquée",
  "lignes": [
    {
      "medicament": 1,
      "quantite": 2,
      "prix_unitaire": "8.00"
    },
    {
      "medicament": 3,
      "quantite": 1,
      "prix_unitaire": "25.00"
    }
  ]
}
```

### 3. Consulter les statistiques du jour

**Endpoint:** `GET /api/v1/ventes/statistiques/`

1. Exécuter l'endpoint
2. Voir:
   - Total des ventes du jour
   - Nombre de transactions
   - Ventes du mois
   - Répartition par statut

### 4. Rechercher un médicament par DCI

**Endpoint:** `GET /api/v1/medicaments/`

**Paramètres:**
```
search: ibuprofene
```

Résultat: Tous les médicaments contenant "ibuprofene" dans le nom ou la DCI.

---

## Conseils et astuces

### 1. Mode clair/sombre
- Utilisez l'icône en haut à droite pour changer le thème
- Le mode sombre est plus confortable pour les yeux

### 2. Copier les requêtes cURL
- Après avoir exécuté une requête
- Trouvez la section "Curl"
- Copiez la commande pour l'utiliser dans un terminal

### 3. Autorisation (si implémenté)
- Cliquez sur le bouton "Authorize" en haut
- Entrez vos credentials ou token
- Toutes les requêtes suivantes incluront l'authentification

### 4. Réinitialiser les paramètres
- Cliquez sur "Clear" pour vider un formulaire
- Rechargez la page pour réinitialiser complètement

### 5. Consulter les exemples
- Chaque endpoint affiche un exemple de réponse
- Utilisez "Example Value" vs "Schema" pour basculer la vue

---

## Dépannage

### Problème: "Failed to fetch"
**Causes:**
- Le serveur backend n'est pas démarré
- CORS non configuré correctement

**Solutions:**
1. Vérifier que le backend tourne: `docker ps`
2. Redémarrer les containers: `docker compose restart backend`

### Problème: 404 Not Found
**Causes:**
- URL incorrecte
- Ressource supprimée

**Solutions:**
- Vérifier l'URL dans la requête
- Utiliser un ID existant

### Problème: 400 Bad Request
**Causes:**
- Données invalides
- Champs requis manquants

**Solutions:**
- Lire les messages d'erreur dans la réponse
- Vérifier le schéma pour les champs obligatoires
- Respecter les types de données

### Problème: 500 Internal Server Error
**Causes:**
- Erreur serveur
- Bug dans l'API

**Solutions:**
- Consulter les logs backend: `docker logs pharma_backend`
- Contacter l'équipe de développement

---

## Workflows recommandés

### Workflow 1: Gestion quotidienne des stocks
1. `GET /api/v1/medicaments/alertes_stock/` - Médicaments à commander
2. `GET /api/v1/medicaments/expiration_proche/` - Médicaments à surveiller
3. `PATCH /api/v1/medicaments/{id}/ajuster_stock/` - Ajuster le stock après inventaire

### Workflow 2: Processus de vente
1. `GET /api/v1/medicaments/?search=...` - Rechercher le médicament
2. `POST /api/v1/ventes/` - Créer la vente
3. `POST /api/v1/ventes/{id}/valider/` - Valider la vente
4. `GET /api/v1/ventes/statistiques/` - Voir les stats

### Workflow 3: Ajout de nouveau stock
1. `GET /api/v1/categories/` - Lister les catégories
2. `POST /api/v1/medicaments/` - Ajouter les nouveaux médicaments
3. `GET /api/v1/medicaments/?ordering=-date_creation` - Vérifier les ajouts

---

## Ressources supplémentaires

### Documentation officielle
- **Swagger UI**: https://swagger.io/tools/swagger-ui/
- **OpenAPI 3.0**: https://swagger.io/specification/

### Vidéos tutoriels
- Swagger UI Basics (YouTube)
- Testing APIs with Swagger

### Support
Pour toute question, consultez la documentation complète dans `docs/API.md` ou contactez l'équipe technique.

---

**Version**: 1.0.0  
**Dernière mise à jour**: Mars 2026  
**Prérequis**: Backend démarré sur http://localhost:8000
