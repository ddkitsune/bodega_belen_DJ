# 🗄️ CONFIGURACIÓN DE BASE DE DATOS

## 📊 Estado Actual

### **Localmente (Tu PC):**
```
✅ SQLite
📁 Archivo: db.sqlite3
💾 Tamaño: 0.26 MB
📍 Ubicación: C:\Users\Deivy\Desktop\proyectos\Bodeja_de_Belen\db.sqlite3
```

### **En Producción (Vercel/Railway):**
```
✅ PostgreSQL
☁️ Base de datos en la nube
🔄 Se configura automáticamente
```

---

## 🔄 Cómo Funciona

### **Desarrollo Local:**
```python
# settings.py detecta que NO estás en Vercel/Railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # ← SQLite
        'NAME': 'db.sqlite3',
    }
}
```

### **Producción (Vercel/Railway):**
```python
# settings.py detecta variable RAILWAY_ENVIRONMENT o VERCEL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # ← PostgreSQL
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}
```

---

## 📋 Migración de Datos

### **¿Qué pasa con tus datos actuales?**

Tus datos están en `db.sqlite3` (local). Para pasarlos a producción:

#### **Opción 1: Exportar/Importar (Recomendado)**
```bash
# 1. Exportar desde SQLite
python manage.py dumpdata > datos.json

# 2. Desplegar en Railway/Vercel (con PostgreSQL)

# 3. Importar a PostgreSQL
python manage.py loaddata datos.json
```

#### **Opción 2: Empezar de cero**
- Desplegar sin datos
- Crear productos/clientes desde cero en producción

---

## ✅ Ventajas de Esta Configuración

### **Local (SQLite):**
- ✅ No requiere instalación
- ✅ Un solo archivo
- ✅ Fácil de respaldar
- ✅ Perfecto para desarrollo

### **Producción (PostgreSQL):**
- ✅ Soporta múltiples usuarios
- ✅ Más rápido
- ✅ Más confiable
- ✅ Backups automáticos

---

## 🎯 Resumen

| Aspecto | Local | Producción |
|---------|-------|------------|
| **Base de Datos** | SQLite | PostgreSQL |
| **Archivo** | db.sqlite3 | En la nube |
| **Configuración** | Automática | Variables de entorno |
| **Datos** | Tus datos actuales | Se migran con dumpdata |

---

## 🚀 Próximos Pasos

1. **Ahora**: Sigue usando SQLite localmente (como siempre)
2. **Al desplegar**: Railway/Vercel configurarán PostgreSQL automáticamente
3. **Migrar datos**: Usa `dumpdata` y `loaddata`

---

**¿Todo claro?** 

Tu sistema seguirá funcionando exactamente igual en local. 
Solo cuando despliegues a Railway/Vercel usará PostgreSQL automáticamente.
