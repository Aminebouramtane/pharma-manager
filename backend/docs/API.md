# Documentation API - PharmaManager

## Vue d'ensemble

L'API PharmaManager est une API RESTful construite avec Django REST Framework qui permet de gérer l'inventaire de médicaments et les ventes d'une pharmacie.

**Base URL**: `http://localhost:8000/api/v1/`

**Format de données**: JSON

**Protocole**: HTTP/HTTPS

---

## Exigences API

### Standards et Conventions

#### 1. Architecture REST
- **GET**: Récupération de données (liste ou détail)
- **POST**: Création de nouvelles ressources
- **PUT**: Mise à jour complète d'une ressource
- **PATCH**: Mise à jour partielle d'une ressource
- **DELETE**: Suppression d'une ressource

#### 2. Codes de statut HTTP
| Code | Signification | Usage |
|------|---------------|-------|
| 200 | OK | Requête réussie (GET, PUT, PATCH) |
| 201 | Created | Ressource créée avec succès (POST) |
| 204 | No Content | Suppression réussie (DELETE) |
| 400 | Bad Request | Données invalides |
| 404 | Not Found | Ressource introuvable |
| 500 | Internal Server Error | Erreur serveur |

#### 3. Format des réponses

**Succès avec pagination:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/v1/medicaments/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nom": "Paracétamol",
      ...
    }
  ]
}
```

**Erreur de validation:**
```json
{
  "field_name": [
    "Message d'erreur détaillé"
  ]
}
```

#### 4. Filtrage et recherche
- **Pagination**: `?page=2&page_size=20`
- **Recherche**: `?search=paracetamol`
- **Tri**: `?ordering=-date_creation`
- **Filtres**: `?categorie=1&stock_alerte=true`

---

## Documentation Interactive Swagger/OpenAPI

### Accès à l'interface Swagger

**URL Swagger UI**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

**URL Schéma OpenAPI**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

### Fonctionnalités Swagger

#### 1. Explorer les endpoints
L'interface Swagger UI permet de:
- Visualiser tous les endpoints disponibles
- Consulter les schémas de requête/réponse
- Tester les API directement depuis le navigateur
- Télécharger le schéma OpenAPI

#### 2. Tester les API
Pour chaque endpoint, vous pouvez:
1. Cliquer sur l'endpoint pour l'ouvrir
2. Cliquer sur "Try it out"
3. Remplir les paramètres requis
4. Cliquer sur "Execute"
5. Voir la réponse en temps réel

#### 3. Schémas de données
Swagger affiche automatiquement:
- Les champs requis et optionnels
- Les types de données attendus
- Les validations appliquées
- Les exemples de valeurs

---

## Endpoints Disponibles

### 1. Catégories (`/api/v1/categories/`)

#### Liste des catégories
```http
GET /api/v1/categories/
```

**Réponse:**
```json
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "nom": "Antalgique",
      "description": "Médicaments contre la douleur",
      "nombre_medicaments": 15,
      "date_creation": "2026-03-10T10:00:00Z"
    }
  ]
}
```

#### Créer une catégorie
```http
POST /api/v1/categories/
Content-Type: application/json

{
  "nom": "Antihistaminique",
  "description": "Médicaments contre les allergies"
}
```

#### Détail d'une catégorie
```http
GET /api/v1/categories/{id}/
```

#### Mettre à jour une catégorie
```http
PUT /api/v1/categories/{id}/
PATCH /api/v1/categories/{id}/
```

#### Supprimer une catégorie
```http
DELETE /api/v1/categories/{id}/
```

---

### 2. Médicaments (`/api/v1/medicaments/`)

#### Liste des médicaments
```http
GET /api/v1/medicaments/
```

**Paramètres de requête:**
- `search`: Recherche par nom ou DCI
- `categorie`: Filtrer par ID de catégorie
- `forme`: Filtrer par forme galénique
- `stock_alerte`: Médicaments en alerte de stock (`true`)
- `ordonnance_requise`: Filtrer par ordonnance
- `ordering`: Tri (`nom`, `-prix_vente`, `stock_actuel`)

**Exemples:**
```http
GET /api/v1/medicaments/?search=paracetamol
GET /api/v1/medicaments/?categorie=1&stock_alerte=true
GET /api/v1/medicaments/?ordering=-date_creation
```

**Réponse:**
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "nom": "Paracétamol 500mg",
      "dci": "Paracétamol",
      "categorie": 1,
      "categorie_nom": "Antalgique",
      "forme": "comprime",
      "dosage": "500mg",
      "prix_achat": "5.50",
      "prix_vente": "8.00",
      "stock_actuel": 150,
      "stock_minimum": 50,
      "date_expiration": "2027-12-31",
      "ordonnance_requise": false,
      "est_actif": true,
      "est_en_alerte": false,
      "date_creation": "2026-03-10T10:00:00Z"
    }
  ]
}
```

#### Créer un médicament
```http
POST /api/v1/medicaments/
Content-Type: application/json

{
  "nom": "Ibuprofène 400mg",
  "dci": "Ibuprofène",
  "categorie": 3,
  "forme": "comprime",
  "dosage": "400mg",
  "prix_achat": "12.00",
  "prix_vente": "18.50",
  "stock_actuel": 200,
  "stock_minimum": 50,
  "date_expiration": "2028-06-30",
  "ordonnance_requise": false
}
```

#### Actions personnalisées

**Médicaments en alerte de stock:**
```http
GET /api/v1/medicaments/alertes_stock/
```

**Médicaments expirés:**
```http
GET /api/v1/medicaments/expires/
```

**Médicaments arrivant à expiration (30 jours):**
```http
GET /api/v1/medicaments/expiration_proche/
```

**Mise à jour du stock:**
```http
PATCH /api/v1/medicaments/{id}/ajuster_stock/
Content-Type: application/json

{
  "quantite": -10,
  "operation": "vente"
}
```

**Archiver un médicament:**
```http
POST /api/v1/medicaments/{id}/archiver/
```

---

### 3. Ventes (`/api/v1/ventes/`)

#### Liste des ventes
```http
GET /api/v1/ventes/
```

**Paramètres de requête:**
- `statut`: Filtrer par statut (`en_cours`, `completee`, `annulee`)
- `date_debut`: Date de début (format: `YYYY-MM-DD`)
- `date_fin`: Date de fin
- `ordering`: Tri (`-date_vente`, `total_ttc`)

**Exemples:**
```http
GET /api/v1/ventes/?statut=completee
GET /api/v1/ventes/?date_debut=2026-03-01&date_fin=2026-03-10
```

**Réponse:**
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "reference": "VNT-2026-0001",
      "date_vente": "2026-03-10T14:30:00Z",
      "total_ttc": "45.50",
      "statut": "completee",
      "nombre_lignes": 3,
      "notes": "",
      "lignes": [
        {
          "id": 1,
          "medicament": 1,
          "medicament_nom": "Paracétamol 500mg",
          "quantite": 2,
          "prix_unitaire": "8.00",
          "sous_total": "16.00"
        }
      ]
    }
  ]
}
```

#### Créer une vente
```http
POST /api/v1/ventes/
Content-Type: application/json

{
  "notes": "Vente comptoir",
  "lignes": [
    {
      "medicament": 1,
      "quantite": 2,
      "prix_unitaire": "8.00"
    },
    {
      "medicament": 5,
      "quantite": 1,
      "prix_unitaire": "15.50"
    }
  ]
}
```

**Note:** La référence est générée automatiquement au format `VNT-{ANNÉE}-{NUMÉRO}`

#### Actions personnalisées

**Valider une vente:**
```http
POST /api/v1/ventes/{id}/valider/
```

**Annuler une vente:**
```http
POST /api/v1/ventes/{id}/annuler/
```

**Statistiques des ventes:**
```http
GET /api/v1/ventes/statistiques/
```

**Réponse:**
```json
{
  "total_ventes_jour": "245.50",
  "nombre_ventes_jour": 12,
  "total_ventes_mois": "5420.00",
  "nombre_ventes_mois": 156,
  "ventes_par_statut": {
    "completee": 145,
    "en_cours": 8,
    "annulee": 3
  }
}
```

---

## Gestion des erreurs

### Erreurs de validation

**Requête:**
```json
{
  "nom": "",
  "prix_achat": -5
}
```

**Réponse (400 Bad Request):**
```json
{
  "nom": ["Ce champ ne peut pas être vide."],
  "prix_achat": ["Assurez-vous que cette valeur est supérieure ou égale à 0."]
}
```

### Ressource introuvable

**Réponse (404 Not Found):**
```json
{
  "detail": "Aucun(e) Medicament correspondant(e) à la requête n'a été trouvé(e)."
}
```

### Erreur métier

**Exemple - Stock insuffisant:**
```json
{
  "detail": "Stock insuffisant pour le médicament Paracétamol 500mg. Stock disponible: 5"
}
```

---

## Exemples d'utilisation

### cURL

**Récupérer la liste des médicaments:**
```bash
curl -X GET "http://localhost:8000/api/v1/medicaments/" \
     -H "Accept: application/json"
```

**Créer un médicament:**
```bash
curl -X POST "http://localhost:8000/api/v1/medicaments/" \
     -H "Content-Type: application/json" \
     -d '{
       "nom": "Aspirine 100mg",
       "dci": "Acide acétylsalicylique",
       "categorie": 1,
       "forme": "comprime",
       "dosage": "100mg",
       "prix_achat": "3.50",
       "prix_vente": "6.00",
       "stock_actuel": 100,
       "stock_minimum": 30,
       "date_expiration": "2027-12-31",
       "ordonnance_requise": false
     }'
```

### JavaScript (Fetch)

```javascript
// Récupérer les médicaments en alerte
fetch('http://localhost:8000/api/v1/medicaments/alertes_stock/')
  .then(response => response.json())
  .then(data => {
    console.log('Médicaments en alerte:', data.results);
  })
  .catch(error => console.error('Erreur:', error));

// Créer une vente
fetch('http://localhost:8000/api/v1/ventes/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    notes: 'Vente client',
    lignes: [
      {
        medicament: 1,
        quantite: 2,
        prix_unitaire: '8.00'
      }
    ]
  })
})
  .then(response => response.json())
  .then(data => console.log('Vente créée:', data))
  .catch(error => console.error('Erreur:', error));
```

### Python (requests)

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
headers = {"Content-Type": "application/json"}

# Récupérer les statistiques
response = requests.get(f"{BASE_URL}/ventes/statistiques/")
stats = response.json()
print(f"Ventes du jour: {stats['total_ventes_jour']} MAD")

# Créer une catégorie
nouvelle_categorie = {
    "nom": "Dermatologie",
    "description": "Produits dermatologiques"
}
response = requests.post(
    f"{BASE_URL}/categories/",
    json=nouvelle_categorie,
    headers=headers
)
print(f"Catégorie créée: {response.json()}")
```

---

## Bonnes pratiques

### 1. Pagination
- Utiliser la pagination pour les listes volumineuses
- Ajuster `page_size` selon vos besoins (max: 100)

### 2. Filtrage
- Combiner les filtres pour des requêtes précises
- Utiliser la recherche pour les recherches textuelles

### 3. Gestion des erreurs
- Toujours vérifier le code de statut HTTP
- Parser les messages d'erreur pour un retour utilisateur clair

### 4. Performance
- Utiliser `?fields=` pour limiter les champs retournés (si implémenté)
- Mettre en cache les données peu changeantes (catégories)

### 5. Sécurité
- Valider les données côté client avant envoi
- Gérer les erreurs de manière appropriée
- Ne pas exposer d'informations sensibles dans les logs

---

## Configuration de la documentation

### DRF Spectacular Settings

La documentation est générée automatiquement avec [drf-spectacular](https://drf-spectacular.readthedocs.io/).

**Configuration dans `config/settings/base.py`:**
```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'PharmaManager API',
    'DESCRIPTION': 'API de gestion de pharmacie — Développé avec SMARTHOLOL standards',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}
```

### Personnalisation

Pour ajouter des descriptions détaillées aux endpoints, utilisez les docstrings dans les ViewSets:

```python
class MedicamentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les médicaments.
    
    list: Retourne la liste des médicaments avec pagination
    create: Crée un nouveau médicament
    retrieve: Retourne les détails d'un médicament
    update: Met à jour un médicament
    partial_update: Met à jour partiellement un médicament
    destroy: Supprime (archive) un médicament
    """
```

---

## Support et ressources

### Documentation technique
- **Django REST Framework**: https://www.django-rest-framework.org/
- **drf-spectacular**: https://drf-spectacular.readthedocs.io/
- **OpenAPI Specification**: https://swagger.io/specification/

### Contact
Pour toute question ou support technique, veuillez contacter l'équipe de développement SMARTHOLOL.

---

**Version**: 1.0.0  
**Dernière mise à jour**: Mars 2026  
**Environnement**: Développement
