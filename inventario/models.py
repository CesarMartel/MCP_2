from django.db import models


class Producto(models.Model):
    """
    Modelo para representar un producto en el inventario.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción")
    cantidad = models.PositiveIntegerField(default=0, verbose_name="Cantidad en Stock")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.cantidad} unidades)"

    @property
    def esta_disponible(self):
        """Retorna True si el producto tiene stock disponible."""
        return self.cantidad > 0

    @property
    def estado_stock(self):
        """Retorna el estado del stock en texto legible."""
        if self.cantidad == 0:
            return "Agotado"
        elif self.cantidad <= 5:
            return "Stock Bajo"
        else:
            return "Disponible"



