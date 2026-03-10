"""
Serializers pour l'application medicaments.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Medicament
from apps.categories.serializers import CategorieSerializer


class MedicamentListSerializer(serializers.ModelSerializer):
    """
    Serializer pour la liste des médicaments (vue simplifiée).
    """
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    est_en_alerte = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Medicament
        fields = [
            'id',
            'nom',
            'dci',
            'categorie',
            'categorie_nom',
            'forme',
            'dosage',
            'prix_vente',
            'stock_actuel',
            'stock_minimum',
            'est_en_alerte',
            'ordonnance_requise',
            'est_actif',
        ]


class MedicamentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour le modèle Medicament.
    
    Inclut toutes les informations du médicament avec des champs calculés.
    """
    categorie_detail = CategorieSerializer(source='categorie', read_only=True)
    est_en_alerte = serializers.BooleanField(read_only=True)
    marge_beneficiaire = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Medicament
        fields = [
            'id',
            'nom',
            'dci',
            'categorie',
            'categorie_detail',
            'forme',
            'dosage',
            'prix_achat',
            'prix_vente',
            'stock_actuel',
            'stock_minimum',
            'date_expiration',
            'ordonnance_requise',
            'date_creation',
            'est_actif',
            'est_en_alerte',
            'marge_beneficiaire',
        ]
        read_only_fields = ['id', 'date_creation', 'est_en_alerte', 'marge_beneficiaire']
    
    def validate_date_expiration(self, value):
        """
        Valide que la date d'expiration est dans le futur.
        
        Args:
            value (date): Date d'expiration à valider.
            
        Returns:
            date: Date validée.
            
        Raises:
            serializers.ValidationError: Si la date est dans le passé.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "La date d'expiration ne peut pas être dans le passé."
            )
        return value
    
    def validate(self, data):
        """
        Validation globale des données du médicament.
        
        Args:
            data (dict): Données à valider.
            
        Returns:
            dict: Données validées.
            
        Raises:
            serializers.ValidationError: Si les données sont invalides.
        """
        # Vérifier que le prix de vente est supérieur au prix d'achat
        prix_achat = data.get('prix_achat', None)
        prix_vente = data.get('prix_vente', None)
        
        if prix_achat and prix_vente:
            if prix_vente <= prix_achat:
                raise serializers.ValidationError(
                    "Le prix de vente doit être supérieur au prix d'achat."
                )
        
        # Vérifier que le stock minimum est positif
        stock_minimum = data.get('stock_minimum', None)
        if stock_minimum is not None and stock_minimum < 0:
            raise serializers.ValidationError(
                "Le stock minimum doit être positif."
            )
        
        return data


class MedicamentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création et mise à jour des médicaments.
    """
    
    class Meta:
        model = Medicament
        fields = [
            'id',
            'nom',
            'dci',
            'categorie',
            'forme',
            'dosage',
            'prix_achat',
            'prix_vente',
            'stock_actuel',
            'stock_minimum',
            'date_expiration',
            'ordonnance_requise',
            'est_actif',
        ]
        read_only_fields = ['id']
    
    def validate_date_expiration(self, value):
        """Valide que la date d'expiration est dans le futur."""
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "La date d'expiration ne peut pas être dans le passé."
            )
        return value
    
    def validate(self, data):
        """Validation globale des données."""
        prix_achat = data.get('prix_achat', getattr(self.instance, 'prix_achat', None))
        prix_vente = data.get('prix_vente', getattr(self.instance, 'prix_vente', None))
        
        if prix_achat and prix_vente and prix_vente <= prix_achat:
            raise serializers.ValidationError(
                {"prix_vente": "Le prix de vente doit être supérieur au prix d'achat."}
            )
        
        return data
