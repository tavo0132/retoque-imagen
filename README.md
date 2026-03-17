# Retoque de Imagen con Python + Web 🖼️

Aplicación web interactiva y modular para procesar imágenes con IA y Python. Incluye herramientas de retoque individual y procesamiento masivo para galerías web.

## 🚀 Características
### 1. 🖌️ Retoque Mágico (Individual)
- **Interfaz Web Interactiva**: Ajusta visualmente el área del logo, la máscara de borrado y la zona de clonación.
- **Enmascarado Suave**: Elimina marcas de agua usando bordes difuminados y clonación de texturas (cielo).

### 2. ⚙️ Galería Masiva (Nuevo)
- **Conversión por Lotes**: Sube múltiples imágenes y conviértelas a **WebP, PNG o JPG** de una sola vez.
- **Redimensionado Inteligente**: Genera automáticamente tamaños estándar para web:
    - **Thumb**: 370x250 px
    - **Big**: 741x521 px
- **Descarga en ZIP**: Recibe todas las imágenes procesadas en un archivo comprimido.

## 📋 Requisitos
- Python 3.x
- Librerías: `fastapi`, `uvicorn`, `python-multipart`, `Pillow`, `pillow-avif-plugin`

```bash
pip install fastapi uvicorn python-multipart Pillow pillow-avif-plugin
```

## 🔧 Uso
### Opción A: Scripts Automáticos (Windows)
1. Haz doble clic en **`iniciar_servidor.bat`**.
2. Se abrirá el navegador en `http://localhost:8000`.
3. Navega entre las pestañas "Retoque" y "Galería".

### Opción B: Manual
1. Ejecuta el servidor desde la terminal:
```bash
python -m uvicorn backend.main:app --reload
```

## 📂 Estructura del Proyecto
- `backend/`: Lógica del servidor (FastAPI) y procesamiento de imagen (Pillow).
- `frontend/`: Interfaz web (HTML + JS).
- `static/`, `templates/`: Archivos web.

## 👤 Autor
Gustavo (tavo0132)
