@echo off
chcp 65001 >nul
echo ═══════════════════════════════════════════════════════════
echo   🔄 ACTUALIZACIÓN SEGURA - Bodega de Belén
echo ═══════════════════════════════════════════════════════════
echo.
echo Este script te ayudará a actualizar el sistema de forma segura
echo manteniendo todos tus datos intactos.
echo.
pause

REM Paso 1: Verificar que existe la base de datos
echo.
echo [1/5] 🔍 Verificando archivos...
if not exist "db.sqlite3" (
    echo ❌ No se encontró db.sqlite3
    echo.
    echo Si es una instalación nueva, puedes continuar.
    echo Si estás actualizando, asegúrate de estar en la carpeta correcta.
    echo.
    set /p CONTINUAR="¿Continuar de todos modos? (S/N): "
    if /i not "%CONTINUAR%"=="S" exit /b 1
) else (
    echo ✅ Base de datos encontrada
)

REM Paso 2: Crear backup automático
echo.
echo [2/5] 💾 Creando backup de seguridad...
if exist "db.sqlite3" (
    for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
    set FECHA=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%
    set HORA=%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%
    
    if not exist "Backups" mkdir Backups
    if not exist "Backups\%FECHA%" mkdir "Backups\%FECHA%"
    
    copy "db.sqlite3" "Backups\%FECHA%\db_backup_%FECHA%_%HORA%.sqlite3" >nul
    
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Backup creado: Backups\%FECHA%\db_backup_%FECHA%_%HORA%.sqlite3
    ) else (
        echo ❌ ERROR: No se pudo crear el backup
        echo.
        echo IMPORTANTE: No continúes sin un backup!
        pause
        exit /b 1
    )
) else (
    echo ℹ️  No hay base de datos para respaldar (instalación nueva)
)

REM Paso 3: Verificar que el nuevo ejecutable existe
echo.
echo [3/5] 📦 Verificando nueva versión...
if not exist "BodegaBelen_NUEVO.exe" (
    echo.
    echo ⚠️  Instrucciones:
    echo.
    echo 1. Descarga la nueva versión de BodegaBelen.exe
    echo 2. Renómbrala a: BodegaBelen_NUEVO.exe
    echo 3. Colócala en esta misma carpeta
    echo 4. Ejecuta este script nuevamente
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Nueva versión encontrada
)

REM Paso 4: Cerrar procesos existentes
echo.
echo [4/5] 🛑 Cerrando procesos anteriores...
taskkill /F /IM BodegaBelen.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Proceso anterior cerrado
    timeout /t 2 >nul
) else (
    echo ℹ️  No había procesos en ejecución
)

REM Paso 5: Reemplazar ejecutable
echo.
echo [5/5] 🔄 Actualizando ejecutable...

REM Hacer backup del ejecutable anterior
if exist "BodegaBelen.exe" (
    if not exist "Backups\ejecutables" mkdir "Backups\ejecutables"
    copy "BodegaBelen.exe" "Backups\ejecutables\BodegaBelen_OLD_%FECHA%.exe" >nul
    echo ✅ Ejecutable anterior respaldado
    
    REM Eliminar el ejecutable anterior
    del "BodegaBelen.exe" >nul 2>&1
)

REM Renombrar el nuevo ejecutable
ren "BodegaBelen_NUEVO.exe" "BodegaBelen.exe" >nul

if %ERRORLEVEL% EQU 0 (
    echo ✅ Ejecutable actualizado correctamente
) else (
    echo ❌ ERROR al renombrar el ejecutable
    pause
    exit /b 1
)

REM Resumen final
echo.
echo ═══════════════════════════════════════════════════════════
echo   ✅ ACTUALIZACIÓN COMPLETADA
echo ═══════════════════════════════════════════════════════════
echo.
echo 📋 Resumen:
echo   • Base de datos respaldada ✅
echo   • Ejecutable actualizado ✅
echo   • Tus datos están seguros ✅
echo.
echo 🚀 Próximos pasos:
echo   1. Ejecuta BodegaBelen.exe
echo   2. El sistema aplicará las migraciones automáticamente
echo   3. Verifica que todos tus datos estén presentes
echo.
echo 💡 Consejo: Guarda los backups por al menos 7 días
echo.
echo ═══════════════════════════════════════════════════════════

REM Preguntar si desea ejecutar el programa
echo.
set /p EJECUTAR="¿Deseas ejecutar el programa ahora? (S/N): "
if /i "%EJECUTAR%"=="S" (
    echo.
    echo 🚀 Iniciando Bodega de Belén...
    start "" "BodegaBelen.exe"
)

echo.
pause
