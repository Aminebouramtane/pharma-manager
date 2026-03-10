from django.contrib import admin
from .models import Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les catégories.
    """
    list_display = ['nom', 'nombre_medicaments', 'date_creation']
    search_fields = ['nom', 'description']
    list_per_page = 20
    
    def nombre_medicaments(self, obj):
        return obj.medicaments.filter(est_actif=True).count()
    nombre_medicaments.short_description = 'Nb médicaments'
