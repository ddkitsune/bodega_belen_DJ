"""
Script de lanzamiento unificado para Bodega de Belén.
Diseñado para funcionar tanto en desarrollo como en modo congelado (EXE).
"""
import os
import sys
import webbrowser
import threading
import time
from pathlib import Path
import traceback

# Configurar entorno Django antes de importar nada de Django
# Determinar si estamos corriendo como ejecutable
if getattr(sys, 'frozen', False):
    # Si es exe, el directorio base es donde está el ejecutable
    BASE_DIR = Path(sys.executable).parent
    # Ajustar sys.path para que encuentre los módulos internos
    sys.path.append(os.path.join(sys._MEIPASS))
else:
    # Si es script, el directorio base es el del script
    BASE_DIR = Path(__file__).resolve().parent

# Configurar variable de entorno para settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodega_belen.settings')

# Importar Django
import django
from django.core.management import execute_from_command_line

def open_browser():
    """Abre el navegador después de una breve espera"""
    time.sleep(3)
    print("🌐 Abriendo navegador en http://127.0.0.1:8000 ...")
    webbrowser.open('http://127.0.0.1:8000')

def main():
    print("="*60)
    print("   🏪 BODEGA DE BELÉN - SISTEMA DE GESTIÓN")
    print("="*60)
    print(f"📂 Directorio Base: {BASE_DIR}")
    
    try:
        # Inicializar Django
        print("⚙️  Cargando configuración...")
        django.setup()
        
        # --- DEBUG INIT ---
        print("🔍 Verificando integridad del sistema...")
        try:
            from django.core.wsgi import get_wsgi_application
            application = get_wsgi_application()
            print("✅ Aplicación WSGI cargada correctamente.")
        except Exception as e:
            print("\n❌ ERROR FATAL AL CARGAR LA APLICACIÓN:")
            traceback.print_exc()
            print("\n")
            input("Presiona ENTER para salir...")
            sys.exit(1)
        # ------------------

        # Ejecutar migraciones automáticamente
        print("🗄️  Verificando base de datos...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Preparar hilo para abrir navegador
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Iniciar servidor
        print("\n🚀 Servidor iniciado. Presiona Ctrl+C para detener.")
        print("   Accede manualmente en: http://127.0.0.1:8000\n")
        
        # Usar --noreload es CRÍTICO para PyInstaller
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000', '--noreload', '--insecure'])
        
    except KeyboardInterrupt:
        print("\n👋 Deteniendo servidor...")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        traceback.print_exc()
        input("Presiona ENTER para salir...")

if __name__ == '__main__':
    main()
