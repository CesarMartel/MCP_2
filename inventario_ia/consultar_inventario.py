# consultar_inventario.py
import os
import django

# 1. Configurar el entorno Django
# Esto es crucial para que el script acceda a la configuración y modelos de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventarioIA.settings')
django.setup()

from core.models import Producto

def consultar_productos_disponibles_ia():
    """
    Simula la lógica de una IA: consulta el inventario y lista solo el stock > 0.
    """
    
    print("--- Asistente de Inventario (IA) Iniciando Consulta ---")
    
    # 2. Filtrado Inteligente (Lógica Clave)
    # Solo recuperamos productos cuya cantidad sea estrictamente mayor a cero.
    productos_disponibles = Producto.objects.filter(cantidad__gt=0).order_by('nombre')
    
    # 3. Generar Respuesta en Lenguaje Natural
    if not productos_disponibles.exists():
        respuesta = "Lo siento, actualmente no hay productos disponibles en el inventario con stock positivo."
    else:
        # Construir la lista de productos disponibles
        lista_productos = []
        for producto in productos_disponibles:
            lista_productos.append(f"- {producto.nombre} ({producto.cantidad} unidades)")
            
        # Unir la respuesta
        respuesta = "Hola, los productos disponibles en el inventario son:\n"
        respuesta += "\n".join(lista_productos)

    print(respuesta)
    print("---------------------------------------------------------")

if __name__ == '__main__':
    consultar_productos_disponibles_ia()