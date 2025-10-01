from django.apps import AppConfig


class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'  # Este atributo DEBE ser 'name' por requerimiento de Django
