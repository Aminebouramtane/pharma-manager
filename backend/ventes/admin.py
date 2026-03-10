from django.contrib import admin
from .models import Vente, LigneVente


class LigneVenteInline(admin.TabularInline):
    """
    Inline pour afficher les lignes de vente dans l'admin des ventes.
    """
    model = LigneVente
    extra = 0
    readonly_fields = ['sous_total']
    fields = ['medicament', 'quantite', 'prix_unitaire', 'sous_total']


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les ventes.
    """
    list_display = ['reference', 'date_vente', 'total_ttc', 'statut']
    list_filter = ['statut', 'date_vente']
    search_fields = ['reference']
    readonly_fields = ['reference', 'total_ttc', 'date_creation', 'date_modification']
    date_hierarchy = 'date_vente'
    inlines = [LigneVenteInline]
    list_per_page = 25
    
    fieldsets = (
        ('Informations de vente', {
            'fields': ('reference', 'date_vente', 'statut')
        }),
        ('Montant', {
            'fields': ('total_ttc',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LigneVente)
class LigneVenteAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les lignes de vente.
    """
    list_display = ['vente', 'medicament', 'quantite', 'prix_unitaire', 'sous_total']
    list_filter = ['vente__statut']
    search_fields = ['vente__reference', 'medicament__nom']
    readonly_fields = ['sous_total']
    list_per_page = 50
