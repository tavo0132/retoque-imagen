import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import os
from datetime import datetime

# Rutas de archivos ajustadas a la estructura del proyecto
CARPETA_ENTRADA = "entrada"
ARCHIVO_ENTRADA = "1.jpg"
ARCHIVO_SALIDA = "1_sin_logo.jpg"

# --- LÓGICA DE CARPETAS INCREMENTALES ---
# Generar nombre de carpeta único: DD-MM-YYYY_N
fecha_actual = datetime.now().strftime("%d-%m-%Y")
contador = 1
while True:
    nombre_carpeta = f"{fecha_actual}_{contador}"
    CARPETA_SALIDA = os.path.join("salida", nombre_carpeta)
    if not os.path.exists(CARPETA_SALIDA):
        break
    contador += 1

# Crear la carpeta específica para esta ejecución
os.makedirs(CARPETA_SALIDA, exist_ok=True)
print(f"--- Nueva ejecución ---")
print(f"Carpeta de salida: {CARPETA_SALIDA}")
# ----------------------------------------

ruta_entrada = os.path.join(CARPETA_ENTRADA, ARCHIVO_ENTRADA)
ruta_salida = os.path.join(CARPETA_SALIDA, ARCHIVO_SALIDA)

try:
    print(f"Buscando imagen en: {ruta_entrada}")
    
    # 1. Cargar la imagen original
    img = PIL.Image.open(ruta_entrada)
    img = img.convert("RGBA")
    ancho, alto = img.size
    print(f"Procesando imagen de {ancho}x{alto} píxeles...")

    # --- LÓGICA DE RECALCULO AUTOMÁTICO ---
    # Dimensiones de referencia (donde funcionaban las coordenadas originales)
    REF_ANCHO = 1024
    REF_ALTO = 575

    # Factores de escala
    fx = ancho / REF_ANCHO
    fy = alto / REF_ALTO
    print(f"Factores de escala calculados -> Ancho: {fx:.2f}x, Alto: {fy:.2f}x")

    def escalar_rect(rect):
        """Escala una tupla (x1, y1, x2, y2) por los factores calculaods"""
        return (
            int(rect[0] * fx), int(rect[1] * fy),
            int(rect[2] * fx), int(rect[3] * fy)
        )

    # Coordenadas base (Originales 1024x575) - MODIFICAR AQUÍ SI ES NECESARIO
    # Formato: (Izquierda, Arriba, Derecha, Abajo)
    
    # 1. Caja Roja: Área aproximada del logo (Moviendo a la derecha y arriba)
    base_caja_logo = (480, 50, 630, 210)    
    
    # 2. Elipse Azul: Máscara de borrado (Debe cubrir el logo completamente)
    #    (Haciéndola un poco más pequeña y movida igual que el logo)
    base_elipse    = (480, 40, 630, 220)    
    
    # 3. Caja Verde: Área de donde copiamos el cielo
    #    (Moviendo a la derecha, acercándonos al logo sin tocarlo)
    base_cielo     = (440, 100, 470, 180)   

    # Coordenadas recalculadas
    caja_logo = escalar_rect(base_caja_logo)
    elipse_mask = escalar_rect(base_elipse)
    cielo_rect = escalar_rect(base_cielo)

    print(f"Nuevas coordenadas logo: {caja_logo}")
    print(f"Nuevas coordenadas cielo: {cielo_rect}")

    # --- GENERAR IMAGEN DE DIAGNÓSTICO ---
    # Para verificar qué estamos borrando
    debug_img = img.copy()
    debug_draw = PIL.ImageDraw.Draw(debug_img)
    # Rectángulo ROJO = Área que se va a borrar (aprox)
    debug_draw.rectangle(caja_logo, outline="red", width=5)
    # Rectángulo VERDE = Área de donde sacamos el cielo
    debug_draw.rectangle(cielo_rect, outline="green", width=5)
    # Elipse AZUL = La máscara de suavizado real
    debug_draw.ellipse(elipse_mask, outline="blue", width=3)
    
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    debug_path = os.path.join(CARPETA_SALIDA, "debug_areas.jpg")
    debug_img.convert("RGB").save(debug_path)
    print(f"Generada imagen de diagnóstico: {debug_path}")
    # --------------------------------------

    # 3. Crear una máscara suave para que la mezcla no se note
    mask = PIL.Image.new("L", (ancho, alto), 0)
    draw = PIL.ImageDraw.Draw(mask)
    # Dibujar una elipse suave sobre el logo usando coords recalculadas
    draw.ellipse(elipse_mask, fill=255)
    # Desenfocar la máscara para suavizar los bordes
    mask = mask.filter(PIL.ImageFilter.GaussianBlur(10))

    # 4. Crear un parche de cielo limpio
    # Tomamos una muestra de cielo usando coords recalculadas
    muestra_cielo = img.crop(cielo_rect) 
    parche_cielo = muestra_cielo.resize((ancho, alto)) # Estirarlo al tamaño total

    # 5. Pegar el parche usando la máscara suave
    # Esto reemplazará SOLO la zona del logo con el cielo limpio
    img.paste(parche_cielo, (0, 0), mask=mask)

    # 6. Guardar como JPG de alta calidad preservando dimensiones
    # Convertir de vuelta a RGB para JPG
    imagen_final = img.convert("RGB")
    
    # Asegurar que existe la carpeta de salida
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    
    # Guardar con calidad 95 para no perder nitidez y optimizar peso
    imagen_final.save(ruta_salida, "JPEG", quality=95, optimize=True)

    print(f"¡Éxito! Tu imagen limpia se ha guardado en '{ruta_salida}'.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{ruta_entrada}'. \nAsegúrate de que 'collage_original.png' esté dentro de la carpeta '{CARPETA_ENTRADA}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
