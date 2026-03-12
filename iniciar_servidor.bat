@echo off
:: Cambiar al directorio donde está este archivo
cd /d "%~dp0"

echo Activando entorno virtual...
call .venv\Scripts\activate

echo.
echo Iniciando servidor de Retoque de Imagen...
echo Puedes acceder en: http://localhost:8000
echo.
echo Cierra esta ventana para detener el servidor o usa detener_servidor.bat
echo.

:: Ejecutar uvicorn apuntando al módulo backend.main y la instancia app
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

pause
