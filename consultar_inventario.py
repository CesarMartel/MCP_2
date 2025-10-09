import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_inteligente.settings')
django.setup()

from inventario.models import Producto

# Importar Vertex AI (como en tu primer ejercicio)
import vertexai
from vertexai.generative_models import GenerativeModel

def consultar_inventario_inteligente():
    # Configurar Vertex AI con tu PROJECT_ID existente
    PROJECT_ID = "stone-poetry-473315-a9"
    LOCATION = "us-central1"
    
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # Obtener productos disponibles (cantidad > 0)
    productos_disponibles = Producto.objects.filter(cantidad__gt=0)
    
    if not productos_disponibles:
        return "❌ No hay productos disponibles en el inventario."
    
    # Formatear datos para la IA
    datos_inventario = "\n".join([
        f"- {producto.nombre} ({producto.cantidad} unidades): {producto.descripcion}"
        for producto in productos_disponibles
    ])
    
    # Prompt para la IA
    prompt = f"""
    Eres un asistente de inventario. Basado en los siguientes productos disponibles:
    
    {datos_inventario}
    
    Genera una respuesta natural y amigable que:
    1. Salude brevemente
    2. Liste SOLO los productos disponibles (cantidad > 0)
    3. Mencione las cantidades de cada uno
    4. Sea concisa y profesional
    
    Responde en español y solo con el texto solicitado, sin formato adicional.
    """
    
    try:
        # Usar el modelo Gemini (igual que tu primer ejercicio)
        model = GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        return response.text.strip()
        
    except Exception as e:
        return f"❌ Error al consultar la IA: {e}"

def consultar_inventario_simple():
    """Versión sin IA por si hay problemas con la API"""
    productos_disponibles = Producto.objects.filter(cantidad__gt=0)
    
    if not productos_disponibles:
        return "❌ No hay productos disponibles en el inventario."
    
    resultado = "Hola, los productos disponibles en el inventario son:\n\n"
    for producto in productos_disponibles:
        resultado += f"• {producto.nombre} ({producto.cantidad} unidades)\n"
    
    return resultado

if __name__ == '__main__':
    print("🔍 Consultando inventario inteligente...\n")
    
    # Intentar con IA primero, fallback a versión simple
    try:
        respuesta = consultar_inventario_inteligente()
        print(respuesta)
    except Exception as e:
        print(f"⚠️ Usando versión simple (IA no disponible: {e})")
        respuesta = consultar_inventario_simple()
        print(respuesta)
    
    print(f"\n📊 Total de productos disponibles: {Producto.objects.filter(cantidad__gt=0).count()}")