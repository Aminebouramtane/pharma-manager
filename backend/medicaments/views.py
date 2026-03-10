"""
Views pour l'application medicaments.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Medicament
from .serializers import (
    MedicamentListSerializer,
    MedicamentDetailSerializer,
    MedicamentCreateUpdateSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Liste des médicaments",
        description="Récupère la liste paginée des médicaments actifs avec filtres optionnels.",
        tags=['Médicaments'],
        parameters=[
            OpenApiParameter(name='search', description='Recherche par nom ou DCI', required=False, type=str),
            OpenApiParameter(name='categorie', description='Filtrer par ID de catégorie', required=False, type=int),
            OpenApiParameter(name='forme', description='Filtrer par forme galénique', required=False, type=str),
        ]
    ),
    create=extend_schema(
        summary="Créer un médicament",
        description="Crée un nouveau médicament dans l'inventaire.",
        tags=['Médicaments']
    ),
    retrieve=extend_schema(
        summary="Détail d'un médicament",
        description="Récupère les détails complets d'un médicament.",
        tags=['Médicaments']
    ),
    update=extend_schema(
        summary="Modifier un médicament",
        description="Modifie complètement un médicament existant.",
        tags=['Médicaments']
    ),
    partial_update=extend_schema(
        summary="Modification partielle",
        description="Modifie partiellement un médicament existant.",
        tags=['Médicaments']
    ),
    destroy=extend_schema(
        summary="Supprimer un médicament",
        description="Supprime un médicament (soft delete - marque comme inactif).",
        tags=['Médicaments']
    ),
)
class MedicamentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des médicaments.
    
    Fournit les opérations CRUD complètes ainsi que des endpoints personnalisés
    pour les alertes de stock.
    """
    queryset = Medicament.objects.select_related('categorie').filter(est_actif=True)
    
    def get_serializer_class(self):
        """
        Retourne le serializer approprié selon l'action.
        
        Returns:
            Serializer: Classe du serializer à utiliser.
        """
        if self.action == 'list':
            return MedicamentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MedicamentCreateUpdateSerializer
        return MedicamentDetailSerializer
    
    def get_queryset(self):
        """
        Retourne le queryset filtré selon les paramètres de la requête.
        
        Returns:
            QuerySet: Queryset filtré.
        """
        queryset = super().get_queryset()
        
        # Filtrage par recherche (nom ou DCI)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) | Q(dci__icontains=search)
            )
        
        # Filtrage par catégorie
        categorie = self.request.query_params.get('categorie', None)
        if categorie:
            queryset = queryset.filter(categorie_id=categorie)
        
        # Filtrage par forme
        forme = self.request.query_params.get('forme', None)
        if forme:
            queryset = queryset.filter(forme=forme)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: marque le médicament comme inactif au lieu de le supprimer.
        
        Args:
            request: Requête HTTP.
            
        Returns:
            Response: Réponse HTTP avec status 204.
        """
        instance = self.get_object()
        instance.est_actif = False
        instance.save(update_fields=['est_actif'])
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        summary="Alertes de stock",
        description="Récupère la liste des médicaments dont le stock est inférieur ou égal au seuil minimum.",
        tags=['Médicaments'],
        responses={200: MedicamentListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def alertes(self, request):
        """
        Endpoint personnalisé pour récupérer les médicaments en alerte de stock.
        
        Args:
            request: Requête HTTP.
            
        Returns:
            Response: Liste des médicaments en alerte.
        """
        medicaments_alerte = Medicament.objects.filter(
            est_actif=True,
            stock_actuel__lte=models.F('stock_minimum')
        ).select_related('categorie')
        
        serializer = MedicamentListSerializer(medicaments_alerte, many=True)
        return Response(serializer.data)


# Import nécessaire pour l'utilisation de F() dans la vue
from django.db import models
