import os
import sys
import time
import traceback
import webbrowser
from threading import Timer

def open_browser():
    time.sleep(3)
    print("Intentando abrir el navegador...")
    webbrowser.open('http://127.0.0.1:8000/')

def main():
    print("--------------------------------------------")
    print("BODEGA DE BELEN - INICIANDO...")
    print("--------------------------------------------")
    
    try:
        # 1. Configurar Entorno
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodega_belen.settings')
        
        print("[1/3] Cargando modulos de sistema...")
        from django.core.management import execute_from_command_line
        import django
        django.setup()
        
        # 2. Base de datos
        print("[2/3] Verificando base de datos...")
        execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
        
        # 3. Lanzar Navegador
        Timer(1, open_browser).start()
        
        # 4. Servidor
        print("[3/3] Iniciando servidor en http://127.0.0.1:8000")
        print("IMPORTANTE: No cierre esta ventana mientras use el programa.")
        print("--------------------------------------------")
        
        execute_from_command_line([sys.argv[0], 'runserver', '127.0.0.1:8000', '--noreload'])

    except Exception as e:
        print("\n!!!!!!!!!!!!!!! ERROR CRITICO !!!!!!!!!!!!!!!")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("\nDetalle tecnico (Stacktrace):")
        traceback.print_exc()
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("\nPresione cualquier tecla para salir...")
        input()

if __name__ == '__main__':
    # Para que los prints se vean en la terminal de usuario sin delay
    sys.stdout.reconfigure(line_buffering=True)
    main()
