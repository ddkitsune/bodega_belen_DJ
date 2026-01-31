#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificación de integridad de la base de datos
Verifica que todos los datos estén presentes después de una actualización
"""

import os
import sys
import sqlite3
from pathlib import Path

def verificar_base_datos():
    """Verifica la integridad de la base de datos"""
    
    print("═" * 60)
    print("  🔍 VERIFICACIÓN DE BASE DE DATOS - Bodega de Belén")
    print("═" * 60)
    print()
    
    # Buscar la base de datos
    db_path = Path('db.sqlite3')
    
    if not db_path.exists():
        print("❌ ERROR: No se encontró el archivo db.sqlite3")
        print()
        print("Asegúrate de ejecutar este script en la misma carpeta")
        print("donde está BodegaBelen.exe")
        return False
    
    print(f"✅ Base de datos encontrada: {db_path}")
    print(f"📊 Tamaño: {db_path.stat().st_size:,} bytes")
    print()
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tablas principales
        print("📋 Verificando tablas...")
        print()
        
        tablas_esperadas = [
            ('inventario_categoria', 'Categorías'),
            ('inventario_producto', 'Productos'),
            ('clientes_cliente', 'Clientes'),
            ('ventas_factura', 'Facturas'),
            ('ventas_detalleventa', 'Detalles de Venta'),
            ('ventas_tasacambio', 'Tasas de Cambio'),
        ]
        
        resultados = {}
        
        for tabla, nombre in tablas_esperadas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                resultados[nombre] = count
                print(f"  ✅ {nombre:20} → {count:5} registros")
            except sqlite3.OperationalError:
                resultados[nombre] = None
                print(f"  ⚠️  {nombre:20} → Tabla no existe")
        
        print()
        print("─" * 60)
        print()
        
        # Resumen
        print("📊 RESUMEN:")
        print()
        
        total_registros = sum(v for v in resultados.values() if v is not None)
        tablas_ok = sum(1 for v in resultados.values() if v is not None)
        
        print(f"  • Total de tablas verificadas: {len(tablas_esperadas)}")
        print(f"  • Tablas encontradas: {tablas_ok}")
        print(f"  • Total de registros: {total_registros:,}")
        print()
        
        # Verificar campos específicos en productos (para detectar migraciones)
        print("🔧 Verificando estructura de Productos...")
        cursor.execute("PRAGMA table_info(inventario_producto)")
        columnas = cursor.fetchall()
        
        campos_importantes = ['es_por_peso', 'precio_usd', 'cantidad', 'codigo']
        campos_encontrados = [col[1] for col in columnas]
        
        print()
        for campo in campos_importantes:
            if campo in campos_encontrados:
                print(f"  ✅ Campo '{campo}' existe")
            else:
                print(f"  ⚠️  Campo '{campo}' no encontrado")
        
        print()
        print("─" * 60)
        print()
        
        # Verificar integridad
        print("🔐 Verificando integridad de la base de datos...")
        cursor.execute("PRAGMA integrity_check")
        integridad = cursor.fetchone()[0]
        
        if integridad == 'ok':
            print("  ✅ La base de datos está íntegra")
        else:
            print(f"  ❌ Problemas de integridad: {integridad}")
        
        conn.close()
        
        print()
        print("═" * 60)
        print("  ✅ VERIFICACIÓN COMPLETADA")
        print("═" * 60)
        print()
        
        if tablas_ok == len(tablas_esperadas) and integridad == 'ok':
            print("✅ Todo está en orden. Puedes usar el sistema con confianza.")
            return True
        else:
            print("⚠️  Se detectaron algunas inconsistencias.")
            print("   Considera restaurar un backup si faltan datos importantes.")
            return False
            
    except Exception as e:
        print(f"❌ ERROR al verificar la base de datos: {e}")
        return False

if __name__ == '__main__':
    try:
        resultado = verificar_base_datos()
        print()
        input("Presiona ENTER para salir...")
        sys.exit(0 if resultado else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada por el usuario")
        sys.exit(1)
