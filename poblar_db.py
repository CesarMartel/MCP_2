import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_inteligente.settings')
django.setup()

from inventario.models import Producto

def poblar_inventario():
    productos = [
        {
            'nombre': 'Teclado Mecánico RGB',
            'descripcion': 'Teclado mecánico con retroiluminación RGB switches azules',
            'cantidad': 15
        },
        {
            'nombre': 'Mouse Inalámbrico', 
            'descripcion': 'Mouse ergonómico inalámbrico con sensor de 16000 DPI',
            'cantidad': 30
        },
        {
            'nombre': 'Monitor 24 pulgadas',
            'descripcion': 'Monitor LED Full HD 1920x1080 75Hz',
            'cantidad': 10
        },
        {
            'nombre': 'Auriculares Gaming',
            'descripcion': 'Auriculares con sonido surround 7.1 y micrófono retráctil',
            'cantidad': 0  # ← Producto agotado como requiere el ejercicio
        }
    ]
    
    # Limpiar productos existentes
    Producto.objects.all().delete()
    
    # Crear nuevos productos
    for producto_data in productos:
        Producto.objects.create(**producto_data)
    
    print("✅ Inventario poblado exitosamente!")
    print("📦 Productos creados:")
    for producto in Producto.objects.all():
        print(f"   - {producto.nombre}: {producto.cantidad} unidades")

if __name__ == '__main__':
    poblar_inventario()