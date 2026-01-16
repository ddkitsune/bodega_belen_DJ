# 🏪 Bodega de Belén - Sistema de Ventas

Sistema de gestión de ventas e inventario desarrollado con Django.

## ✨ Características

- 📦 **Gestión de Inventario**: Control de productos, categorías y stock
- 👥 **Gestión de Clientes**: Clientes con límite de crédito
- 💰 **Ventas**: Facturas de contado y crédito
- 💳 **Pagos**: Registro automático de pagos
- 📊 **Reportes**: Dashboard con estadísticas
- 💱 **Tasa de Cambio**: Integración con tasa BCV
- 📥📤 **Importar/Exportar**: Inventario desde/hacia Excel

## 🚀 Inicio Rápido

### Requisitos
- Python 3.11+
- pip

### Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/bodega-belen.git
cd bodega-belen

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

Abre tu navegador en: http://127.0.0.1:8000

### Inicio Rápido (Windows)

Simplemente ejecuta `INICIAR.bat`

## 🌐 Despliegue en Vercel (Gratis)

Este proyecto está configurado para desplegarse fácilmente en **Vercel** (la opción recomendada gratuita).

### 🚀 Pasos Rápidos

1. **Subir a GitHub**: Asegúrate de que tu código esté en GitHub.
2. **Crear Proyecto en Vercel**: Importa tu repositorio desde [vercel.com](https://vercel.com).
3. **Agregar Base de Datos (OBLIGATORIO)**:
   - SQLite no funciona en Vercel (se borra).
   - Usa la pestaña "Storage" en Vercel para crear una base de datos Postgres gratuita (Neon).
   - O conecta cualquier Postgres externo.
4. **Variables de Entorno**:
   - `SECRET_KEY`: Tu clave secreta.
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.vercel.app`
   
**Ver guía detallada**: `DESPLIEGUE_VERCEL.md`

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FDeivyg4%2Fbodega_belen_DJ)

## 📁 Estructura del Proyecto

```
bodega_belen/
├── bodega_belen/      # Configuración principal
├── inventario/        # App de inventario
├── ventas/            # App de ventas
├── clientes/          # App de clientes
├── templates/         # Plantillas HTML
├── static/            # Archivos estáticos
├── db.sqlite3         # Base de datos (desarrollo)
└── manage.py          # CLI de Django
```

## 🛠️ Tecnologías

- **Backend**: Django 5.2.9
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: Bootstrap 5
- **Importar/Exportar**: django-import-export, openpyxl

## 📝 Licencia

Este proyecto es privado.

## 👨‍💻 Autor

Desarrollado para Bodega de Belén
