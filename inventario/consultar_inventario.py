import os
import django
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de .env
load_dotenv()

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
django.setup()

from productos.models import Producto

def consultar_inventario():

    # Obtener productos disponibles
    disponibles = Producto.objects.filter(cantidad__gt=0)
    lista = "\n".join([f"{p.nombre} ({p.cantidad} unidades)" for p in disponibles])

    if not lista:
        lista = "No hay productos disponibles en el inventario."

    # Configurar Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No encontré la variable GEMINI_API_KEY. Configúrala primero.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Eres un asistente. 
    Muestra los productos disponibles en el inventario en este formato exacto:
    
    Hola, los productos disponibles en el inventario son:
    Lista de productos:
    {lista}
    """

    response = model.generate_content(prompt)
    print(response.text)

if __name__ == "__main__":
    consultar_inventario()
