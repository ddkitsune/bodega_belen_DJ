@echo off
cls
color 0A
echo ============================================================
echo.
echo          BODEGA DE BELEN - Sistema de Ventas
echo.
echo ============================================================
echo.
echo  [*] Iniciando servidor Django...
echo  [*] Accede a: http://127.0.0.1:8000
echo.
echo  [!] Para detener el servidor presiona Ctrl+C
echo.
echo ============================================================
echo.

REM Ejecutar migraciones si es necesario
python manage.py migrate --noinput >nul 2>&1

REM Iniciar servidor
python manage.py runserver 127.0.0.1:8000

pause
