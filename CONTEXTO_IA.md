# Contexto del Proyecto: Retoque de Imagen (IA) 🤖

Este archivo sirve para reiniciar el contexto de desarrollo con un asistente de IA en caso de perder el historial de chat.

## 🎯 Objetivo
El proyecto busca automatizar la **eliminación de logos y marcas de agua** en imágenes (específicamente en cielos o fondos uniformes) mediante técnicas de clonación y enmascarado difuso.

## 📂 Estructura del Proyecto
- **`retoque_imagen.py`**: Script principal.
    - Usa **Pillow (PIL)**.
    - Detecta automáticamente el tamaño de la imagen y reescala las coordenadas de borrado.
    - Genera una **máscara suave** (Gaussian Blur) para integrar el parche.
    - Toma una muestra de textura (ej. cielo) de otro lado de la imagen para tapar el logo.
    - Crea carpetas de salida incrementales: `salida/DD-MM-YYYY_N`.
    - Genera imagen de debug: `debug_areas.jpg` (muestra cajas rojas/verdes/azules de las zonas afectadas).
- **`entrada/`**: Carpeta donde se pone la imagen original (por defecto busca `1.jpg`).
- **`salida/`**: Carpeta donde se guardan los resultados.

## ⚙️ Configuración Clave (Coordenadas)
Las coordenadas base en `retoque_imagen.py` están calibradas para una resolución de referencia de **1024x575** y se escalan automáticamente.
- **Caja Logo (Rojo)**: Área aproximada a borrar.
- **Elipse Máscara (Azul)**: Forma exacta del borrado (con bordes difuminados).
- **Muestra Cielo (Verde)**: Área desde donde se clona la textura limpia.

*Si el logo cambia de sitio, estas son las coordenadas que hay que editar en el script.*

## 🚀 Estado Actual (11-03-2026)
- El script es funcional y se ha ajustado para mover el área de borrado hacia la derecha y arriba según las necesidades del usuario.
- El proyecto está versionado en **Git local** y subido a **GitHub**.
- Repositorio: `https://github.com/tavo0132/retoque-imagen`

## 🔜 Pasos Futuros (Pendientes)
- Hacer que el nombre del archivo de entrada sea un argumento de línea de comandos o recorra todos los archivos de la carpeta `entrada/`.
- Mejorar la interfaz o hacerlo ejecutable (.exe) si fuera necesario.
