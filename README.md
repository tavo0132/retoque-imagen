# Retoque de Imagen con Python + Web 🖼️

Aplicación web interactiva para eliminar logos y marcas de agua en imágenes utilizando técnicas de enmascarado y clonación de texturas. Permite ajustar visualmente las áreas de borrado directamente en el navegador.

## 🚀 Características
- **Interfaz Web Interactiva**: Ajusta visualmente el área del logo, la máscara de borrado y la zona de clonación (cielo) arrastrando cuadros sobre la imagen.
- **Backend Potente (FastAPI)**: Procesa las imágenes en tiempo real utilizando Python y Pillow.
- **Frontend Dinámico (Fabric.js)**: Lienzo interactivo html5 para manipulación fácil.
- **Detección Automática de Escala**: El backend se adapta a la resolución real de la imagen.
- **Enmascarado Suave**: Usa bordes difuminados (Gaussian Blur) para resultados naturales.

## 📋 Requisitos
- Python 3.x
- Librerías: `fastapi`, `uvicorn`, `python-multipart`, `Pillow`

```bash
pip install fastapi uvicorn python-multipart Pillow
```

## 🔧 Uso
### Opción A: Scripts Automáticos (Windows)
1. Haz doble clic en **`iniciar_servidor.bat`**.
2. Se abrirá el navegador automáticamente en `http://localhost:8000`.
3. Sube tu imagen, ajusta los cuadros de colores y dale a "Procesar".

### Opción B: Manual
1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta el servidor:
```bash
python -m uvicorn backend.main:app --reload
```
3. Ve a `http://localhost:8000`.

## 📂 Estructura del Proyecto
- `backend/`: Código Python del servidor y procesamiento de imagen.
- `frontend/`: Código HTML/JS de la interfaz web.
- `static/`, `templates/`: Archivos para el servidor web.
- `entrada/`, `salida/`: Carpetas para pruebas locales manuales (legacy).

## ⚙️ Ajustes Avanzados
El script de procesamiento base se encuentra en `backend/processing.py`.

## 👤 Autor
Gustavo (tavo0132)
