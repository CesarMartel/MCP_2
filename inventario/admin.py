from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'estado_stock', 'fecha_creacion')
    list_filter = ('cantidad', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('cantidad',)
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Inventario', {
            'fields': ('cantidad',)
        }),
    )



