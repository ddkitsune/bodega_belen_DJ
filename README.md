# 🏪 Bodega de Belén - Sistema de Gestión

Sistema completo de gestión para bodegas y pequeños negocios desarrollado en Django. Incluye gestión de inventario, ventas, clientes, y reportes con integración de tasa de cambio BCV.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2.9-green)
![License](https://img.shields.io/badge/License-Private-red)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## 📋 Características

### 📦 Gestión de Inventario
- ✅ Productos con código, nombre, descripción y categorías
- ✅ Control de stock con alertas de stock bajo
- ✅ Soporte para productos por peso (Kg) y por unidad
- ✅ Precios en USD con conversión automática a Bs
- ✅ Importación/Exportación de inventario en Excel

### 💰 Sistema de Ventas
- ✅ Creación de facturas con múltiples productos
- ✅ Ventas al contado y a crédito
- ✅ Múltiples métodos de pago (Efectivo, Transferencia, Pago Móvil, etc.)
- ✅ Cálculo automático de vueltos en USD y Bs
- ✅ Historial completo de ventas
- ✅ Anulación de facturas

### 👥 Gestión de Clientes
- ✅ Registro de clientes con datos completos
- ✅ Sistema de crédito con límites configurables
- ✅ Control de deuda por cliente
- ✅ Historial de compras por cliente

### 📊 Reportes y Dashboard
- ✅ Dashboard con métricas en tiempo real
- ✅ Reportes de ventas por período
- ✅ Análisis de productos más vendidos
- ✅ Gráficos interactivos

### 💱 Integración BCV
- ✅ Actualización automática de tasa de cambio
- ✅ Historial de tasas
- ✅ Conversión automática USD ↔ Bs

---

## 🚀 Instalación

### Opción 1: Ejecutable para Windows (Recomendado para usuarios finales)

1. Descarga el paquete de distribución `BodegaBelen_vX.X.zip`
2. Descomprime en una carpeta
3. Ejecuta `BodegaBelen.exe`
4. ¡Listo para usar!

📖 **Documentación completa:** Ver `LEEME.txt` en el paquete

### Opción 2: Instalación para Desarrollo

#### Requisitos
- Python 3.11+
- pip
- virtualenv (recomendado)

#### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/bodega_belen_DJ.git
cd bodega_belen_DJ
```

2. **Crear entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

8. **Acceder a la aplicación**
```
http://127.0.0.1:8000
```

---

## 🔧 Compilar Ejecutable

Para crear el ejecutable de Windows:

1. **Instalar PyInstaller**
```bash
pip install pyinstaller
```

2. **Compilar**
```bash
pyinstaller --clean bodega.spec
```

3. **El ejecutable estará en:**
```
dist/BodegaBelen.exe
```

📖 **Guía completa:** Ver `COMO_CREAR_EJECUTABLE.md`

---

## 📦 Estructura del Proyecto

```
bodega_belen/
├── 📁 bodega_belen/        # Configuración principal del proyecto
├── 📁 inventario/          # App de gestión de inventario
├── 📁 ventas/              # App de gestión de ventas
├── 📁 clientes/            # App de gestión de clientes
├── 📁 templates/           # Templates HTML
├── 📁 static/              # Archivos estáticos (CSS, JS, imágenes)
├── 📁 dist/                # Ejecutable compilado (no en Git)
├── 📄 manage.py            # Comando de gestión de Django
├── 📄 bodega.spec          # Configuración de PyInstaller
├── 📄 requirements.txt     # Dependencias Python
├── 📄 .env.example         # Ejemplo de variables de entorno
└── 📄 README.md            # Este archivo
```

---

## 🔄 Sistema de Actualización

Este proyecto incluye un sistema completo de actualización segura que protege los datos del usuario:

### Para Usuarios Finales

- **BACKUP_AUTOMATICO.bat** - Crea backups automáticos
- **ACTUALIZAR.bat** - Actualización automática con respaldo
- **RESTAURAR_BACKUP.bat** - Restaura backups anteriores
- **verificar_datos.py** - Verifica integridad de datos

📖 **Guía completa:** Ver `GUIA_ACTUALIZACION.md`

### Para Desarrolladores

Al distribuir nuevas versiones:

1. Sigue el `CHECKLIST_DISTRIBUCION.md`
2. Incluye todos los scripts de actualización
3. Documenta cambios en `LEEME_DISTRIBUCION.md`
4. Prueba el proceso completo de actualización

📖 **Documentación técnica:** Ver `SISTEMA_ACTUALIZACION_RESUMEN.md`

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 5.2.9** - Framework web
- **SQLite** - Base de datos (portable)
- **Python 3.11** - Lenguaje de programación

### Frontend
- **Bootstrap 5** - Framework CSS
- **Select2** - Selectores mejorados
- **Chart.js** - Gráficos interactivos
- **jQuery** - Manipulación DOM

### Librerías Adicionales
- **django-import-export** - Importación/Exportación Excel
- **openpyxl** - Manejo de archivos Excel
- **requests** - Consultas HTTP (API BCV)
- **python-decouple** - Gestión de configuración
- **PyInstaller** - Compilación a ejecutable

---

## 📊 Base de Datos

El sistema usa **SQLite** para máxima portabilidad:

- ✅ No requiere instalación de servidor de BD
- ✅ Base de datos en un solo archivo (`db.sqlite3`)
- ✅ Fácil de respaldar (copiar archivo)
- ✅ Ideal para pequeños negocios

### Modelos Principales

- **Producto** - Inventario de productos
- **Categoria** - Categorías de productos
- **Cliente** - Información de clientes
- **Factura** - Ventas realizadas
- **DetalleVenta** - Items de cada factura
- **TasaCambio** - Historial de tasas BCV

---

## 🔐 Seguridad

- ✅ Autenticación de usuarios (opcional)
- ✅ Auto-login para uso en negocio pequeño
- ✅ Protección CSRF en formularios
- ✅ Validación de datos en backend
- ✅ Backups automáticos de datos

---

## 📝 Configuración

### Variables de Entorno (.env)

```env
# Django
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos (opcional, usa SQLite por defecto)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
```

---

## 🚀 Despliegue

### Vercel (Web)

El proyecto incluye configuración para Vercel:

```bash
vercel --prod
```

📖 **Guía completa:** Ver `DESPLIEGUE_VERCEL.md`

### Windows Ejecutable (Local)

Distribuye el paquete completo:
- `BodegaBelen.exe`
- Scripts de actualización (.bat)
- Documentación (LEEME.txt)

---

## 📖 Documentación

- **LEEME.txt** - Instrucciones rápidas para usuarios
- **GUIA_ACTUALIZACION.md** - Guía de actualización
- **COMO_CREAR_EJECUTABLE.md** - Compilar ejecutable
- **SISTEMA_ACTUALIZACION_RESUMEN.md** - Sistema de actualización (técnico)
- **CHECKLIST_DISTRIBUCION.md** - Checklist para distribuir versiones
- **DESPLIEGUE_VERCEL.md** - Despliegue en Vercel

---

## 🐛 Solución de Problemas

### El programa no inicia
- Ejecuta como administrador
- Verifica que no haya otra instancia corriendo
- Revisa el archivo de log

### Error de base de datos
- Ejecuta `verificar_datos.py`
- Restaura un backup si es necesario
- Contacta soporte

### Problemas de actualización
- Ejecuta `RESTAURAR_BACKUP.bat`
- Selecciona el backup más reciente
- Intenta la actualización nuevamente

---

## 🤝 Contribuir

Este es un proyecto privado para **Bodega de Belén**. 

Para reportar bugs o sugerir mejoras, contacta al desarrollador.

---

## 📄 Licencia

Este software es de uso privado para **Bodega de Belén**.

Todos los derechos reservados © 2026

---

## 👨‍💻 Autor

Desarrollado para **Bodega de Belén**

---

## 📞 Soporte

Para soporte técnico:
- Ejecuta `verificar_datos.py` y envía el resultado
- Incluye mensaje de error completo
- Indica versión del software

---

## 🎯 Roadmap

### Versión Actual (2.0)
- ✅ Sistema de ventas completo
- ✅ Gestión de inventario
- ✅ Sistema de actualización segura
- ✅ Soporte productos por peso/unidad

### Futuras Mejoras
- 🔲 App móvil para consultas
- 🔲 Reportes PDF
- 🔲 Integración con impresora térmica
- 🔲 Múltiples sucursales
- 🔲 Sistema de empleados y permisos

---

## 📸 Capturas de Pantalla

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Gestión de Inventario
![Inventario](docs/screenshots/inventario.png)

### Crear Venta
![Ventas](docs/screenshots/ventas.png)

---

## ⭐ Agradecimientos

- Django Team por el excelente framework
- Bootstrap por los componentes UI
- Comunidad Python por las librerías

---

**Última actualización:** 18 de Enero, 2026  
**Versión:** 2.0  
**Estado:** Producción ✅
