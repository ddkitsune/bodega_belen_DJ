# 📦 Paquete de Distribución - Bodega de Belén

## 📋 Contenido del Paquete

Este paquete incluye todo lo necesario para instalar o actualizar el sistema:

```
📁 BodegaBelen_v2.0/
├── 📄 BodegaBelen.exe           ← Ejecutable principal
├── 📄 LEEME.txt                 ← Instrucciones rápidas
├── 📄 GUIA_ACTUALIZACION.md     ← Guía completa de actualización
├── 📄 BACKUP_AUTOMATICO.bat     ← Script para hacer backups
├── 📄 ACTUALIZAR.bat            ← Script de actualización automática
├── 📄 RESTAURAR_BACKUP.bat      ← Script para restaurar backups
├── 📄 verificar_datos.py        ← Verificar integridad de datos
└── 📄 db.sqlite3                ← Base de datos (solo en instalación nueva)
```

---

## 🚀 Instalación Nueva

Si es tu primera vez usando el sistema:

1. **Descomprime** todos los archivos en una carpeta
2. **Ejecuta** `BodegaBelen.exe`
3. El sistema creará automáticamente la base de datos
4. ¡Listo para usar!

---

## 🔄 Actualización desde Versión Anterior

Si ya tienes una versión anterior instalada:

### Opción 1: Actualización Manual (Rápida)

1. **Cierra** el programa si está abierto
2. **Ejecuta** `BACKUP_AUTOMATICO.bat` para respaldar tus datos
3. **Reemplaza** solo el archivo `BodegaBelen.exe` con el nuevo
4. **Ejecuta** el programa
5. ✅ ¡Actualización completa!

### Opción 2: Actualización Automática (Recomendada)

1. **Copia** el nuevo `BodegaBelen.exe` a tu carpeta actual
2. **Renómbralo** a `BodegaBelen_NUEVO.exe`
3. **Ejecuta** `ACTUALIZAR.bat`
4. El script hará todo automáticamente
5. ✅ ¡Actualización completa!

---

## 💾 Backups

### Crear Backup Manual

Simplemente ejecuta: `BACKUP_AUTOMATICO.bat`

Los backups se guardan en: `Backups/FECHA/`

### Restaurar Backup

Si algo sale mal:

1. Ejecuta `RESTAURAR_BACKUP.bat`
2. Selecciona el backup que deseas restaurar
3. Confirma la restauración
4. ✅ Datos restaurados

---

## 🔍 Verificar Datos

Después de actualizar, puedes verificar que todo esté bien:

```bash
python verificar_datos.py
```

Este script te mostrará:
- ✅ Número de productos, clientes, ventas, etc.
- ✅ Estado de la base de datos
- ✅ Campos y tablas existentes

---

## ⚠️ IMPORTANTE

### Antes de Actualizar

1. ✅ **SIEMPRE** haz un backup de `db.sqlite3`
2. ✅ Cierra completamente el programa
3. ✅ Lee la guía de actualización

### Durante la Actualización

- ❌ NO elimines `db.sqlite3`
- ❌ NO interrumpas el proceso
- ❌ NO ejecutes múltiples instancias

### Después de Actualizar

- ✅ Verifica que tus datos estén presentes
- ✅ Prueba crear una venta de prueba
- ✅ Guarda el backup por al menos 7 días

---

## 📊 Compatibilidad

### Versiones Compatibles

Esta versión puede actualizar desde:
- ✅ Versión 1.0
- ✅ Versión 1.5
- ✅ Cualquier versión que use SQLite

### Migraciones Automáticas

El sistema aplicará automáticamente:
- ✅ Nuevas tablas
- ✅ Nuevos campos
- ✅ Índices mejorados
- ✅ Valores por defecto

**Tus datos NO se perderán** durante las migraciones.

---

## 🆘 Solución de Problemas

### "No se puede abrir db.sqlite3"

**Causa:** El archivo está en uso o corrupto

**Solución:**
1. Cierra todas las instancias del programa
2. Reinicia tu computadora
3. Intenta nuevamente

### "Error de migración"

**Causa:** Problema durante la actualización de la base de datos

**Solución:**
1. Ejecuta `RESTAURAR_BACKUP.bat`
2. Restaura el último backup
3. Contacta soporte

### "Faltan datos después de actualizar"

**Causa:** Posible corrupción durante la actualización

**Solución:**
1. **NO CIERRES** el programa
2. Ejecuta `RESTAURAR_BACKUP.bat` inmediatamente
3. Restaura el backup más reciente
4. Contacta soporte antes de intentar nuevamente

---

## 📞 Soporte

Si tienes problemas:

1. **Ejecuta** `verificar_datos.py` y guarda el resultado
2. **Copia** el mensaje de error completo
3. **Contacta** al desarrollador con:
   - Versión anterior que tenías
   - Versión nueva que instalaste
   - Resultado de `verificar_datos.py`
   - Mensaje de error (si hay)

---

## 📝 Notas de la Versión

### Versión 2.0 - Enero 2026

**Nuevas Características:**
- ✨ Soporte para productos por peso y por unidad
- ✨ Mejoras en la interfaz de ventas
- ✨ Corrección de errores en templates

**Cambios en la Base de Datos:**
- ➕ Campo `es_por_peso` en tabla `inventario_producto`
- 🔧 Optimización de índices

**Mejoras:**
- ⚡ Rendimiento mejorado en listados
- 🎨 Interfaz más intuitiva
- 🐛 Corrección de bugs menores

---

## 📄 Licencia y Uso

Este software es para uso exclusivo de **Bodega de Belén**.

- ✅ Puedes hacer backups
- ✅ Puedes actualizar
- ✅ Puedes instalar en múltiples computadoras de tu negocio
- ❌ NO redistribuir sin autorización

---

## ✅ Lista de Verificación Post-Instalación

Después de instalar o actualizar, verifica:

- [ ] El programa inicia correctamente
- [ ] Puedes ver tus productos
- [ ] Puedes ver tus clientes
- [ ] Puedes ver el historial de ventas
- [ ] La tasa BCV se actualiza
- [ ] Puedes crear una venta de prueba
- [ ] Los reportes funcionan

Si todos los puntos están ✅, ¡estás listo para usar el sistema!

---

**Última actualización:** 18 de Enero, 2026  
**Versión:** 2.0  
**Desarrollado para:** Bodega de Belén
