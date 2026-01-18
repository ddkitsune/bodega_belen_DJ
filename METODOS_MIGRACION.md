# 🔄 MÉTODOS DE MIGRACIÓN DE DATOS

## 📋 Opciones Disponibles

Existen **3 métodos** para migrar tus datos a una nueva versión:

---

## ✅ MÉTODO 1: Copiar Base de Datos (Recomendado)

### ¿Cuándo usar?
- Actualización normal del sistema
- Quieres mantener TODO el historial
- La base de datos funciona correctamente

### ¿Qué se mantiene?
- ✅ Todos los productos
- ✅ Todas las categorías
- ✅ Todos los clientes
- ✅ Todo el historial de ventas
- ✅ Todas las tasas de cambio
- ✅ Toda la configuración

### Pasos:
1. Cierra el programa
2. Ejecuta `BACKUP_AUTOMATICO.bat`
3. Copia `db.sqlite3` a la nueva carpeta
4. Ejecuta el nuevo `BodegaBelen.exe`
5. ¡Listo! Todo migrado automáticamente

**Tiempo:** ~1 minuto  
**Dificultad:** ⭐ Muy fácil

---

## 📊 MÉTODO 2: Exportar/Importar Excel

### ¿Cuándo usar?
- Quieres empezar con una instalación limpia
- Solo necesitas migrar productos
- La base de datos antigua tiene problemas
- Quieres limpiar/revisar datos antes de migrar

### ¿Qué se mantiene?
- ✅ Productos (código, nombre, precio, stock, etc.)
- ✅ Categorías (si están en el Excel)
- ❌ Clientes (se pierden)
- ❌ Historial de ventas (se pierde)
- ❌ Tasas de cambio (se pierden)

### Pasos:

#### En el Sistema Antiguo:
1. Abre el programa antiguo
2. Ve a **Inventario → Productos**
3. Click en **"Exportar"**
4. Guarda el archivo Excel (ejemplo: `productos_backup.xlsx`)
5. Cierra el programa

#### En el Sistema Nuevo:
1. Instala la nueva versión en una carpeta nueva
2. Ejecuta `BodegaBelen.exe`
3. Ve a **Inventario → Productos**
4. Click en **"Importar"**
5. Selecciona el archivo Excel que exportaste
6. Verifica que los productos se importaron correctamente

**Tiempo:** ~5 minutos  
**Dificultad:** ⭐⭐ Fácil

### ⚠️ Limitaciones:
- Solo migra productos, NO clientes ni ventas
- Debes recrear manualmente:
  - Clientes
  - Configuración de créditos
  - No tendrás historial de ventas antiguas

---

## 🔧 MÉTODO 3: Migración Selectiva (Avanzado)

### ¿Cuándo usar?
- Quieres migrar solo algunos datos específicos
- Necesitas combinar datos de múltiples fuentes
- Tienes conocimientos técnicos

### Pasos:

1. **Exporta desde el sistema antiguo:**
   - Productos → Exportar Excel
   - (Opcional) Anota manualmente clientes importantes

2. **Instala sistema nuevo**

3. **Importa selectivamente:**
   - Importa productos desde Excel
   - Recrea clientes manualmente (si son pocos)
   - Configura límites de crédito

**Tiempo:** ~15-30 minutos  
**Dificultad:** ⭐⭐⭐ Moderado

---

## 🎯 ¿Cuál Método Elegir?

### Usa MÉTODO 1 si:
- ✅ Tienes historial de ventas que quieres conservar
- ✅ Tienes clientes con crédito configurado
- ✅ Quieres la migración más rápida y completa
- ✅ Tu base de datos funciona bien

### Usa MÉTODO 2 si:
- ✅ Solo te importan los productos
- ✅ Quieres empezar "limpio"
- ✅ No tienes muchos clientes o ventas
- ✅ La base de datos antigua tiene problemas

### Usa MÉTODO 3 si:
- ✅ Necesitas control total del proceso
- ✅ Quieres migrar solo datos específicos
- ✅ Tienes tiempo para hacerlo manualmente

---

## 📝 Comparación Rápida

| Aspecto | Método 1 (DB) | Método 2 (Excel) | Método 3 (Manual) |
|---------|---------------|------------------|-------------------|
| **Productos** | ✅ Todos | ✅ Todos | ⚠️ Selectivo |
| **Categorías** | ✅ Todas | ✅ Todas | ⚠️ Selectivo |
| **Clientes** | ✅ Todos | ❌ Ninguno | ⚠️ Manual |
| **Ventas** | ✅ Todas | ❌ Ninguna | ❌ Ninguna |
| **Tasas BCV** | ✅ Todas | ❌ Ninguna | ❌ Ninguna |
| **Tiempo** | 1 min | 5 min | 15-30 min |
| **Dificultad** | Muy fácil | Fácil | Moderado |
| **Reversible** | ✅ Sí | ❌ No | ❌ No |

---

## 🛡️ Recomendación de Seguridad

**SIEMPRE haz backup antes de cualquier método:**

```bash
# Ejecuta esto ANTES de migrar
BACKUP_AUTOMATICO.bat
```

Esto te permite volver atrás si algo sale mal.

---

## 📖 Guías Detalladas

### Para MÉTODO 1:
Ver: `GUIA_ACTUALIZACION.md`

### Para MÉTODO 2:
Ver: Sección siguiente

### Para MÉTODO 3:
Contacta soporte para asistencia personalizada

---

## 📊 GUÍA DETALLADA: Exportar/Importar Excel

### Formato del Excel

El archivo Excel debe tener estas columnas:

| Columna | Requerido | Ejemplo |
|---------|-----------|---------|
| codigo | ✅ Sí | PROD001 |
| nombre | ✅ Sí | Arroz Diana 1Kg |
| descripcion | ❌ No | Arroz blanco premium |
| categoria | ❌ No | Granos |
| precio_usd | ✅ Sí | 2.50 |
| cantidad | ✅ Sí | 100 |
| stock_minimo | ❌ No | 10 |
| es_por_peso | ❌ No | FALSE |
| activo | ❌ No | TRUE |

### Ejemplo de Excel:

```
codigo    | nombre           | categoria | precio_usd | cantidad | es_por_peso
----------|------------------|-----------|------------|----------|------------
PROD001   | Arroz Diana 1Kg  | Granos    | 2.50       | 100      | FALSE
PROD002   | Carne Molida     | Carnes    | 4.00       | 50       | TRUE
PROD003   | Leche Completa   | Lácteos   | 1.80       | 75       | FALSE
```

### Consejos:
- ✅ Usa códigos únicos para cada producto
- ✅ Revisa que los precios sean correctos
- ✅ Verifica las cantidades antes de importar
- ✅ Para productos por peso, marca `es_por_peso = TRUE`

---

## 🆘 Solución de Problemas

### "Error al importar Excel"
**Causa:** Formato incorrecto del archivo

**Solución:**
1. Verifica que las columnas requeridas existan
2. Asegúrate que no haya filas vacías
3. Revisa que los números usen punto (.) no coma (,)

### "Productos duplicados"
**Causa:** Códigos repetidos en el Excel

**Solución:**
1. Abre el Excel
2. Busca códigos duplicados
3. Asigna códigos únicos
4. Importa nuevamente

### "Faltan categorías"
**Causa:** Las categorías no se importaron

**Solución:**
1. Crea las categorías manualmente primero
2. Luego importa los productos

---

## 💡 Mejor Práctica

**Recomendación para usuarios nuevos:**

1. **Primera vez:** Usa MÉTODO 2 (Excel)
   - Permite revisar y limpiar datos
   - Instalación limpia

2. **Actualizaciones futuras:** Usa MÉTODO 1 (DB)
   - Más rápido
   - Mantiene todo el historial

---

**Última actualización:** 18 de Enero, 2026  
**Versión:** 1.0
