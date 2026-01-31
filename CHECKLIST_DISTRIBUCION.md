# ✅ CHECKLIST DE DISTRIBUCIÓN - Nueva Versión

## 📋 Antes de Compilar

- [ ] Todos los cambios están commiteados en Git
- [ ] Los templates están corregidos (sin tags divididos)
- [ ] Las migraciones están creadas (`python manage.py makemigrations`)
- [ ] Las migraciones fueron probadas en BD de prueba
- [ ] El código fue probado en desarrollo
- [ ] No hay errores en consola
- [ ] Todas las vistas funcionan correctamente

## 🔧 Compilación

- [ ] Cerrar todas las instancias de BodegaBelen.exe
- [ ] Ejecutar: `pyinstaller --clean bodega.spec`
- [ ] Compilación completada sin errores
- [ ] Verificar que `dist/BodegaBelen.exe` existe
- [ ] Verificar tamaño del ejecutable (debe ser ~40-50 MB)

## 🧪 Pruebas del Ejecutable

### Instalación Nueva
- [ ] Crear carpeta de prueba vacía
- [ ] Copiar BodegaBelen.exe
- [ ] Ejecutar el programa
- [ ] Verificar que crea db.sqlite3
- [ ] Crear un producto de prueba
- [ ] Crear un cliente de prueba
- [ ] Crear una venta de prueba
- [ ] Verificar que todo funciona

### Actualización desde Versión Anterior
- [ ] Crear carpeta con versión anterior + datos de prueba
- [ ] Copiar db.sqlite3 con datos reales de prueba
- [ ] Ejecutar BACKUP_AUTOMATICO.bat
- [ ] Verificar que se creó el backup
- [ ] Copiar nuevo BodegaBelen.exe
- [ ] Ejecutar el nuevo programa
- [ ] Verificar que aplica migraciones automáticamente
- [ ] Verificar que los datos antiguos siguen ahí:
  - [ ] Productos
  - [ ] Categorías
  - [ ] Clientes
  - [ ] Ventas
  - [ ] Tasa de cambio
- [ ] Crear una venta nueva
- [ ] Verificar que los nuevos campos funcionan

### Restauración de Backup
- [ ] Ejecutar RESTAURAR_BACKUP.bat
- [ ] Verificar que lista los backups
- [ ] Restaurar un backup
- [ ] Verificar que los datos se restauraron correctamente

## 📦 Preparar Paquete de Distribución

- [ ] Crear carpeta: `BodegaBelen_v[VERSION]`
- [ ] Copiar archivos necesarios:
  - [ ] BodegaBelen.exe (desde dist/)
  - [ ] LEEME.txt
  - [ ] GUIA_ACTUALIZACION.md
  - [ ] LEEME_DISTRIBUCION.md
  - [ ] BACKUP_AUTOMATICO.bat
  - [ ] ACTUALIZAR.bat
  - [ ] RESTAURAR_BACKUP.bat
  - [ ] verificar_datos.py

## 📝 Actualizar Documentación

- [ ] Actualizar LEEME_DISTRIBUCION.md:
  - [ ] Número de versión
  - [ ] Fecha de lanzamiento
  - [ ] Nuevas características
  - [ ] Cambios en BD (migraciones)
  - [ ] Bugs corregidos

- [ ] Actualizar LEEME.txt:
  - [ ] Verificar que las instrucciones siguen siendo correctas
  - [ ] Actualizar fecha

- [ ] Crear CHANGELOG.txt con:
  ```
  Versión X.X - DD/MM/YYYY
  
  Nuevas Características:
  - [Lista de nuevas características]
  
  Mejoras:
  - [Lista de mejoras]
  
  Correcciones:
  - [Lista de bugs corregidos]
  
  Cambios en Base de Datos:
  - [Lista de migraciones aplicadas]
  ```

## 🗜️ Comprimir y Distribuir

- [ ] Comprimir carpeta en ZIP
- [ ] Nombre del archivo: `BodegaBelen_v[VERSION]_[FECHA].zip`
- [ ] Verificar que el ZIP contiene todos los archivos
- [ ] Probar descomprimir en carpeta nueva
- [ ] Ejecutar desde el ZIP descomprimido

## 📧 Comunicación con Usuario

- [ ] Preparar email/mensaje con:
  - [ ] Enlace de descarga
  - [ ] Instrucciones básicas
  - [ ] Recordatorio de hacer backup
  - [ ] Novedades principales
  - [ ] Contacto para soporte

Ejemplo de mensaje:

```
Hola,

Está disponible la nueva versión X.X de Bodega de Belén.

🎉 Novedades:
- [Lista de novedades principales]

📥 Descarga:
[Enlace al archivo ZIP]

⚠️ IMPORTANTE antes de actualizar:
1. Cierra el programa
2. Ejecuta BACKUP_AUTOMATICO.bat
3. Sigue las instrucciones del archivo LEEME.txt

📚 Documentación:
Dentro del ZIP encontrarás:
- LEEME.txt: Instrucciones rápidas
- GUIA_ACTUALIZACION.md: Guía completa

🆘 Soporte:
Si tienes algún problema, contáctame con:
- Versión que tenías antes
- Mensaje de error (si hay)
- Resultado de verificar_datos.py

¡Saludos!
```

## 🔍 Verificación Final

- [ ] El ZIP está en un lugar seguro
- [ ] Hay una copia de respaldo del ZIP
- [ ] La documentación está completa
- [ ] Las instrucciones son claras
- [ ] Se probó todo el proceso de actualización
- [ ] Se probó la restauración de backup

## 📊 Post-Distribución

- [ ] Hacer seguimiento con el usuario después de 24h
- [ ] Preguntar si todo funciona correctamente
- [ ] Resolver cualquier problema que surja
- [ ] Documentar problemas encontrados para la próxima versión

## 🐛 Si Hay Problemas

Si el usuario reporta problemas:

1. [ ] Pedirle que ejecute `verificar_datos.py`
2. [ ] Pedirle que envíe el resultado
3. [ ] Pedirle que describa el problema exacto
4. [ ] Si es crítico, pedirle que restaure el backup
5. [ ] Investigar el problema
6. [ ] Crear hotfix si es necesario
7. [ ] Distribuir corrección

---

## 📝 Notas

**Versión actual:** _____
**Fecha de compilación:** _____
**Probado por:** _____
**Distribuido el:** _____
**Problemas reportados:** _____

---

**Última actualización del checklist:** 18 de Enero, 2026
