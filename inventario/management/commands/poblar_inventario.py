"""
Comando de Django para poblar el inventario con datos de ejemplo.
"""
from django.core.management.base import BaseCommand
from inventario.models import Producto


class Command(BaseCommand):
    help = 'Pobla el inventario con productos de ejemplo'

    def handle(self, *args, **options):
        """Ejecuta el comando para poblar el inventario."""
        
        # Productos de ejemplo según los requisitos
        productos_ejemplo = [
            {
                'nombre': 'Teclado Mecánico RGB',
                'descripcion': 'Teclado mecánico con retroiluminación RGB, switches Cherry MX Blue, perfecto para gaming y programación.',
                'cantidad': 15
            },
            {
                'nombre': 'Mouse Inalámbrico',
                'descripcion': 'Mouse óptico inalámbrico con sensor de alta precisión, batería de larga duración y diseño ergonómico.',
                'cantidad': 30
            },
            {
                'nombre': 'Monitor 24 pulgadas',
                'descripcion': 'Monitor LED de 24 pulgadas, resolución Full HD, panel IPS, ideal para trabajo y entretenimiento.',
                'cantidad': 10
            },
            {
                'nombre': 'Auriculares Gaming',
                'descripcion': 'Auriculares gaming con micrófono, sonido surround 7.1, cancelación de ruido y RGB.',
                'cantidad': 0  # Producto agotado como se requiere
            },
            {
                'nombre': 'Webcam HD',
                'descripcion': 'Cámara web HD 1080p con micrófono integrado, perfecta para videoconferencias y streaming.',
                'cantidad': 8
            },
            {
                'nombre': 'Disco SSD 1TB',
                'descripcion': 'Disco sólido SSD de 1TB, velocidad de lectura/escritura alta, ideal para mejorar el rendimiento del sistema.',
                'cantidad': 0  # Otro producto agotado
            }
        ]
        
        # Limpiar productos existentes
        Producto.objects.all().delete()
        self.stdout.write('[INFO] Productos existentes eliminados')
        
        # Crear productos de ejemplo
        productos_creados = 0
        for producto_data in productos_ejemplo:
            producto, created = Producto.objects.get_or_create(
                nombre=producto_data['nombre'],
                defaults={
                    'descripcion': producto_data['descripcion'],
                    'cantidad': producto_data['cantidad']
                }
            )
            if created:
                productos_creados += 1
                estado = "[OK] Disponible" if producto.cantidad > 0 else "[OUT] Agotado"
                self.stdout.write(
                    f'  [PRODUCTO] {producto.nombre} - {producto.cantidad} unidades - {estado}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n[SUCCESS] Inventario poblado exitosamente con {productos_creados} productos'
            )
        )
        
        # Mostrar resumen
        total = Producto.objects.count()
        disponibles = Producto.objects.filter(cantidad__gt=0).count()
        agotados = Producto.objects.filter(cantidad=0).count()
        
        self.stdout.write(f'\n[RESUMEN] Resumen del inventario:')
        self.stdout.write(f'   Total de productos: {total}')
        self.stdout.write(f'   Productos disponibles: {disponibles}')
        self.stdout.write(f'   Productos agotados: {agotados}')
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n[READY] Listo! Ahora puedes ejecutar "python consultar_inventario.py"'
            )
        )
