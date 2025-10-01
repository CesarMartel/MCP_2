from django.contrib import admin

from .models import Productos


@admin.register(Productos)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cantidad")
    search_fields = ("nombre", "descripcion")

# Register your models here.
