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
# Ajustamos la importación relativa según la estructura de paquetes
from .processing import procesar_imagen_bytes

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
async def read_root():
    # Servir el HTML principal
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

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
