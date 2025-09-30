🚀 Ejercicio #2: Inventario Inteligente con Django y IA
📋 El Desafío
El objetivo es desarrollar un sistema de inventario backend utilizando Python y Django. Este sistema gestionará un catálogo de productos almacenado en la base de datos por defecto, SQLite.

Requisitos de la Base de Datos:
Debe contener un mínimo de 4 productos de ejemplo.

Cada producto debe tener: nombre, descripción y cantidad.

Es crucial que al menos uno de los productos tenga una cantidad de cero (0) para simular y probar el manejo de stock agotado.

🎯 Entregable y Resultado Esperado
El entregable final es el proyecto Django completo junto con un script principal, consultar_inventario.py, que demuestra la interacción con la IA.

Funcionalidad Clave
Al ejecutar consultar_inventario.py, el script debe realizar una única acción: preguntarle a la IA qué productos están disponibles en el inventario.

La IA, a su vez, debe leer la base de datos y generar una respuesta en lenguaje natural, listando únicamente los productos cuyo stock sea mayor a cero.

Ejemplo de Ejecución
La salida en la terminal debe ser limpia y directa, como se muestra a continuación:

Shell

> python consultar_inventario.py

Hola, los productos disponibles en el inventario son:
* Teclado Mecánico RGB (15 unidades)
* Mouse Inalámbrico (30 unidades)
* Monitor 24 pulgadas (10 unidades)
