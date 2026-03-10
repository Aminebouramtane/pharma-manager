"""
URLs pour l'application medicaments.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Will be imported after creating viewsets
# from .views import MedicamentViewSet

router = DefaultRouter()
# router.register(r'', MedicamentViewSet, basename='medicament')

urlpatterns = [
    path('', include(router.urls)),
]
