import os
import django
import vertexai
from vertexai.generative_models import GenerativeModel

def conectar_vertexai(project_id, location):
    try:
        vertexai.init(project=project_id, location=location)
    except Exception as e:
        print(f"Error al inicializar Vertex AI: {e}")
        exit(1)

def consultar_inventario_disponible():
    # Consulta la base de datos y devuelve una cadena con los productos disponibles.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    from inventario.models import Producto
    productos = Producto.objects.filter(cantidad__gt=0)

    productos_disponibles_str = ""
    for producto in productos:
        productos_disponibles_str += f"- {producto.nombre} ({producto.cantidad} unidades)\n"
    
    return productos_disponibles_str

def generar_respuesta_ia(model_name, productos_disponibles):
    model = GenerativeModel(model_name=model_name)
    
    prompt = f"""
    Eres un asistente de inventario. Basado en la siguiente lista de productos y sus cantidades, 
    genera una respuesta para el usuario, indicando qué productos están disponibles.
    No incluyas productos con cantidad cero. Si la lista de productos está vacía,
    informa al usuario que no hay productos disponibles en el inventario.

    Productos:
    {productos_disponibles}
    """

    response = model.generate_content(prompt)
    return response.text

def main():
    PROJECT_ID = "stone-poetry-473315-a9"
    LOCATION = "us-central1"
    MODEL_NAME = "gemini-2.5-flash"

    conectar_vertexai(PROJECT_ID, LOCATION)
    productos_disponibles = consultar_inventario_disponible()
    respuesta_ia = generar_respuesta_ia(MODEL_NAME, productos_disponibles)
    print(respuesta_ia)

if __name__ == '__main__':
    main()
