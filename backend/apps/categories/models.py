"""
Modèle Categorie pour la classification des médicaments.
"""
from django.db import models


class Categorie(models.Model):
    """
    Représente une catégorie de médicaments (ex: antibiotique, antalgique).
    
    Attributs:
        nom (str): Nom de la catégorie.
        description (str): Description optionnelle de la catégorie.
        date_creation (datetime): Date de création automatique.
    """
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nom de la catégorie'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
