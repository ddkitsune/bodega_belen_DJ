@echo off
REM ============================================
REM  BODEGA DE BELÉN - Sistema de Ventas
REM  Script de Inicio Rápido
REM ============================================

title Bodega de Belén - Sistema de Ventas

REM Cambiar al directorio del script
cd /d "%~dp0"

echo ============================================
echo    BODEGA DE BELÉN - SISTEMA DE VENTAS
echo ============================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] No se encuentra el entorno virtual
    echo Por favor ejecuta primero: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [1/3] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar que Django esté instalado
python -c "import django" 2>nul
if errorlevel 1 (
    echo [ERROR] Django no está instalado
    echo Por favor ejecuta: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [2/3] Abriendo navegador...
start http://127.0.0.1:8000

echo [3/3] Iniciando servidor Django...
echo.
echo ============================================
echo  Servidor corriendo en: http://127.0.0.1:8000
echo.
echo  NO CIERRES ESTA VENTANA
echo  Para detener: presiona Ctrl+C
echo ============================================
echo.

REM Iniciar servidor Django
python manage.py runserver 127.0.0.1:8000

pause
