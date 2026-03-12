@echo off
echo Buscando instancias del servidor (puerto 8000)...
echo.

:: Buscar PID escuchando en puerto 8000 y matarlo
for /f "tokens=5" %%a in ('netstat -aon ^| find "LISTENING" ^| find ":8000"') do (
    echo [INFO] Encontrado proceso (PID: %%a) en puerto 8000. Terminando...
    taskkill /f /pid %%a
)

echo.
echo Operacion completada.
pause
