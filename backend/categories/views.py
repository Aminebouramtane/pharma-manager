"""
Views pour l'application categories.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Categorie
from .serializers import CategorieSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Liste des catégories",
        description="Récupère la liste de toutes les catégories de médicaments.",
        tags=['Catégories']
    ),
    create=extend_schema(
        summary="Créer une catégorie",
        description="Crée une nouvelle catégorie de médicaments.",
        tags=['Catégories']
    ),
    retrieve=extend_schema(
        summary="Détail d'une catégorie",
        description="Récupère les détails d'une catégorie spécifique.",
        tags=['Catégories']
    ),
    update=extend_schema(
        summary="Modifier une catégorie",
        description="Modifie complètement une catégorie existante.",
        tags=['Catégories']
    ),
    partial_update=extend_schema(
        summary="Modification partielle",
        description="Modifie partiellement une catégorie existante.",
        tags=['Catégories']
    ),
    destroy=extend_schema(
        summary="Supprimer une catégorie",
        description="Supprime une catégorie (uniquement si elle ne contient pas de médicaments).",
        tags=['Catégories']
    ),
)
class CategorieViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des catégories de médicaments.
    
    Fournit les opérations CRUD complètes sur les catégories.
    """
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    
    def destroy(self, request, *args, **kwargs):
        """
        Supprime une catégorie uniquement si elle ne contient pas de médicaments actifs.
        
        Args:
            request: Requête HTTP.
            
        Returns:
            Response: Réponse HTTP avec status 204 ou 400.
        """
        instance = self.get_object()
        
        # Vérifier si la catégorie contient des médicaments actifs
        if instance.medicaments.filter(est_actif=True).exists():
            return Response(
                {
                    'error': 'Impossible de supprimer cette catégorie car elle contient des médicaments actifs.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
