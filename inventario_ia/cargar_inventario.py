# cargar_inventario.py
import os
import django

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventarioIA.settings')
django.setup()

from core.models import Producto
from django.db.utils import IntegrityError

def cargar_datos_iniciales():
    """Carga los productos de ejemplo en la base de datos."""
    
    productos_iniciales = [
        # Stock Disponible (Disponibles para la IA)
        {"nombre": "Teclado  ", "descripcion": "Teclado con switches marrones y luces personalizables.", "cantidad": 15},
        {"nombre": "Mouse Inalámbrico", "descripcion": "Mouse ergonómico con sensor óptico de alta precisión.", "cantidad": 30},
        {"nombre": "Monitor 50 pulgadas", "descripcion": "Monitor Full HD con tasa de refresco de 75Hz.", "cantidad": 10},
        
        # Stock Agotado (ESENCIAL: No debe aparecer en la respuesta de la IA)
        {"nombre": "Cable HDMI 3m", "descripcion": "Cable para conexión de video de alta velocidad.", "cantidad": 0},
    ]

    print("Iniciando carga de datos...")
    for datos in productos_iniciales:
        try:
            # Crea o actualiza el producto si ya existe por nombre (para evitar duplicados)
            producto, created = Producto.objects.update_or_create(
                nombre=datos['nombre'],
                defaults=datos
            )
            if created:
                print(f"✅ Creado: {producto.nombre} ({producto.cantidad} uds)")
            else:
                print(f"🔄 Actualizado: {producto.nombre} ({producto.cantidad} uds)")
                
        except IntegrityError:
            print(f"⚠️ Error de integridad: {datos['nombre']} ya existe.")
        except Exception as e:
            print(f"❌ Error al cargar {datos['nombre']}: {e}")

    print("\nCarga de datos finalizada.")

if __name__ == '__main__':
    cargar_datos_iniciales()