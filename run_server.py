"""
Script launcher para ejecutar el servidor Django como .exe
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar el path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodega_belen.settings')
django.setup()

def main():
    """Ejecutar el servidor Django"""
    print("=" * 60)
    print("🏪 BODEGA DE BELÉN - Sistema de Ventas")
    print("=" * 60)
    print("\n📡 Iniciando servidor...")
    print("🌐 Accede a: http://127.0.0.1:8000")
    print("\n⚠️  Para detener el servidor presiona Ctrl+C\n")
    print("=" * 60)
    
    # Ejecutar migraciones si es necesario
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    except:
        pass
    
    # Iniciar servidor
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000', '--noreload'])

if __name__ == '__main__':
    main()
