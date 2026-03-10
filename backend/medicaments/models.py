"""
Modèle Medicament pour la gestion de l'inventaire de la pharmacie.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Medicament(models.Model):
    """
    Représente un médicament dans l'inventaire de la pharmacie.
    
    Attributs:
        nom (str): Nom commercial du médicament.
        dci (str): Dénomination Commune Internationale.
        categorie (ForeignKey): Catégorie du médicament.
        forme (str): Forme galénique (comprimé, sirop, injection...).
        dosage (str): Dosage du médicament (ex: 500mg, 250mg/5ml).
        prix_achat (Decimal): Prix d'achat unitaire.
        prix_vente (Decimal): Prix de vente public.
        stock_actuel (int): Quantité disponible en stock.
        stock_minimum (int): Seuil déclenchant une alerte de réapprovisionnement.
        date_expiration (date): Date de péremption.
        ordonnance_requise (bool): Médicament sous ordonnance ou non.
        date_creation (datetime): Horodatage automatique.
        est_actif (bool): Soft delete. False = médicament archivé.
    """
    
    FORME_CHOICES = [
        ('comprime', 'Comprimé'),
        ('gelule', 'Gélule'),
        ('sirop', 'Sirop'),
        ('injection', 'Injection'),
        ('pommade', 'Pommade'),
        ('suppositoire', 'Suppositoire'),
        ('sachet', 'Sachet'),
        ('gouttes', 'Gouttes'),
        ('spray', 'Spray'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(
        max_length=200,
        verbose_name='Nom commercial'
    )
    dci = models.CharField(
        max_length=200,
        verbose_name='DCI',
        blank=True,
        help_text='Dénomination Commune Internationale'
    )
    categorie = models.ForeignKey(
        'categories.Categorie',
        on_delete=models.PROTECT,
        related_name='medicaments',
        verbose_name='Catégorie'
    )
    forme = models.CharField(
        max_length=50,
        choices=FORME_CHOICES,
        verbose_name='Forme galénique'
    )
    dosage = models.CharField(
        max_length=50,
        verbose_name='Dosage',
        help_text='Ex: 500mg, 250mg/5ml'
    )
    prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Prix d'achat"
    )
    prix_vente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Prix de vente'
    )
    stock_actuel = models.PositiveIntegerField(
        default=0,
        verbose_name='Stock actuel'
    )
    stock_minimum = models.PositiveIntegerField(
        default=10,
        verbose_name='Stock minimum',
        help_text='Seuil d\'alerte de réapprovisionnement'
    )
    date_expiration = models.DateField(
        verbose_name='Date d\'expiration'
    )
    ordonnance_requise = models.BooleanField(
        default=False,
        verbose_name='Ordonnance requise'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name='Actif',
        help_text='Soft delete - False = médicament archivé'
    )
    
    class Meta:
        verbose_name = 'Médicament'
        verbose_name_plural = 'Médicaments'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['categorie']),
            models.Index(fields=['est_actif']),
        ]
    
    def __str__(self):
        return f'{self.nom} ({self.dosage})'
    
    @property
    def est_en_alerte(self):
        """
        Retourne True si le stock est inférieur ou égal au seuil minimum.
        
        Returns:
            bool: True si le médicament nécessite un réapprovisionnement.
        """
        return self.stock_actuel <= self.stock_minimum
    
    @property
    def marge_beneficiaire(self):
        """
        Calcule la marge bénéficiaire en pourcentage.
        
        Returns:
            Decimal: Marge bénéficiaire en pourcentage.
        """
        if self.prix_achat > 0:
            return ((self.prix_vente - self.prix_achat) / self.prix_achat) * 100
        return Decimal('0.00')
