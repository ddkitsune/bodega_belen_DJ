# 🔄 GUÍA DE ACTUALIZACIÓN - Bodega de Belén

## 📋 Proceso de Actualización Seguro

Esta guía te ayudará a actualizar el sistema sin perder ningún dato de tus clientes, productos, categorías o ventas.

---

## ⚠️ IMPORTANTE: Antes de Actualizar

### 1. **Hacer Backup de la Base de Datos**

La base de datos (`db.sqlite3`) contiene TODA tu información. **SIEMPRE haz una copia de seguridad antes de actualizar.**

**Ubicación del archivo:**
```
📁 Carpeta donde está BodegaBelen.exe/
└── 📄 db.sqlite3  ← Este archivo contiene todos tus datos
```

**Cómo hacer el backup:**
1. Cierra completamente el programa (si está abierto)
2. Copia el archivo `db.sqlite3`
3. Pégalo en una carpeta segura (ejemplo: `Backup_2026-01-18`)
4. Opcional: Comprime el archivo en un ZIP

---

## 🚀 Métodos de Actualización

### **MÉTODO 1: Actualización Simple (Recomendado)**

Este método es el más seguro y fácil.

#### Pasos:

1. **Cierra el programa actual** completamente

2. **Haz backup de tu base de datos** (ver arriba)

3. **Descarga la nueva versión** del ejecutable

4. **Reemplaza SOLO el archivo .exe:**
   ```
   📁 Tu carpeta actual/
   ├── 📄 BodegaBelen.exe  ← Reemplaza este archivo
   └── 📄 db.sqlite3       ← NO TOQUES este archivo
   ```

5. **Ejecuta el nuevo BodegaBelen.exe**

6. El sistema detectará automáticamente si necesita actualizar la base de datos

7. ¡Listo! Tus datos se mantienen intactos

---

### **MÉTODO 2: Instalación Limpia con Migración de Datos**

Si quieres empezar con una carpeta nueva pero mantener tus datos:

#### Pasos:

1. **Haz backup** de tu `db.sqlite3` actual

2. **Crea una nueva carpeta** para la versión actualizada:
   ```
   📁 BodegaBelen_v2/
   └── 📄 BodegaBelen.exe  ← Nueva versión
   ```

3. **Copia tu base de datos antigua** a la nueva carpeta:
   ```
   📁 BodegaBelen_v2/
   ├── 📄 BodegaBelen.exe
   └── 📄 db.sqlite3  ← Copiado de la versión anterior
   ```

4. **Ejecuta el nuevo programa**

5. El sistema aplicará automáticamente las migraciones necesarias

---

## 🔧 Migraciones Automáticas

El sistema está configurado para aplicar migraciones automáticamente al iniciar. Esto significa que:

✅ **Se agregan nuevas columnas** a las tablas existentes
✅ **Se crean nuevas tablas** si son necesarias
✅ **Tus datos existentes se mantienen** sin cambios
✅ **No se elimina información** antigua

### ¿Qué son las migraciones?

Las migraciones son cambios en la estructura de la base de datos (nuevos campos, tablas, etc.) pero **NO afectan los datos existentes**.

Ejemplo:
- Si agregamos un campo `es_por_peso` a los productos
- Los productos existentes seguirán ahí
- El nuevo campo tendrá un valor por defecto
- Puedes editarlos después para actualizar esa información

---

## 📊 Verificar que Todo Funciona

Después de actualizar, verifica:

1. ✅ **Productos**: Ve a Inventario y confirma que todos tus productos están
2. ✅ **Categorías**: Verifica que las categorías existen
3. ✅ **Clientes**: Revisa la lista de clientes
4. ✅ **Ventas**: Confirma que el historial de ventas está completo
5. ✅ **Tasa de cambio**: Verifica que la tasa BCV se actualiza

---

## 🆘 Solución de Problemas

### Problema: "Error al abrir la base de datos"

**Solución:**
1. Cierra el programa
2. Verifica que el archivo `db.sqlite3` no esté corrupto
3. Restaura el backup si es necesario
4. Ejecuta el script de reparación (ver abajo)

### Problema: "Faltan datos después de actualizar"

**Solución:**
1. Cierra el programa inmediatamente
2. Restaura el backup de `db.sqlite3`
3. Contacta soporte antes de intentar nuevamente

### Problema: "El programa no inicia"

**Solución:**
1. Verifica que tienes permisos de administrador
2. Desactiva temporalmente el antivirus
3. Ejecuta como administrador (click derecho → Ejecutar como administrador)

---

## 🔐 Mejores Prácticas

### Backups Regulares

Recomendamos hacer backup de `db.sqlite3`:
- **Diariamente**: Si haces muchas ventas
- **Semanalmente**: Si el uso es moderado
- **Antes de cada actualización**: SIEMPRE

### Dónde Guardar los Backups

```
📁 Mis Documentos/
└── 📁 Backups_BodegaBelen/
    ├── 📁 2026-01-18/
    │   └── 📄 db.sqlite3
    ├── 📁 2026-01-17/
    │   └── 📄 db.sqlite3
    └── 📁 2026-01-16/
        └── 📄 db.sqlite3
```

### Automatizar Backups

Puedes usar el script `backup_automatico.bat` incluido para hacer backups automáticos.

---

## 📝 Registro de Cambios por Versión

### Versión 2.0 (Actual)
- ✅ Corrección de errores en templates
- ✅ Mejoras en la interfaz de ventas
- ✅ Optimización del manejo de productos por peso vs unidad
- ⚠️ **Migración requerida**: Se agrega campo `es_por_peso` a productos

### Versión 1.0 (Anterior)
- Sistema base con inventario, ventas y clientes

---

## 🎯 Resumen Rápido

**Para actualizar sin perder datos:**

1. ✅ Cierra el programa
2. ✅ Copia `db.sqlite3` a un lugar seguro
3. ✅ Reemplaza `BodegaBelen.exe` con la nueva versión
4. ✅ Ejecuta el programa
5. ✅ Verifica que todo funciona

**¡Eso es todo!** 🎉

---

## 📞 Soporte

Si tienes problemas durante la actualización:
- Restaura el backup de `db.sqlite3`
- Ejecuta el script de diagnóstico (ver carpeta `scripts/`)
- Contacta al desarrollador con el reporte de errores

---

**Última actualización:** 18 de Enero, 2026
**Versión del documento:** 1.0
