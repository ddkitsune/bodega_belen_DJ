# 🚂 Guía de Despliegue en Railway

Esta guía te ayudará a desplegar tu aplicación **Bodega de Belén** en Railway.

## 📋 Pre-requisitos

- ✅ Cuenta en [Railway.app](https://railway.app) (puedes registrarte con GitHub)
- ✅ Proyecto subido a GitHub
- ✅ Archivos de configuración creados (Procfile, railway.json)

## 🚀 Pasos para Desplegar

### 1. Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app) e inicia sesión
2. Haz clic en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Autoriza a Railway para acceder a tus repositorios de GitHub
5. Selecciona el repositorio **`bodega_belen_DJ`**

### 2. Agregar Base de Datos PostgreSQL

1. En tu proyecto de Railway, haz clic en **"+ New"**
2. Selecciona **"Database"**
3. Elige **"Add PostgreSQL"**
4. Railway creará automáticamente una base de datos PostgreSQL

### 3. Configurar Variables de Entorno

En tu proyecto de Railway, ve a la pestaña **"Variables"** y agrega las siguientes:

```env
# Django Configuration
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=.railway.app

# Database (Railway las configura automáticamente, pero puedes verificar)
DATABASE_URL=postgresql://...  # Railway lo configura automáticamente
RAILWAY_ENVIRONMENT=production

# Opcional: Si usas la API de BCV
BCV_API_URL=https://pydolarve.org/api/v1/dollar/page
```

**Importante:** Railway automáticamente configura `DATABASE_URL` cuando agregas PostgreSQL. No necesitas configurar manualmente DB_NAME, DB_USER, DB_PASSWORD, etc.

### 4. Actualizar settings.py para usar DATABASE_URL

Railway proporciona la URL de la base de datos en la variable `DATABASE_URL`. Necesitamos actualizar `settings.py` para usarla.

### 5. Desplegar

1. Railway detectará automáticamente tu `Procfile` y `railway.json`
2. Comenzará el proceso de build automáticamente
3. Ejecutará las migraciones
4. Recolectará archivos estáticos
5. Iniciará el servidor con Gunicorn

### 6. Crear Superusuario

Una vez desplegado, necesitas crear un superusuario:

1. En Railway, ve a tu servicio
2. Haz clic en la pestaña **"Settings"**
3. Busca la sección **"Service"** y haz clic en **"Open Shell"**
4. Ejecuta:
```bash
python manage.py createsuperuser
```
5. Sigue las instrucciones para crear tu usuario administrador

### 7. Acceder a tu Aplicación

1. En Railway, ve a la pestaña **"Settings"**
2. En la sección **"Domains"**, haz clic en **"Generate Domain"**
3. Railway te dará una URL como: `https://tu-proyecto.railway.app`
4. ¡Accede a tu aplicación!

## 🔧 Comandos Útiles en Railway Shell

```bash
# Ver migraciones
python manage.py showmigrations

# Ejecutar migraciones manualmente
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Ver logs
# (Los logs se ven automáticamente en la pestaña "Deployments")
```

## 📊 Monitoreo

- **Logs**: Ve a la pestaña "Deployments" para ver los logs en tiempo real
- **Métricas**: Railway muestra uso de CPU, memoria y red
- **Reiniciar**: Puedes reiniciar el servicio desde la pestaña "Settings"

## 🔄 Actualizar la Aplicación

Cada vez que hagas `git push` a tu repositorio de GitHub, Railway automáticamente:
1. Detectará los cambios
2. Construirá una nueva versión
3. Ejecutará las migraciones
4. Desplegará la nueva versión

## ⚠️ Solución de Problemas

### Error: "Application failed to respond"
- Verifica que `Procfile` esté correctamente configurado
- Revisa los logs en Railway
- Asegúrate de que `ALLOWED_HOSTS` incluya `.railway.app`

### Error de Base de Datos
- Verifica que PostgreSQL esté agregado al proyecto
- Confirma que `DATABASE_URL` esté configurada
- Ejecuta migraciones manualmente desde el shell

### Archivos Estáticos no se Cargan
- Verifica que WhiteNoise esté instalado
- Ejecuta `python manage.py collectstatic --noinput`
- Revisa la configuración de `STATIC_ROOT` y `STATIC_URL`

## 💰 Costos

Railway ofrece:
- **Plan Gratuito**: $5 USD de crédito mensual (suficiente para proyectos pequeños)
- **Plan Developer**: $5 USD/mes + uso
- **Plan Pro**: $20 USD/mes + uso

Para este proyecto, el plan gratuito debería ser suficiente para empezar.

## 📚 Recursos Adicionales

- [Documentación de Railway](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Guía de Django en Railway](https://docs.railway.app/guides/django)

## ✅ Checklist de Despliegue

- [ ] Cuenta de Railway creada
- [ ] Repositorio conectado
- [ ] PostgreSQL agregado
- [ ] Variables de entorno configuradas
- [ ] Build exitoso
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Dominio generado
- [ ] Aplicación accesible
- [ ] Login funcionando
- [ ] Datos de prueba cargados

---

**¡Listo!** Tu aplicación Bodega de Belén ahora está en producción en Railway 🎉
