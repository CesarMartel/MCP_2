"""
WSGI config for inventario_inteligente project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_inteligente.settings')

application = get_wsgi_application()



