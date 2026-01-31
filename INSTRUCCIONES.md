# 🚀 INSTRUCCIONES PARA INICIAR EL SISTEMA

## ✅ Estado Actual

- ✅ Base de datos creada (migrations aplicadas)
- ✅ Superusuario creado: **admin**
- ❌ Contraseña del admin pendiente
- ❌ Tasa de cambio inicial pendiente

---

## 📝 PASOS PARA COMPLETAR LA CONFIGURACIÓN

### 1. Establecer contraseña del administrador

Ejecuta en la terminal (dentro del entorno virtual):

```bash
python manage.py changepassword admin
```

Cuando te pida la nueva contraseña, ingresa: **admin123** (o la que prefieras)

### 2. Crear tasa de cambio inicial

**Opción A - Desde el navegador (más fácil):**

1. Accede a http://localhost:8000/admin
2. Login: `admin` / `admin123`
3. Ve a "Tasas de Cambio" → "Agregar tasa de cambio"
4. Ingresa:
   - Tasa: 40.00 (o la tasa actual)
   - Fuente: Manual
5. Guardar

**Opción B - Desde la terminal:**

```bash
python manage.py shell
```

Dentro del shell de Django:
```python
from ventas.models import TasaCambio
from decimal import Decimal
TasaCambio.objects.create(tasa=Decimal('40.00'), fuente='Manual')
exit()
```

### 3. Acceder al sistema

**URL Frontend:** http://localhost:8000
**URL Admin:** http://localhost:8000/admin

**Credenciales:**
- Usuario: `admin`
- Contraseña: `admin123` (o la que hayas establecido)

---

## 🎯 NUEVAS FUNCIONALIDADES AGREGADAS

### ✨ Eliminar Tasas de Cambio Manuales

Ahora puedes **eliminar tasas de cambio** que hayas creado manualmente si te equivocaste:

1. Ve a **Tasas de Cambio**
2. Verás un botón **🗑️** (trash) en las tasas marcadas como "Manual"
3. Click en el botón para eliminar
4. **Las tasas del BCV NO se pueden eliminar** (solo las manuales)

---

## 🔧 SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "No such table"
Ejecutar:
```bash
python manage.py migrate
```

### Error al acceder a secciones
1. Asegúrate de haber creado al menos una tasa de cambio
2. Reinicia el servidor: Ctrl+C y luego `python manage.py runserver`

### Olvidé la contraseña del admin
```bash
python manage.py changepassword admin
```

---

## 📊 PRIMEROS PASOS EN EL SISTEMA

### 1. Configurar Tasa de Cambio ✅
- Dashboard → "Actualizar" (desde BCV)
- O crear manualmente desde Admin

### 2. Crear Categorías (Opcional)
- Admin → Categorías → Agregar

### 3. Crear Productos
- Inventario → Nuevo Producto
- Ejemplo:
  - Código: PROD001
  - Nombre: Arroz 1kg
  - Precio USD: 2.50
  - Cantidad: 100

### 4. Crear Clientes
- Clientes → Nuevo Cliente
- Ejemplo:
  - V-12345678
  - Juan Pérez
  - Tiene Crédito: Sí
  - Límite: 500.00 USD

### 5. Realizar Primera Venta
- Nueva Venta
- Seleccionar cliente
- Agregar productos
- El sistema calcula USD y Bs automáticamente
- Crear factura

### 6. Registrar Pago
- Desde la factura → "Registrar Pago"
- Ingresa monto en Bs
- El sistema calcula el vuelto en USD y Bs automáticamente

---

## ✨ CARACTERÍSTICAS DEL SISTEMA

- ✅ Todos los precios se muestran en USD Y Bs
- ✅ Cálculo automático de vueltos en ambas divisas
- ✅ Control de stock automático
- ✅ Sistema de créditos con límites
- ✅ Validación de límites de crédito
- ✅ Historial completo de movimientos
- ✅ **NUEVO:** Eliminar tasas manuales incorrectas

---

## 🆘 ¿NECESITAS AYUDA?

Si algo no funciona:

1. Verifica que el servidor esté corriendo: `python manage.py runserver`
2. Verifica que tengas al menos una tasa de cambio creada
3. Revisa los mensajes de error en la terminal del servidor
4. Intenta desde el panel de Admin primero

---

¡El sistema está listo para usar! 🎉
