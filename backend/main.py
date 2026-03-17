import typing

# --- PARCHE DE COMPATIBILIDAD PYTHON 3.14 (BETA) ---
# Pydantic intenta usar un argumento 'prefer_fwd_module' que ha sido eliminado en Python 3.14.
# Este parche intercepta la llamada interna y elimina ese argumento para evitar el error.
if hasattr(typing, "_eval_type"):
    original_eval_type = typing._eval_type
    def patched_eval_type(t, globalns, localns, *args, **kwargs):
        if "prefer_fwd_module" in kwargs:
            del kwargs["prefer_fwd_module"]
        return original_eval_type(t, globalns, localns, *args, **kwargs)
    typing._eval_type = patched_eval_type
# ---------------------------------------------------

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
import io
import zipfile
from fastapi.responses import JSONResponse
from typing import List

# Ajustamos la importaciÃ³n relativa segÃºn la estructura de paquetes
from .processing import procesar_imagen_bytes, transformar_imagen

app = FastAPI()

# Configurar CORS (Permitir todo en desarrollo local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(): # Eliminamos async innecesario para lectura directa de archivo
    # Servir el HTML principal
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

@app.post("/procesar-galeria")
async def procesar_galeria(
    files: List[UploadFile] = File(...),
    tipo_salida: str = Form("thumb"), # "thumb" (370x250) | "big" (741x521)
    formato: str = Form("WEBP")       # WEBP | PNG | JPEG
):
    """
    Recibe múltiples imágenes, las redimensiona según el tipo (thumb/big) 
    y las devuelve comprimidas en un ZIP.
    Simula la estructura de carpetas de tu web.
    """
    try:
        # Definir dimensiones según la plantilla
        if tipo_salida == "thumb":
            ANCHO, ALTO = 370, 250
        elif tipo_salida == "big":
            ANCHO, ALTO = 741, 521
        else:
            return JSONResponse({"error": "Tipo de salida no válido"}, status_code=400)
        
        # Buffer en memoria para el ZIP resultante
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                contenido = await file.read()
                
                # Procesar imagen individual
                img_bytes, ext = transformar_imagen(
                    contenido, 
                    formato_salida=formato, 
                    ancho=ANCHO, 
                    alto=ALTO
                )
                
                if img_bytes:
                    # Crear nombre: "foto1.jpg" -> "foto1.webp"
                    # Usamos rsplit para quitar la extensión original de forma segura
                    nombre_base = file.filename.rsplit('.', 1)[0]
                    nombre_final = f"{nombre_base}.{ext}"
                    
                    # Añadir al ZIP
                    zip_file.writestr(nombre_final, img_bytes)
        
        # Preparar respuesta como descarga de archivo
        zip_buffer.seek(0)
        
        # Limpiar headers para evitar errores de codificación
        filename = f"galeria_{tipo_salida}.zip"
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        return Response(content=zip_buffer.getvalue(), media_type="application/zip", headers=headers)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/procesar")
async def procesar(
    file: UploadFile = File(...),
    coords: str = Form(...)  # Recibimos un JSON stringify con todas las coordenadas
):
    try:
        # 1. Leer imagen
        image_bytes = await file.read()
        
        # 2. Parsear coordenadas
        data = json.loads(coords)
        # { 'mask': {left, top, width, height}, 'cielo': ... }
        
        # Convertir [left, top, width, height] -> (x1, y1, x2, y2) para Pillow
        def to_box(rect):
            return (
                int(rect['left']), 
                int(rect['top']), 
                int(rect['left'] + rect['width']), 
                int(rect['top'] + rect['height'])
            )
        
        c_mask = to_box(data['mask'])
        c_cielo = to_box(data['cielo'])
        
        # 3. Procesar
        # Le pasamos None como coords_logo porque no lo usa para procesar, solo mask y cielo
        # Pero mi funcion espera (img, logo, mask, cielo) -> (img, mask, cielo) ???
        # Revisa processing.py: procesar_imagen_bytes(imagen_bytes, coords_logo, coords_mask, coords_cielo)
        resultado_bytes = procesar_imagen_bytes(image_bytes, None, c_mask, c_cielo)
        
        if resultado_bytes:
             return Response(content=resultado_bytes, media_type="image/jpeg")
        else:
            return Response(content="Error al procesar la imagen", status_code=500)

    except Exception as e:
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    # Ejecutar servidor en puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
