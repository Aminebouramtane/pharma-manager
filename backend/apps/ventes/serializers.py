"""
Serializers pour l'application ventes.
"""
from rest_framework import serializers
from django.db import transaction
from .models import Vente, LigneVente
from apps.medicaments.models import Medicament


class LigneVenteSerializer(serializers.ModelSerializer):
    """
    Serializer pour les lignes de vente.
    """
    medicament_nom = serializers.CharField(source='medicament.nom', read_only=True)
    medicament_dosage = serializers.CharField(source='medicament.dosage', read_only=True)
    
    class Meta:
        model = LigneVente
        fields = [
            'id',
            'medicament',
            'medicament_nom',
            'medicament_dosage',
            'quantite',
            'prix_unitaire',
            'sous_total',
        ]
        read_only_fields = ['id', 'sous_total']
    
    def validate_quantite(self, value):
        """
        Valide que la quantité est positive.
        
        Args:
            value (int): Quantité à valider.
            
        Returns:
            int: Quantité validée.
            
        Raises:
            serializers.ValidationError: Si la quantité est invalide.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "La quantité doit être supérieure à zéro."
            )
        return value


class VenteListSerializer(serializers.ModelSerializer):
    """
    Serializer pour la liste des ventes (vue simplifiée).
    """
    nombre_articles = serializers.SerializerMethodField()
    
    class Meta:
        model = Vente
        fields = [
            'id',
            'reference',
            'date_vente',
            'total_ttc',
            'statut',
            'nombre_articles',
        ]
        read_only_fields = ['id', 'reference']
    
    def get_nombre_articles(self, obj):
        """
        Retourne le nombre total d'articles dans la vente.
        
        Args:
            obj (Vente): Instance de la vente.
            
        Returns:
            int: Nombre total d'articles.
        """
        return sum(ligne.quantite for ligne in obj.lignes.all())


class VenteDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour les ventes avec leurs lignes.
    """
    lignes = LigneVenteSerializer(many=True, read_only=True)
    nombre_articles = serializers.SerializerMethodField()
    
    class Meta:
        model = Vente
        fields = [
            'id',
            'reference',
            'date_vente',
            'total_ttc',
            'statut',
            'notes',
            'lignes',
            'nombre_articles',
            'date_creation',
            'date_modification',
        ]
        read_only_fields = ['id', 'reference', 'total_ttc', 'date_creation', 'date_modification']
    
    def get_nombre_articles(self, obj):
        """Retourne le nombre total d'articles dans la vente."""
        return sum(ligne.quantite for ligne in obj.lignes.all())


class VenteCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création d'une vente avec ses lignes.
    """
    lignes = LigneVenteSerializer(many=True)
    
    class Meta:
        model = Vente
        fields = [
            'id',
            'reference',
            'date_vente',
            'statut',
            'notes',
            'lignes',
            'total_ttc',
        ]
        read_only_fields = ['id', 'reference', 'total_ttc']
    
    def validate_lignes(self, value):
        """
        Valide les lignes de vente.
        
        Args:
            value (list): Liste des lignes de vente.
            
        Returns:
            list: Lignes validées.
            
        Raises:
            serializers.ValidationError: Si les lignes sont invalides.
        """
        if not value:
            raise serializers.ValidationError(
                "Une vente doit contenir au moins une ligne."
            )
        
        # Vérifier les stocks disponibles pour chaque médicament
        for ligne in value:
            medicament = ligne['medicament']
            quantite = ligne['quantite']
            
            if not medicament.est_actif:
                raise serializers.ValidationError(
                    f"Le médicament '{medicament.nom}' n'est plus disponible."
                )
            
            if medicament.stock_actuel < quantite:
                raise serializers.ValidationError(
                    f"Stock insuffisant pour '{medicament.nom}'. "
                    f"Disponible: {medicament.stock_actuel}, Demandé: {quantite}"
                )
        
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Crée une vente avec ses lignes et déduit les stocks.
        
        Args:
            validated_data (dict): Données validées.
            
        Returns:
            Vente: Instance de la vente créée.
        """
        lignes_data = validated_data.pop('lignes')
        vente = Vente.objects.create(**validated_data)
        
        total = 0
        for ligne_data in lignes_data:
            medicament = ligne_data['medicament']
            quantite = ligne_data['quantite']
            
            # Utiliser le prix de vente actuel du médicament (snapshot)
            prix_unitaire = medicament.prix_vente
            
            # Créer la ligne de vente
            LigneVente.objects.create(
                vente=vente,
                medicament=medicament,
                quantite=quantite,
                prix_unitaire=prix_unitaire,
                sous_total=quantite * prix_unitaire
            )
            
            # Déduire le stock
            medicament.stock_actuel -= quantite
            medicament.save(update_fields=['stock_actuel'])
            
            total += quantite * prix_unitaire
        
        # Mettre à jour le total de la vente
        vente.total_ttc = total
        vente.statut = 'completee'
        vente.save(update_fields=['total_ttc', 'statut'])
        
        return vente
