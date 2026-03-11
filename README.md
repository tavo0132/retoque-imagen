# Retoque de Imagen con Python 🖼️

Este script automatiza la eliminación de logos y marcas de agua en imágenes o collages. Utiliza la librería **Pillow** para detectar áreas específicas, aplicar máscaras difuminadas y clonar texturas de fondo (como el cielo) para rellenar el espacio eliminado de forma natural.

## 🚀 Características
- **Detección Automática de Escala**: Se adapta a imágenes de diferentes resoluciones (1024px, 1632px, etc.) recalculando las coordenadas proporcionalmente.
- **Enmascarado Suave**: Usa bordes difuminados (Gaussian Blur) para que no se noten los cortes.
- **Historial de Ejecuciones**: Guarda cada resultado en carpetas organizadas por fecha y número de ejecución (ej. `salida/11-03-2026_1`).
- **Modo Debug**: Genera una imagen `debug_areas.jpg` mostrando exactamente qué áreas se están borrando y clonando para facilitar ajustes.

## 📋 Requisitos
- Python 3.x
- Librería Pillow

```bash
pip install Pillow
```

## 🔧 Uso
1. Coloca tu imagen en la carpeta `entrada/` (por defecto busca `1.jpg`, configurable en el script).
2. Ejecuta el script:

```bash
python retoque_imagen.py
```

3. Revisa la carpeta `salida/` más reciente para ver el resultado.

## ⚙️ Ajustes
Puedes modificar las coordenadas de borrado directamente en el archivo `retoque_imagen.py` buscando la sección:
`# Coordenadas base (Originales 1024x575)`

## 👤 Autor
Gustavo (tavo0132)
