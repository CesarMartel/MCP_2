from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto


def index(request):
    """Vista principal que muestra el inventario."""
    productos = Producto.objects.all()
    context = {
        'productos': productos,
        'total_productos': productos.count(),
        'productos_disponibles': productos.filter(cantidad__gt=0).count(),
    }
    return render(request, 'inventario/index.html', context)



