import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import os
import io

# --- FUNCIONES DE UTILIDAD (Refactorizadas) ---

def procesar_imagen_bytes(imagen_bytes, coords_logo, coords_mask, coords_cielo):
    """
    Procesa una imagen recibida en bytes y devuelve la imagen procesada en bytes.
    Todas las coordenadas deben venir ya escaladas o ser absolutas para la imagen dada.
    Formato coordenadas: (x1, y1, x2, y2)
    """
    try:
        # 1. Cargar imagen desde memoria
        img = PIL.Image.open(io.BytesIO(imagen_bytes))
        img = img.convert("RGBA")
        ancho, alto = img.size
        print(f"Procesando imagen de {ancho}x{alto} píxeles...")

        # 2. Crear máscaras
        mask = PIL.Image.new("L", (ancho, alto), 0)
        draw = PIL.ImageDraw.Draw(mask)
        
        # Dibujar elipse de borrado
        draw.ellipse(coords_mask, fill=255)
        # Suavizar
        mask = mask.filter(PIL.ImageFilter.GaussianBlur(10))

        # 3. Crear parche de cielo
        # Validar coordenadas para evitar errores de recorte fuera de límites
        cielo_crop = (
            max(0, coords_cielo[0]), max(0, coords_cielo[1]),
            min(ancho, coords_cielo[2]), min(alto, coords_cielo[3])
        )
        muestra_cielo = img.crop(cielo_crop)
        parche_cielo = muestra_cielo.resize((ancho, alto))

        # 4. Pegar parche
        img.paste(parche_cielo, (0, 0), mask=mask)

        # 5. Guardar en memoria
        output_buffer = io.BytesIO()
        img.convert("RGB").save(output_buffer, format="JPEG", quality=95, optimize=True)
        return output_buffer.getvalue()
        
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return None


# --- NUEVA FUNCIÓN: PROCESAMIENTO MASIVO ---

def transformar_imagen(imagen_bytes, formato_salida="WEBP", ancho=None, alto=None, calidad=85):
    """
    Recibe imagen en bytes, la redimensiona (si se especifica) y la convierte de formato.
    Devuelve: (nombre_archivo_sugerido, bytes_imagen_procesada)
    """
    try:
        img = PIL.Image.open(io.BytesIO(imagen_bytes))
        
        # 1. Convertir a RGB (necesario si guardamos como JPG, aunque WebP soporta RGBA)
        if formato_salida.upper() in ["JPG", "JPEG"]:
            img = img.convert("RGB")
        
        # 2. Redimensionar (Resize) de alta calidad
        if ancho and alto:
            img = img.resize((ancho, alto), PIL.Image.Resampling.LANCZOS)
            
        # 3. Guardar en memoria con el nuevo formato
        output_buffer = io.BytesIO()
        img.save(output_buffer, format=formato_salida, quality=calidad, optimize=True)
        
        # Generar extensión correcta
        ext = formato_salida.lower().replace("jpeg", "jpg")
        return output_buffer.getvalue(), ext
        
    except Exception as e:
        print(f"Error transformando imagen: {e}")
        return None, None

# --- CÓDIGO LEGACY PARA TERMINAL (Solo si se ejecuta directo) ---
if __name__ == "__main__":
    # Rutas de archivos ajustadas a la estructura del proyecto
    # Subimos un nivel porque ahora estamos en /backend
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CARPETA_ENTRADA = os.path.join(BASE_DIR, "entrada")
    ARCHIVO_ENTRADA = "1.jpg"
    ARCHIVO_SALIDA = "1_sin_logo.jpg"
    
    # ... (Resto del código original adaptado mínimamente) ...
    # Por simplicidad, aquí dejo funcional solo la parte de importación para la API
    print("Este script ahora está optimizado para ser importado por el servidor web.")
    print("Para ejecutarlo manualmente, usa el código antiguo o adapta las rutas.")
