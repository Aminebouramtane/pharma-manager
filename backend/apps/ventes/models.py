"""
Modèles pour la gestion des ventes et transactions.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class Vente(models.Model):
    """
    Représente une transaction de vente dans la pharmacie.
    
    Attributs:
        reference (str): Code unique auto-généré (ex: VNT-2024-0001).
        date_vente (datetime): Date et heure de la transaction.
        total_ttc (Decimal): Montant total calculé automatiquement.
        statut (str): État de la vente (en_cours, completee, annulee).
        notes (str): Remarques optionnelles.
    """
    
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('completee', 'Complétée'),
        ('annulee', 'Annulée'),
    ]
    
    reference = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Référence',
        help_text='Code unique auto-généré (ex: VNT-2024-0001)'
    )
    date_vente = models.DateTimeField(
        default=timezone.now,
        verbose_name='Date de vente'
    )
    total_ttc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Total TTC',
        help_text='Montant total calculé automatiquement'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_cours',
        verbose_name='Statut'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Remarques'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )
    
    class Meta:
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'
        ordering = ['-date_vente']
        indexes = [
            models.Index(fields=['-date_vente']),
            models.Index(fields=['statut']),
            models.Index(fields=['reference']),
        ]
    
    def __str__(self):
        return f'{self.reference} - {self.date_vente.strftime("%Y-%m-%d %H:%M")}'
    
    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour générer automatiquement la référence.
        """
        if not self.reference:
            # Génération de la référence: VNT-YYYY-NNNN
            year = timezone.now().year
            last_vente = Vente.objects.filter(
                reference__startswith=f'VNT-{year}-'
            ).order_by('-reference').first()
            
            if last_vente:
                last_number = int(last_vente.reference.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.reference = f'VNT-{year}-{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    def calculer_total(self):
        """
        Calcule le total TTC de la vente en sommant tous les sous-totaux des lignes.
        
        Returns:
            Decimal: Total TTC de la vente.
        """
        total = sum(ligne.sous_total for ligne in self.lignes.all())
        self.total_ttc = total
        self.save(update_fields=['total_ttc'])
        return total


class LigneVente(models.Model):
    """
    Représente une ligne de vente (un médicament dans une vente).
    
    Attributs:
        vente (ForeignKey): Vente associée.
        medicament (ForeignKey): Médicament vendu.
        quantite (int): Quantité vendue.
        prix_unitaire (Decimal): Prix au moment de la vente (snapshot).
        sous_total (Decimal): Calculé: quantité × prix_unitaire.
    
    Note:
        Le prix_unitaire est un snapshot du prix au moment de la vente.
        Ne pas utiliser de ForeignKey au prix car les prix peuvent changer.
    """
    
    vente = models.ForeignKey(
        Vente,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name='Vente'
    )
    medicament = models.ForeignKey(
        'medicaments.Medicament',
        on_delete=models.PROTECT,
        related_name='lignes_ventes',
        verbose_name='Médicament'
    )
    quantite = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantité'
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Prix unitaire',
        help_text='Prix au moment de la vente (snapshot)'
    )
    sous_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Sous-total',
        help_text='Calculé: quantité × prix_unitaire'
    )
    
    class Meta:
        verbose_name = 'Ligne de vente'
        verbose_name_plural = 'Lignes de vente'
        ordering = ['id']
    
    def __str__(self):
        return f'{self.medicament.nom} x {self.quantite}'
    
    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour calculer automatiquement le sous-total.
        """
        self.sous_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
