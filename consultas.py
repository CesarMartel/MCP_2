#paso 1 biblioteca y configuracion
from dis import Instruction
import os
import vertexai
import json

from  vertexai.generative_models import GenerativeModel

# Reemplaza con los datos de tu proyecto de Google Cloud
# Asegúrate de haber instalado 'google-cloud-aiplatform'
PROJECT_ID = "stone-poetry-473315-a9"
LOCATION = "us-central1"

PRIMARY_MODEL = "gemini-1.5-flash"

#configuracion de djangopara usar los modelos ORM
def _django_bootstrap() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuracion.settings")
    os.environ.setdefault("GRPC_VERBOSITY", "NONE")
    os.environ.setdefault("GRPC_TRACE", "")
    import django
    django.setup()


def listar_productos(only_available: bool = False):
    from inventario.models import Productos

    producto = Productos.objects.all().order_by("nombre")
    if only_available:
        producto = producto.filter(cantidad__gt=0)
    return [{"id": p.id, "nombre": p.nombre, "cantidad": p.cantidad, "descripcion": p.descripcion} for p in producto]

def agregar_producto(nombre: str, cantidad: int, descripcion: str):
    from inventario.models import Productos

    objeto = Productos.objects.create(nombre=nombre, cantidad=max(0, cantidad), descripcion=descripcion)
    return {"id": objeto.id, "nombre": objeto.nombre, "cantidad": objeto.cantidad, "descripcion": objeto.descripcion}

def actualizar_producto(id: int, nombre: str, cantidad: int, descripcion: str):
    from inventario.models import Productos

    objeto = Productos.objects.filter(id=id).first()
    if objeto is None:
        raise ValueError("Producto no encontrado")
    objeto.nombre = nombre
    objeto.cantidad = max(0, cantidad)
    objeto.descripcion = descripcion
    objeto.save()
    return {"id": objeto.id, "nombre": objeto.nombre, "cantidad": objeto.cantidad, "descripcion": objeto.descripcion}

def eliminar_producto(id: int):
    from inventario.models import Productos
    return Productos.objects.filter(id=id).delete()[0]

SYSTEM_INSTRUCTIONS = (
    "Eres un asistente que convierte instrucciones en una orden JSON. "
    "No expliques, solo responde con JSON válido. Campos: \n"
    "acciones que puedes realizar: ver inventario, añadir producto, actualizar producto, eliminar producto, salir"
    "nombre: string|null, cantidad: int|null, descripcion: string|null, id: int|null"
    "ejemplos: \n"
    "- 'ver inventario' -> {\"accion\":\"ver_inventario\", \"nombre\":null, \"cantidad\":null, \"descripcion\":null, \"id\":null}\n"
    "- 'añadir producto' -> {\"accion\":\"añadir_producto\", \"nombre\":null, \"cantidad\":null, \"descripcion\":null, \"id\":null}\n"
    "- 'actualizar producto' -> {\"accion\":\"actualizar_producto\", \"nombre\":null, \"cantidad\":null, \"descripcion\":null, \"id\":null}\n"
    "- 'eliminar producto' -> {\"accion\":\"eliminar_producto\", \"nombre\":null, \"cantidad\":null, \"descripcion\":null, \"id\":null}\n"
    "- 'salir' -> {\"accion\":\"salir\", \"nombre\":null, \"cantidad\":null, \"descripcion\":null, \"id\":null}\n"
)

def llamada_modelo(user_text: str):
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    last_error: Exception | None = None
    for model_nombre in (PRIMARY_MODEL,):
        try:
            model = GenerativeModel(model_nombre)
            prompt = f"{SYSTEM_INSTRUCTIONS}\nUsuario: {user_text}\nJSON:"
            resp = model.generate_content(prompt)
            text = resp.text if hasattr(resp, "text") else str(resp)
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                text = text[start : end + 1]
            return json.loads(text)

        except Exception as e:
            last_error = e
            continue
    assert last_error is not None
    raise last_error

def frases_comunes(user_text: str):
    t = user_text.strip().lower()
    if any(word in t for word in ["listar", "ver", "mostrar", "inventario", "muestrame", "que hay", "muestrame todo lo que tengas", "muestra","tienes"]):
        return {"accion": "listar", "nombre": None, "cantidad": None, "descripcion": None, "id": None}
    if any(word in t for word in ["agregar", "añadir", "agregue", "añada", "agrega", "añade"]):
        return {"accion": "añadir", "nombre": None, "cantidad": None, "descripcion": None, "id": None}
    if any(word in t for word in ["actualizar", "cambiar", "modificar", "editar"]):
        return {"accion": "actualizar", "nombre": None, "cantidad": None, "descripcion": None, "id": None}
    if any(word in t for word in ["eliminar", "borrar", "quitar", "delete", "sacar", "no deseo tener", "no deseo que tengas"]):
        return {"accion": "eliminar", "nombre": None, "cantidad": None, "descripcion": None, "id": None}
    if t in {"salir", "exit", "quit", "terminar", "terminar el programa", "terminar el asistente", "no quiero estar aqui", "safo," "me voy"}:
        return {"accion": "salir", "nombre": None, "cantidad": None, "descripcion": None, "id": None}
    return None

def mostrar_capacidades():
    """Muestra las acciones disponibles para el usuario."""
    print("\nCAPACIDADES DISPONIBLES:")
    print("- inventario: Ver todo el inventario")
    print("- añadir: Agregar nuevo producto") 
    print("- actualizar: Modificar producto existente")
    print("- eliminar: Borrar producto")

def entrada():
    _django_bootstrap()
    
    print("\nSISTEMA DE INVENTARIO")
    
    productos = listar_productos(only_available=False)
    print("\nINVENTARIO ACTUAL:")
    if not productos:
        print("(El inventario está vacío)")
    else:
        for p in productos:
            disponible = "SI" if p['cantidad'] > 0 else "NO"
            print(f"ID {p['id']}: {p['nombre']} - Cantidad: {p['cantidad']} - {p['descripcion']} (Disponible: {disponible})")

    mostrar_capacidades()
    
    while True:
        try:
            user_text = input("\n¿Qué deseas hacer? ").strip()
        except EOFError:
            break
        
        if not user_text:
            continue

        try:
            intent = frases_comunes(user_text) or llamada_modelo(user_text)
        except Exception as e:
            print(f"No pude interpretar la instrucción: {e}")
            continue

        accion = intent.get("accion")
        nombre = intent.get("nombre")
        cantidad = intent.get("cantidad")
        descripcion = intent.get("descripcion")
        pid = intent.get("id")

        try:
            if accion == "salir":
                print("Hasta luego!")
                break
                
            if accion is None:
                print("No entendí la acción. Intenta de nuevo.")
                
            elif accion == "listar":
                print("\nINVENTARIO COMPLETO:")
                productos = listar_productos(only_available=False)
                if not productos:
                    print("(El inventario está vacío)")
                else:
                    for p in productos:
                        disponible = "SI" if p['cantidad'] > 0 else "NO"
                        print(f"ID {p['id']}: {p['nombre']} - Cantidad: {p['cantidad']} - {p['descripcion']} (Disponible: {disponible})")
                        
            elif accion == "añadir":
                print("\nAGREGAR NUEVO PRODUCTO")
                if not nombre:
                    nombre = input("Nombre del producto: ").strip()
                    while not nombre:
                        nombre = input("Nombre del producto: ").strip()
                        
                if not isinstance(cantidad, int):
                    while True:
                        qtxt = input("Cantidad: ").strip()
                        try:
                            cantidad = int(qtxt)
                            break
                        except ValueError:
                            print("Ingresa un número entero.")
                            
                if not descripcion:
                    descripcion = input("Descripción: ").strip()
                created = agregar_producto(nombre=nombre, cantidad=int(cantidad), descripcion=descripcion)
                print(f"Producto agregado: ID {created['id']} - {created['nombre']} ({created['cantidad']}) - {created['descripcion']}")
                
            elif accion == "actualizar":
                print("\nACTUALIZAR PRODUCTO")
                if pid is None:
                    while True:
                        id_txt = input("ID del producto: ").strip()
                        try:
                            pid = int(id_txt)
                            break
                        except ValueError:
                            print("Ingresa un número entero para el ID.")
                
                if not nombre:
                    nombre = input("Nuevo nombre: ").strip()
                    while not nombre:
                        nombre = input("Nuevo nombre: ").strip()
                
                if not isinstance(cantidad, int):
                    while True:
                        qtxt = input("Cantidad: ").strip()
                        try:
                            cantidad = int(qtxt)
                            break
                        except ValueError:
                            print("Ingresa un número entero.")
                
                if not descripcion:
                    descripcion = input("Descripción: ").strip()
                
                try:
                    updated = actualizar_producto(id=pid, nombre=nombre, cantidad=int(cantidad), descripcion=descripcion)
                    print(f"Producto actualizado: ID {updated['id']} - {updated['nombre']} ({updated['cantidad']}) - {updated['descripcion']}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif accion == "eliminar":
                print("\nELIMINAR PRODUCTO")
                if pid is None and not nombre:
                    sel = input("ID o nombre del producto: ").strip()
                    if sel.isdigit():
                        pid = int(sel)
                    else:
                        nombre = sel
                        
                try:
                    deleted = eliminar_producto(id=pid)
                    if deleted:
                        print("Producto eliminado exitosamente")
                    else:
                        print("No se encontró el producto")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            else:
                print("Acción no reconocida. Usa: inventario, añadir, actualizar, eliminar")
                
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    entrada()