@echo off
chcp 65001 >nul
echo ═══════════════════════════════════════════════════════════
echo   🔙 RESTAURAR BACKUP - Bodega de Belén
echo ═══════════════════════════════════════════════════════════
echo.
echo Este script te ayudará a restaurar una copia de seguridad
echo de tu base de datos.
echo.
echo ⚠️  ADVERTENCIA: Esto reemplazará la base de datos actual
echo    con una versión anterior. Todos los cambios realizados
echo    después del backup se perderán.
echo.
pause

REM Verificar que existe la carpeta de backups
if not exist "Backups" (
    echo ❌ ERROR: No se encontró la carpeta de Backups
    echo.
    echo No hay backups disponibles para restaurar.
    pause
    exit /b 1
)

REM Listar backups disponibles
echo.
echo 📂 Backups disponibles:
echo.
echo ─────────────────────────────────────────────────────────
dir /b /s Backups\*.sqlite3
echo ─────────────────────────────────────────────────────────
echo.

REM Solicitar la ruta del backup
echo Copia y pega la ruta completa del backup que deseas restaurar:
echo (Ejemplo: Backups\2026-01-18\db_backup_2026-01-18_14-30-00.sqlite3)
echo.
set /p BACKUP_PATH="Ruta del backup: "

REM Verificar que el archivo existe
if not exist "%BACKUP_PATH%" (
    echo.
    echo ❌ ERROR: El archivo especificado no existe
    echo.
    echo Verifica que la ruta sea correcta.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   ⚠️  CONFIRMACIÓN
echo ═══════════════════════════════════════════════════════════
echo.
echo Estás a punto de restaurar:
echo   📁 %BACKUP_PATH%
echo.
echo Esto reemplazará:
echo   📁 db.sqlite3 (actual)
echo.
set /p CONFIRMAR="¿Estás seguro? (S/N): "

if /i not "%CONFIRMAR%"=="S" (
    echo.
    echo ❌ Restauración cancelada
    pause
    exit /b 0
)

REM Cerrar procesos
echo.
echo 🛑 Cerrando procesos...
taskkill /F /IM BodegaBelen.exe >nul 2>&1
timeout /t 2 >nul

REM Hacer backup de la base de datos actual antes de restaurar
if exist "db.sqlite3" (
    echo.
    echo 💾 Respaldando base de datos actual...
    
    for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
    set FECHA=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%
    set HORA=%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%
    
    if not exist "Backups\pre-restauracion" mkdir "Backups\pre-restauracion"
    copy "db.sqlite3" "Backups\pre-restauracion\db_antes_restaurar_%FECHA%_%HORA%.sqlite3" >nul
    
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Base de datos actual respaldada
    ) else (
        echo ⚠️  No se pudo respaldar la base de datos actual
    )
)

REM Restaurar el backup
echo.
echo 🔄 Restaurando backup...
copy /Y "%BACKUP_PATH%" "db.sqlite3" >nul

if %ERRORLEVEL% EQU 0 (
    echo ✅ Backup restaurado exitosamente
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo   ✅ RESTAURACIÓN COMPLETADA
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo 📋 Resumen:
    echo   • Backup restaurado: %BACKUP_PATH%
    echo   • Base de datos actual respaldada en: Backups\pre-restauracion\
    echo.
    echo 🚀 Próximos pasos:
    echo   1. Ejecuta BodegaBelen.exe
    echo   2. Verifica que tus datos estén correctos
    echo.
) else (
    echo ❌ ERROR: No se pudo restaurar el backup
    echo.
    echo Verifica que:
    echo - El archivo de backup no esté corrupto
    echo - Tienes permisos de escritura en esta carpeta
)

echo.
pause
