"""
Servicio de IA local para consultas del inventario.
Genera respuestas en lenguaje natural sin dependencias externas.
"""
import random
from .models import Producto


class InventarioAIService:
    """
    Servicio que simula IA para consultar el inventario y generar respuestas en lenguaje natural.
    """
    
    def __init__(self):
        """Inicializa el servicio de IA local."""
        self.saludos = [
            "Hola, los productos disponibles en el inventario son:",
            "¡Buenos días! Los productos disponibles son:",
            "Hola! Aquí tienes los productos disponibles:",
            "¡Hola! Los productos que tenemos disponibles son:"
        ]
    
    def consultar_productos_disponibles(self):
        """
        Consulta los productos disponibles en el inventario y genera una respuesta en lenguaje natural.
        
        Returns:
            str: Respuesta en lenguaje natural sobre los productos disponibles
        """
        try:
            # Obtener productos con stock mayor a 0
            productos_disponibles = Producto.objects.filter(cantidad__gt=0).order_by('nombre')
            
            if not productos_disponibles.exists():
                return "Lo siento, actualmente no hay productos disponibles en el inventario."
            
            # Generar respuesta natural
            saludo = random.choice(self.saludos)
            respuesta = saludo + "\n\n"
            
            for producto in productos_disponibles:
                respuesta += f"- {producto.nombre} ({producto.cantidad} unidades)\n"
            
            return respuesta
            
        except Exception as e:
            return f"Error al consultar el inventario: {e}"
    
    def consultar_estado_inventario(self):
        """
        Consulta el estado general del inventario.
        
        Returns:
            str: Resumen del estado del inventario en lenguaje natural
        """
        try:
            total_productos = Producto.objects.count()
            productos_disponibles = Producto.objects.filter(cantidad__gt=0).count()
            productos_agotados = Producto.objects.filter(cantidad=0).count()
            
            # Obtener productos con stock bajo (1-5 unidades)
            productos_stock_bajo = Producto.objects.filter(cantidad__gt=0, cantidad__lte=5).count()
            
            respuesta = f"""
Estado actual del inventario:

- Total de productos en catálogo: {total_productos}
- Productos disponibles: {productos_disponibles}
- Productos agotados: {productos_agotados}
- Productos con stock bajo: {productos_stock_bajo}

El inventario se encuentra en buen estado con {productos_disponibles} productos disponibles.
"""
            
            return respuesta
            
        except Exception as e:
            return f"Error al consultar el estado del inventario: {e}"

