# Contexto del Proyecto: Retoque de Imagen Web (IA) 🖼️

Este archivo sirve para reiniciar el contexto de desarrollo con un asistente de IA.

## 🎯 Objetivo
Proyecto automatizado y visual para la **eliminación de logos y marcas de agua** mediante técnicas de enmascarado y clonación de texturas, utilizando Backend Python (FastAPI) y Frontend Web interactivo (Fabric.js).

## 📂 Arquitectura del Proyecto
1. **Frontend (`frontend/index.html`)**:
    - **Tecnología**: HTML5 + JavaScript + **Fabric.js**.
    - **Funcionalidad**: Carga la imagen en un lienzo (`canvas`) y permite dibujar y manipular objetos interactivos:
        - 🔴 **Rojo (Logo)**: Referencia visual.
        - 🔵 **Azul (Máscara)**: Área exacta donde se aplicará el borrado difuso.
        - 🟢 **Verde (Cielo)**: Área de origen para clonar textura limpia.
    - Envía la imagen (blob) y las coordenadas JSON al servidor.

2. **Backend (`backend/`)**:
    - **`main.py`**: Servidor **FastAPI**.
        - Endpoint `/`: Sirve el frontend.
        - Endpoint `/procesar` (POST): Recibe imagen y coordenadas, llama al procesador y devuelve la imagen limpia.
        - **Compatibilidad**: Incluye parche para `pydantic` en Python 3.14 (Beta).
    - **`processing.py`**: Lógica de imagen pura (Pillow).
        - Función `procesar_imagen_bytes()`: Recibe bytes y coordenadas, devuelve bytes procesados.
        - No depende del sistema de archivos, trabaja en memoria.

3. **Scripts de Utilidad**:
    - `iniciar_servidor.bat`: Lanza el servidor en `0.0.0.0:8000`.
    - `detener_servidor.bat`: Mata procesos en el puerto 8000.

## 🚀 Estado Actual (12-03-2026)
- **Funcionalidad Completa**: La aplicación web permite subir, ajustar áreas y descargar la imagen procesada.
- **Repositorio**: Estructura reorganizada (`backend/`, `frontend/`).
- **Problemas Conocidos y Resueltos**:
    - **Python 3.14**: Se aplicó un *shim* en `main.py` para corregir incompatibilidad de `typing._eval_type` con `pydantic`.
    - **CORS/Puertos**: Configurado para escuchar en `0.0.0.0` y permitir acceso local.

## 🔗 Stack Tecnológico
- **Python**: 3.14 (Beta)
- **Web Framework**: FastAPI + Uvicorn
- **Imagen**: Pillow (PIL)
- **Frontend**: Fabric.js (Canvas Interactivo)
