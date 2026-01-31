@echo off
chcp 65001 >nul
echo ═══════════════════════════════════════════════════════════
echo   🔄 BACKUP AUTOMÁTICO - Bodega de Belén
echo ═══════════════════════════════════════════════════════════
echo.

REM Obtener fecha y hora actual
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set FECHA=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%
set HORA=%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%

REM Crear carpeta de backups si no existe
if not exist "Backups" mkdir Backups
if not exist "Backups\%FECHA%" mkdir "Backups\%FECHA%"

REM Verificar si existe la base de datos
if not exist "db.sqlite3" (
    echo ❌ ERROR: No se encontró el archivo db.sqlite3
    echo.
    echo Asegúrate de ejecutar este script en la misma carpeta
    echo donde está el archivo BodegaBelen.exe y db.sqlite3
    pause
    exit /b 1
)

REM Copiar la base de datos
echo 📦 Creando backup de la base de datos...
copy "db.sqlite3" "Backups\%FECHA%\db_%FECHA%_%HORA%.sqlite3" >nul

if %ERRORLEVEL% EQU 0 (
    echo ✅ Backup creado exitosamente!
    echo.
    echo 📂 Ubicación: Backups\%FECHA%\db_%FECHA%_%HORA%.sqlite3
    echo 📊 Tamaño: 
    dir "Backups\%FECHA%\db_%FECHA%_%HORA%.sqlite3" | find "db_"
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo   ✅ BACKUP COMPLETADO
    echo ═══════════════════════════════════════════════════════════
) else (
    echo ❌ ERROR: No se pudo crear el backup
    echo.
    echo Verifica que:
    echo - El archivo db.sqlite3 no esté en uso
    echo - Tienes permisos de escritura en esta carpeta
)

echo.
pause
