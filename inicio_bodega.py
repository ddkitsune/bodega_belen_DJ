"""
Script de inicio para Bodega de Belén
Inicia el servidor Django y abre el navegador automáticamente
"""
import os
import sys
import webbrowser
import time
from threading import Timer
import subprocess

def abrir_navegador():
    """Espera 3 segundos y abre el navegador en el sistema"""
    time.sleep(3)
    print("🌐 Abriendo navegador...")
    webbrowser.open('http://127.0.0.1:8000')

def main():
    """Función principal que inicia el servidor Django"""
    # Banner de bienvenida
    print("=" * 60)
    print("   🏪 BODEGA DE BELÉN - SISTEMA DE VENTAS")
    print("=" * 60)
    print()
    print("🚀 Iniciando servidor...")
    print("📍 URL: http://127.0.0.1:8000")
    print()
    print("⚠️  IMPORTANTE: NO CIERRES ESTA VENTANA")
    print("    Para detener el servidor, presiona Ctrl+C")
    print()
    print("=" * 60)
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("❌ ERROR: No se encuentra manage.py")
        print("   Asegúrate de ejecutar este script desde la carpeta del proyecto")
        input("Presiona Enter para salir...")
        sys.exit(1)
    
    # Programar la apertura del navegador
    timer = Timer(3.0, abrir_navegador)
    timer.start()
    
    try:
        # Iniciar servidor Django
        subprocess.run([
            sys.executable,
            'manage.py',
            'runserver',
            '127.0.0.1:8000',
            '--noreload'
        ])
    except KeyboardInterrupt:
        print("\n\n⏹️  Servidor detenido correctamente")
        print("👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")
        input("Presiona Enter para salir...")
        sys.exit(1)

if __name__ == '__main__':
    main()
