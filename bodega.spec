# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Dependencias ocultas de Django y librerías usadas
hidden_imports = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.middleware.security',
    'whitenoise.middleware',
    'django.contrib.sessions.middleware',
    'django.middleware.common',
    'django.middleware.csrf',
    'django.contrib.auth.middleware',
    'django.contrib.messages.middleware',
    'django.middleware.clickjacking',
    'sqlparse',  # Required for migrations
    'decimal',
    'requests',
    'pkg_resources.py2_warn',
    'import_export',
    'openpyxl',
    'tablib',
]

# Recolectar submodulos de tablib para incluir formatos (xlsx, csv, etc.)
hidden_imports += collect_submodules('tablib')
hidden_imports += collect_submodules('openpyxl')

# Agregar submodulos de mis apps
hidden_imports += collect_submodules('bodega_belen')
hidden_imports += collect_submodules('inventario')
hidden_imports += collect_submodules('ventas')
hidden_imports += collect_submodules('clientes')

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('bodega_belen', 'bodega_belen'),
        ('inventario', 'inventario'),
        ('ventas', 'ventas'),
        ('clientes', 'clientes'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BodegaBelen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
