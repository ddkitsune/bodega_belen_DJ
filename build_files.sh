#!/bin/bash

echo "🚀 Iniciando Build..."
python3 --version

# Asegurar pip disponible usando solo python3 (el entorno ya debería tener la versión correcta)
echo "🔧 Configurando pip..."
python3 -m ensurepip --default-pip 2>/dev/null || true
python3 -m pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando requerimientos..."
python3 -m pip install -r requirements.txt

# Crear directorio de estáticos si no existe
echo "📁 Creando directorio staticfiles_build..."
mkdir -p staticfiles_build

# Colectar estáticos
echo "🎨 Colectando archivos estáticos..."
python3 manage.py collectstatic --noinput --clear

echo "✅ Build completado!"
