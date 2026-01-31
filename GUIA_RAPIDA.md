# 🚀 Guía Rápida de Inicio

## Pasos para ejecutar el proyecto localmente

### 1. Configurar PostgreSQL

Tienes dos opciones:

#### Opción A: Usar SQLite temporalmente (más fácil para empezar)

Edita `bodega_belen/settings.py` y temporalmente cambia:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Opción B: Configurar PostgreSQL (recomendado)

1. Instalar PostgreSQL desde https://www.postgresql.org/download/
2. Crear base de datos:
   ```sql
   CREATE DATABASE bodega_belen;
   ```
3. Configurar `.env` con las credenciales

### 2. Crear entorno virtual y instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ejecutar migraciones

```bash
python manage.py migrate
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
```

Ingresa:
- Usuario: admin
- Email: admin@bodega.com
- Contraseña: (tu contraseña)

### 5. Crear tasa de cambio inicial

```bash
python manage.py actualizar_tasa
```

O desde el shell:
```bash
python manage.py shell
```

```python
from ventas.models import TasaCambio
from decimal import Decimal
TasaCambio.objects.create(tasa=Decimal('40.00'), fuente='Manual')
exit()
```

### 6. Ejecutar servidor

```bash
python manage.py runserver
```

### 7. Acceder al sistema

- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin

### 8. Primeros pasos en el sistema

1. **Login** con el superusuario
2. **Dashboard** → Actualizar tasa de cambio BCV
3. **Admin** → Crear algunas categorías (opcional)
4. **Admin** → Crear productos de prueba
5. **Admin** → Crear clientes de prueba
6. **Nueva Venta** → Realizar primera venta

## Datos de Prueba Recomendados

### Categorías
- Alimentos
- Bebidas
- Limpieza
- Otros

### Productos de Ejemplo
```
Código: PROD001
Nombre: Arroz 1kg
Precio USD: 2.50
Cantidad: 100

Código: PROD002
Nombre: Azúcar 1kg  
Precio USD: 1.80
Cantidad: 50
```

### Cliente de Ejemplo
```
Tipo: V
Documento: 12345678
Nombre: Juan
Apellido: Pérez
Tiene Crédito: Sí
Límite: 500.00 USD
```

## Comandos Útiles

```bash
# Actualizar tasa BCV
python manage.py actualizar_tasa

# Crear superusuario
python manage.py createsuperuser

# Ejecutar migraciones
python manage.py migrate

# Acceder a shell de Django
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic
```

## Solución de Problemas Rápidos

### Puerto 8000 ocupado
```bash
python manage.py runserver 8080
```

### Error de base de datos
- Verificar PostgreSQL esté corriendo
- Verificar credenciales en `.env`
- Usar SQLite temporalmente

### Error de tasa de cambio
- Crear manualmente desde el admin o shell
- O desde la interfaz: Tasas de Cambio → Crear Manualmente

---

¡Listo! El sistema está configurado y funcionando. 🎉
