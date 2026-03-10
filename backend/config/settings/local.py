"""
Settings de développement local.
Hérite de base.py et ajoute des configurations spécifiques au développement.
"""

from .base import *

# Override DEBUG pour le développement
DEBUG = True

# Additional apps for development
INSTALLED_APPS += [
    # 'debug_toolbar',  # Décommenter si nécessaire
]

# Development middleware
MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',  # Décommenter si nécessaire
]

# CORS plus permissif en développement
CORS_ALLOW_ALL_ORIGINS = True

# Logging pour le développement
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
