"""
URLs pour l'application ventes.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Will be imported after creating viewsets
# from .views import VenteViewSet

router = DefaultRouter()
# router.register(r'', VenteViewSet, basename='vente')

urlpatterns = [
    path('', include(router.urls)),
]
