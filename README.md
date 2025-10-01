# 🚀 Ejercicio #2: Inventario Inteligente con Django y IA

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema de inventario backend utilizando Python y Django con integración de IA. El sistema gestiona un catálogo de productos almacenado en SQLite y permite consultar el inventario disponible mediante inteligencia artificial.

## 🎯 Funcionalidades

- Sistema de inventario con productos (nombre, descripción, cantidad)
- Base de datos SQLite para almacenamiento
- Integración con IA para consultas en lenguaje natural
- Script de consulta que lista solo productos con stock disponible

## 📦 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Google Cloud con Vertex AI habilitado
- Google Cloud CLI instalado (opcional, pero recomendado)

### Pasos para configurar el proyecto

1. **Clonar el repositorio**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd MCP_2
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Google Cloud (requerido para IA)**
   
   **Opción A: Autenticación con cuenta de servicio (recomendado para producción)**
   ```bash
   # Descarga el archivo JSON de credenciales de Google Cloud
   # Luego configura la variable de entorno:
   export GOOGLE_APPLICATION_CREDENTIALS="ruta/al/archivo/credenciales.json"
   ```
   
   **Opción B: Autenticación con gcloud CLI (recomendado para desarrollo)**
   ```bash
   # Instala Google Cloud CLI y autentica:
   gcloud auth application-default login
   ```
   
   **Importante:** Asegúrate de que tu proyecto de Google Cloud tenga habilitado Vertex AI y que el PROJECT_ID en `consultas.py` coincida con tu proyecto.

5. **Aplicar migraciones de la base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrations

   ```

6. **Crear datos de ejemplo si quiere mrd**
   ```bash
   python manage.py shell
   ```
   
   En el shell de Django, ejecuta:
   ```python
   from inventario.models import Productos
   
   # Crear productos de ejemplo
   Productos.objects.create(
       nombre="Teclado Mecánico RGB",
       descripcion="Teclado mecánico con retroiluminación RGB",
       cantidad=15
   )
   
   Productos.objects.create(
       nombre="Mouse Inalámbrico",
       descripcion="Mouse inalámbrico ergonómico",
       cantidad=30
   )
   
   Productos.objects.create(
       nombre="Monitor 24 pulgadas",
       descripcion="Monitor Full HD de 24 pulgadas",
       cantidad=10
   )
   
   Productos.objects.create(
       nombre="Auriculares Bluetooth",
       descripcion="Auriculares inalámbricos con cancelación de ruido",
       cantidad=0  # Producto sin stock
   )
   
   exit()
   ```
   
7. **Ejecutar el script de consulta**
   ```bash
   python consultar_inventario.py
   ```

## 🚀 Uso del Sistema

### Ejecutar consultas de inventario

```bash
python consultar_inventario.py
```
