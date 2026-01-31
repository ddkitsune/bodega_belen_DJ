import os
import subprocess
import sys

def run():
    print("--- INICIANDO LIMPIEZA PROFUNDA ---")
    cwd = os.getcwd()
    
    # 1. Matar procesos colgados
    print("Cerrando procesos de Python/BodegaBelen...")
    if sys.platform == 'win32':
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe', '/T'], capture_output=True)
        subprocess.run(['taskkill', '/F', '/IM', 'BodegaBelen.exe', '/T'], capture_output=True)

    # 2. Eliminar DB y migraciones viejas
    print("Limpiando base de datos y migraciones...")
    files_to_del = ['db.sqlite3']
    dirs_to_clean = ['inventario/migrations', 'ventas/migrations', 'clientes/migrations']
    
    for f in files_to_del:
        if os.path.exists(f): os.remove(f)
        
    for d in dirs_to_clean:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f != '__init__.py' and f != '__pycache__':
                    try: os.remove(os.path.join(d, f))
                    except: pass

    # 3. Re-crear migraciones
    print("Creando nuevas migraciones...")
    subprocess.run([sys.executable, 'manage.py', 'makemigrations'])
    subprocess.run([sys.executable, 'manage.py', 'migrate'])

    print("\n--- TODO LISTO ---")
    print("Iniciando servidor en modo DEBUG (Presiona Ctrl+C para detener)")
    subprocess.run([sys.executable, 'manage.py', 'runserver'])

if __name__ == '__main__':
    run()
