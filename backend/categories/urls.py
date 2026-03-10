"""
URLs pour l'application categories.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Will be imported after creating viewsets
# from .views import CategorieViewSet

router = DefaultRouter()
# router.register(r'', CategorieViewSet, basename='categorie')

urlpatterns = [
    path('', include(router.urls)),
]
