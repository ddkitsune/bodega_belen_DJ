# 🚀 GUÍA DE DESPLIEGUE EN VERCEL

## ✅ Archivos Preparados

El proyecto ya está configurado para Vercel con:
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `build_files.sh` - Script de build
- ✅ `requirements.txt` - Dependencias
- ✅ `wsgi.py` - Configurado para Vercel
- ✅ `settings.py` - ALLOWED_HOSTS configurado

---

## 📋 PASO A PASO

### **1. Crear cuenta en Vercel**
1. Ve a: https://vercel.com
2. Click en "Sign Up"
3. Usa tu cuenta de GitHub (recomendado)

### **2. Subir proyecto a GitHub**

#### Opción A: Desde GitHub Desktop
1. Descarga GitHub Desktop: https://desktop.github.com
2. Abre GitHub Desktop
3. File → Add Local Repository
4. Selecciona la carpeta del proyecto
5. Publish repository

#### Opción B: Desde Git Bash
```bash
# Inicializar repositorio
git init

# Agregar archivos
git add .

# Commit
git commit -m "Initial commit - Bodega de Belén"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/bodega-belen.git
git push -u origin main
```

### **3. Desplegar en Vercel**
1. Ve a https://vercel.com/dashboard
2. Click en "Add New" → "Project"
3. Import Git Repository
4. Selecciona tu repositorio "bodega-belen"
5. Click en "Deploy"
6. ¡Espera 2-3 minutos!

### **4. Configurar Variables de Entorno**
1. En Vercel, ve a tu proyecto
2. Settings → Environment Variables
3. Agrega estas variables:

```
SECRET_KEY = tu-clave-secreta-aqui
DEBUG = False
ALLOWED_HOSTS = .vercel.app
```

### **5. Ejecutar Migraciones**
Después del primer despliegue:
1. Ve a Vercel Dashboard
2. Tu proyecto → Settings → Functions
3. O usa Vercel CLI:
```bash
vercel env pull
python manage.py migrate
```

---

## ⚠️ IMPORTANTE: Base de Datos

### **Problema:**
SQLite NO funciona en Vercel (serverless)

### **Soluciones:**

#### **Opción 1: PostgreSQL en Vercel (Recomendado)**
1. Vercel → Storage → Create Database
2. Selecciona "Postgres"
3. Copia las credenciales
4. Actualiza `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=verceldb
DB_USER=default
DB_PASSWORD=...
DB_HOST=...
DB_PORT=5432
```

#### **Opción 2: Supabase (Gratis)**
1. Ve a https://supabase.com
2. Create New Project
3. Copia las credenciales de PostgreSQL
4. Actualiza `.env`

#### **Opción 3: Railway (Gratis)**
1. Ve a https://railway.app
2. New Project → PostgreSQL
3. Copia las credenciales
4. Actualiza `.env`

---

## 🔧 Actualizar settings.py para Producción

Agrega esto a `settings.py`:

```python
# Para Vercel con PostgreSQL
if 'VERCEL' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    # SQLite para desarrollo local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_DIR / 'db.sqlite3',
        }
    }
```

---

## 📦 Archivos Estáticos

Vercel maneja automáticamente los archivos estáticos con la configuración en `vercel.json`.

---

## ✅ Verificar Despliegue

1. Vercel te dará una URL: `https://tu-proyecto.vercel.app`
2. Abre la URL
3. Deberías ver tu sistema funcionando

---

## 🐛 Solución de Problemas

### **Error: "Application error"**
- Revisa los logs en Vercel Dashboard
- Verifica variables de entorno
- Asegúrate que `DEBUG=False`

### **Error: "Database connection failed"**
- Verifica credenciales de PostgreSQL
- Asegúrate que las variables de entorno estén configuradas

### **Archivos estáticos no cargan**
- Ejecuta `python manage.py collectstatic`
- Verifica `STATIC_ROOT` en settings.py

---

## 🎯 ALTERNATIVA MÁS SIMPLE: Railway

Si Vercel es complicado, Railway es más fácil:

1. Ve a https://railway.app
2. "Start a New Project"
3. "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detecta Django automáticamente
6. ¡Listo!

Railway incluye:
- ✅ PostgreSQL gratis
- ✅ Configuración automática
- ✅ Variables de entorno fáciles
- ✅ $5 gratis al mes

---

## 📝 Resumen

**Para Vercel:**
1. Subir a GitHub
2. Conectar con Vercel
3. Configurar PostgreSQL
4. Desplegar

**Para Railway (más fácil):**
1. Subir a GitHub
2. Conectar con Railway
3. ¡Listo! (PostgreSQL incluido)

---

**¿Prefieres Vercel o Railway?**
