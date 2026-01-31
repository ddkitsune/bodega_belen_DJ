# 🚀 GUÍA PARA CREAR EJECUTABLE DE WINDOWS

## 📋 OPCIÓN 1: USO SIMPLE CON BATCH (RECOMENDADO)

### **Para ti o usuarios en la misma PC:**

**Archivo creado:** `INICIAR_BODEGA.bat`

**¿Cómo usarlo?**
1. Doble click en `INICIAR_BODEGA.bat`
2. Se abre automáticamente el navegador
3. ¡Listo! El sistema está funcionando

**Ventajas:**
- ✅ No requiere instalación adicional
- ✅ Funciona inmediatamente
- ✅ Fácil de usar

---

## 📦 OPCIÓN 2: CREAR EJECUTABLE .EXE

### **Para distribuir a otras computadoras:**

#### **Paso 1: Instalar PyInstaller**

```bash
pip install pyinstaller
```

#### **Paso 2: Crear el ejecutable**

**Método Simple (con consola visible):**
```bash
pyinstaller --onefile inicio_bodega.py
```

**Método Sin Consola:**
```bash
pyinstaller --onefile --noconsole inicio_bodega.py
```

**Método Con Ícono Personalizado:**
```bash
pyinstaller --onefile --noconsole --icon=icono.ico inicio_bodega.py
```

#### **Paso 3: Encontrar el ejecutable**

El archivo `.exe` estará en: `dist/inicio_bodega.exe`

#### **Paso 4: Preparar para distribución**

Debes copiar junto al `.exe`:

```
📁 Bodega_Belen_Portable/
├── 📄 inicio_bodega.exe        ← El ejecutable
├── 📄 manage.py
├── 📁 bodega_belen/            ← Carpeta del proyecto
├── 📁 inventario/
├── 📁 ventas/
├── 📁 clientes/
├── 📁 templates/
├── 📁 static/
├── 📄 db.sqlite3              ← Base de datos (si usas SQLite)
└── 📄 requirements.txt
```

---

## 🎨 OPCIÓN 3: CREAR INSTALADOR PROFESIONAL

### **Con Inno Setup (Windows Installer):**

#### **Paso 1: Descargar Inno Setup**
https://jrsoftware.org/isdl.php

#### **Paso 2: Crear script de instalación**

Archivo creado: `installer_script.iss` (ver abajo)

#### **Paso 3: Compilar con Inno Setup**

1. Abrir Inno Setup
2. Abrir `installer_script.iss`
3. Click en "Compile"
4. ¡Listo! Tendrás `Setup_BodegaBelen.exe`

---

## ⚡ USO RÁPIDO (SIN CREAR .EXE)

### **Método 1: Doble Click en .BAT**
```
Doble click en: INICIAR_BODEGA.bat
```

### **Método 2: Acceso Directo**
1. Click derecho en `INICIAR_BODEGA.bat`
2. Crear acceso directo
3. Mover al escritorio
4. Opcional: Cambiar ícono

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### **Error: "Python no reconocido"**
- Asegúrate de tener Python instalado
- Agrega Python al PATH

### **Error: "No se encuentra manage.py"**
- Ejecuta el script desde la carpeta del proyecto
- Verifica que todos los archivos estén presentes

### **Error: "Puerto 8000 en uso"**
- Cierra otras instancias del servidor
- O cambia el puerto en el script

---

## 📊 COMPARACIÓN DE MÉTODOS

| Método | Facilidad | Distribución | Profesional |
|--------|-----------|--------------|-------------|
| .BAT | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| .EXE | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Instalador | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## ✅ RECOMENDACIÓN

**Para tu caso:**
- 🏠 **Uso personal:** Usa `INICIAR_BODEGA.bat` → ¡Ya está listo!
- 💼 **Distribución local:** Crea `.exe` con PyInstaller
- 🏢 **Distribución profesional:** Usa Inno Setup

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Prueba el archivo `INICIAR_BODEGA.bat`
2. ✅ Si funciona bien, úsalo así
3. ✅ Si necesitas distribuir, crea el `.exe`

**¡El sistema está listo para usar!** 🎉
