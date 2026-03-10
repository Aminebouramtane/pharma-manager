from django.contrib import admin
from .models import Medicament


@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les médicaments.
    """
    list_display = [
        'nom',
        'dosage',
        'categorie',
        'stock_actuel',
        'stock_minimum',
        'prix_vente',
        'est_en_alerte',
        'est_actif'
    ]
    list_filter = ['categorie', 'forme', 'ordonnance_requise', 'est_actif']
    search_fields = ['nom', 'dci']
    list_editable = ['stock_actuel']
    list_per_page = 25
    date_hierarchy = 'date_creation'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'dci', 'categorie', 'forme', 'dosage')
        }),
        ('Prix', {
            'fields': ('prix_achat', 'prix_vente')
        }),
        ('Stock', {
            'fields': ('stock_actuel', 'stock_minimum')
        }),
        ('Autres', {
            'fields': ('date_expiration', 'ordonnance_requise', 'est_actif')
        }),
    )
    
    def est_en_alerte(self, obj):
        return obj.est_en_alerte
    est_en_alerte.boolean = True
    est_en_alerte.short_description = 'Alerte stock'
