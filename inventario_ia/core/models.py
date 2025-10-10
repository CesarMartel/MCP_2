from django.db import models

# Create your models here.
# core/models.py

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    cantidad = models.IntegerField(default=0, verbose_name="Cantidad en Stock")

    class Meta:
        # Esto es opcional, mejora el nombre de la tabla en el Admin
        verbose_name_plural = "Productos"
        
    def __str__(self):
        return f"{self.nombre} ({self.cantidad} uds.)"