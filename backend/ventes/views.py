"""
Views pour l'application ventes.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Vente, LigneVente
from .serializers import (
    VenteListSerializer,
    VenteDetailSerializer,
    VenteCreateSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Liste des ventes",
        description="Récupère l'historique des ventes avec filtrage optionnel par date et statut.",
        tags=['Ventes'],
        parameters=[
            OpenApiParameter(name='date_debut', description='Filtrer à partir de cette date (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='date_fin', description='Filtrer jusqu\'à cette date (YYYY-MM-DD)', required=False, type=str),
            OpenApiParameter(name='statut', description='Filtrer par statut', required=False, type=str),
        ]
    ),
    create=extend_schema(
        summary="Créer une vente",
        description="Enregistre une nouvelle vente avec ses lignes et déduit automatiquement les stocks.",
        tags=['Ventes']
    ),
    retrieve=extend_schema(
        summary="Détail d'une vente",
        description="Récupère les détails complets d'une vente avec toutes ses lignes.",
        tags=['Ventes']
    ),
)
class VenteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des ventes.
    
    Fournit les opérations de création, consultation et annulation des ventes.
    """
    queryset = Vente.objects.prefetch_related('lignes__medicament').all()
    http_method_names = ['get', 'post', 'head', 'options']  # Pas de PUT/PATCH/DELETE
    
    def get_serializer_class(self):
        """
        Retourne le serializer approprié selon l'action.
        
        Returns:
            Serializer: Classe du serializer à utiliser.
        """
        if self.action == 'list':
            return VenteListSerializer
        elif self.action == 'create':
            return VenteCreateSerializer
        return VenteDetailSerializer
    
    def get_queryset(self):
        """
        Retourne le queryset filtré selon les paramètres de la requête.
        
        Returns:
            QuerySet: Queryset filtré.
        """
        queryset = super().get_queryset()
        
        # Filtrage par date de début
        date_debut = self.request.query_params.get('date_debut', None)
        if date_debut:
            queryset = queryset.filter(date_vente__date__gte=date_debut)
        
        # Filtrage par date de fin
        date_fin = self.request.query_params.get('date_fin', None)
        if date_fin:
            queryset = queryset.filter(date_vente__date__lte=date_fin)
        
        # Filtrage par statut
        statut = self.request.query_params.get('statut', None)
        if statut:
            queryset = queryset.filter(statut=statut)
        
        return queryset
    
    @extend_schema(
        summary="Annuler une vente",
        description="Annule une vente et réintègre les quantités dans le stock.",
        tags=['Ventes'],
        responses={200: VenteDetailSerializer}
    )
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def annuler(self, request, pk=None):
        """
        Annule une vente et réintègre les stocks.
        
        Args:
            request: Requête HTTP.
            pk: ID de la vente.
            
        Returns:
            Response: Détails de la vente annulée ou erreur.
        """
        vente = self.get_object()
        
        # Vérifier si la vente peut être annulée
        if vente.statut == 'annulee':
            return Response(
                {'error': 'Cette vente est déjà annulée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Réintégrer les stocks pour chaque ligne
        for ligne in vente.lignes.all():
            medicament = ligne.medicament
            medicament.stock_actuel += ligne.quantite
            medicament.save(update_fields=['stock_actuel'])
        
        # Marquer la vente comme annulée
        vente.statut = 'annulee'
        vente.save(update_fields=['statut'])
        
        serializer = VenteDetailSerializer(vente)
        return Response(serializer.data)
