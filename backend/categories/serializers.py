"""
Serializers pour l'application categories.
"""
from rest_framework import serializers
from .models import Categorie


class CategorieSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Categorie.
    
    Fournit la sérialisation/désérialisation complète des catégories de médicaments.
    """
    nombre_medicaments = serializers.SerializerMethodField()
    
    class Meta:
        model = Categorie
        fields = [
            'id',
            'nom',
            'description',
            'nombre_medicaments',
            'date_creation',
        ]
        read_only_fields = ['id', 'date_creation', 'nombre_medicaments']
    
    def get_nombre_medicaments(self, obj):
        """
        Retourne le nombre de médicaments actifs dans cette catégorie.
        
        Args:
            obj (Categorie): Instance de la catégorie.
            
        Returns:
            int: Nombre de médicaments actifs.
        """
        return obj.medicaments.filter(est_actif=True).count()
    
    def validate_nom(self, value):
        """
        Valide que le nom de la catégorie est unique (case-insensitive).
        
        Args:
            value (str): Nom de la catégorie à valider.
            
        Returns:
            str: Nom validé.
            
        Raises:
            serializers.ValidationError: Si le nom existe déjà.
        """
        # Check for duplicates (case-insensitive), excluding current instance
        queryset = Categorie.objects.filter(nom__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                "Une catégorie avec ce nom existe déjà."
            )
        
        return value
