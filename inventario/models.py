from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    cantidad = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.nombre} ({self.cantidad} unidades)"
    
    def esta_disponible(self):
        return self.cantidad > 0

# Create your models here.
