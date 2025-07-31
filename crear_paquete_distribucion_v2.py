#!/usr/bin/env python3
"""
Script para crear paquete de distribución v2.0
Incluye todas las nuevas funcionalidades:
- Formularios PDF funcionales
- Edición y reenvío de certificados
- Base de datos mejorada
- Interfaz gráfica completa
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime


def crear_paquete_distribucion_v2():
    """Crear paquete de distribución con todas las mejoras"""

    # Configuración
    nombre_paquete = "CertificadorBautismos_v2"
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    paquete_dir = Path(f"{nombre_paquete}_{fecha}")

    print("🚀 CREANDO PAQUETE DE DISTRIBUCIÓN v2.0")
    print("=" * 50)

    # 1. Crear directorio del paquete
    paquete_dir.mkdir(exist_ok=True)
    print(f"✅ Directorio creado: {paquete_dir}")

    # 2. Buscar el ejecutable
    dist_dir = Path("dist")
    ejecutable_encontrado = None

    if dist_dir.exists():
        for archivo in dist_dir.glob("*.exe"):
            if "CertificadorBautismos" in archivo.name:
                ejecutable_encontrado = archivo
                break

    if ejecutable_encontrado:
        print(f"✅ Ejecutable encontrado: {ejecutable_encontrado.name}")

        # 3. Copiar ejecutable al paquete
        destino_ejecutable = paquete_dir / "CertificadorBautismos.exe"
        shutil.copy2(ejecutable_encontrado, destino_ejecutable)
        print(f"✅ Ejecutable copiado a: {destino_ejecutable}")
    else:
        print("⚠️  Ejecutable no encontrado. Asegúrate de compilar primero.")
        return False

    # 4. Crear carpeta data en el paquete
    paquete_data_dir = paquete_dir / "data"
    paquete_data_dir.mkdir(exist_ok=True)

    # 5. Copiar archivos de datos
    data_dir = Path("data")
    if data_dir.exists():
        print("📁 Copiando archivos de datos...")
        for archivo in data_dir.glob("*"):
            if archivo.is_file():
                destino = paquete_data_dir / archivo.name
                shutil.copy2(archivo, destino)
                print(f"✅ Copiado: {archivo.name}")

    # 6. Crear carpeta output
    paquete_output_dir = paquete_dir / "output"
    paquete_output_dir.mkdir(exist_ok=True)
    print("✅ Carpeta output creada")

    # 7. Crear archivo .env de ejemplo
    env_ejemplo = paquete_dir / ".env.ejemplo"
    with open(env_ejemplo, "w", encoding="utf-8") as f:
        f.write(
            """# Configuración de Email - Certificador de Bautismos v2.0
# Copia este archivo como .env y configura tus credenciales

# Email del remitente
EMAIL_SENDER=tu_email@gmail.com

# Contraseña de aplicación (NO tu contraseña normal)
EMAIL_PASSWORD=tu_contraseña_de_aplicación

# Servidor SMTP (Gmail por defecto)
SMTP_SERVER=smtp.gmail.com

# Puerto SMTP (587 para TLS, 465 para SSL)
SMTP_PORT=587

# Instrucciones para Gmail:
# 1. Activa la verificación en dos pasos en tu cuenta de Google
# 2. Ve a "Seguridad" > "Contraseñas de aplicación"
# 3. Genera una nueva contraseña para "Correo"
# 4. Usa esa contraseña aquí (no tu contraseña normal)
"""
        )
    print("✅ Archivo .env.ejemplo creado")

    # 8. Crear archivo de información del paquete
    info_paquete = paquete_dir / "INFO_PAQUETE_v2.txt"
    with open(info_paquete, "w", encoding="utf-8") as f:
        f.write(
            f"""🎯 CERTIFICADOR DE BAUTISMOS v2.0
{'='*50}

📦 PAQUETE DE DISTRIBUCIÓN
Fecha de creación: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
Versión: 2.0

🚀 NUEVAS FUNCIONALIDADES v2.0:
✅ Formularios PDF funcionales
✅ Edición y reenvío de certificados
✅ Base de datos mejorada
✅ Interfaz gráfica completa
✅ Detección automática de campos
✅ Mapeo configurable de campos
✅ Regeneración de certificados
✅ Reenvío de emails

📁 ESTRUCTURA DEL PAQUETE:
├── CertificadorBautismos.exe    # Aplicación principal
├── data/                        # Archivos de configuración
│   ├── template.pdf             # Template PDF
│   └── field_mapping.json       # Mapeo de campos (opcional)
├── output/                      # Certificados generados
├── .env.ejemplo                 # Configuración de email
└── INFO_PAQUETE_v2.txt         # Este archivo

🎯 INSTRUCCIONES DE USO:

1. CONFIGURACIÓN INICIAL:
   - Copia .env.ejemplo como .env
   - Configura tus credenciales de email
   - Asegúrate de que data/template.pdf existe

2. EJECUTAR LA APLICACIÓN:
   - Doble clic en CertificadorBautismos.exe
   - O desde línea de comandos: CertificadorBautismos.exe

3. FUNCIONES PRINCIPALES:
   - Agregar nuevos bautismos
   - Generar certificados automáticamente
   - Enviar emails con certificados
   - Editar datos existentes
   - Regenerar certificados
   - Reenviar emails

4. EDICIÓN DE DATOS:
   - Selecciona un bautismo en la lista
   - Haz clic en "✏️ Editar Seleccionado"
   - Modifica los datos
   - Guarda cambios y regenera certificado

5. CONFIGURACIÓN DE CAMPOS:
   - Si tu PDF tiene campos diferentes, edita data/field_mapping.json
   - Formato: {{"NOMBRE_COMPLETO": "tu_campo", ...}}

📞 SOPORTE:
- Revisa los logs en la consola para errores
- Verifica que el template PDF tenga campos válidos
- Asegúrate de que la configuración de email sea correcta

🎉 ¡Disfruta usando el Certificador de Bautismos v2.0!
"""
        )
    print("✅ Archivo de información creado")

    # 9. Crear README específico para v2.0
    readme_v2 = paquete_dir / "README_v2.md"
    with open(readme_v2, "w", encoding="utf-8") as f:
        f.write(
            """# Certificador de Bautismos v2.0

## 🎯 Nuevas Funcionalidades

### ✅ Formularios PDF Funcionales
- Detección automática de campos de formulario
- Rellenado correcto de campos PDF
- Soporte para múltiples tipos de campos

### ✅ Edición y Reenvío
- Editar datos de bautismos existentes
- Regenerar certificados con datos corregidos
- Reenviar emails con certificados actualizados

### ✅ Base de Datos Mejorada
- Funciones de actualización de registros
- Regeneración de certificados
- Mejor manejo de errores

### ✅ Interfaz Gráfica Completa
- Botón de edición integrado
- Ventana de edición dedicada
- Validación de datos en tiempo real

## 🚀 Instalación

1. **Extraer el paquete** en una carpeta
2. **Configurar email** (opcional):
   - Copiar `.env.ejemplo` como `.env`
   - Editar con tus credenciales
3. **Ejecutar**: `CertificadorBautismos.exe`

## 📋 Uso

### Agregar Nuevo Bautismo
1. Llenar formulario con datos
2. Hacer clic en "💾 Guardar"
3. Generar certificado automáticamente

### Editar Bautismo Existente
1. Seleccionar bautismo en la lista
2. Hacer clic en "✏️ Editar Seleccionado"
3. Modificar datos en ventana de edición
4. Guardar cambios y regenerar certificado

### Reenviar Email
1. Abrir ventana de edición
2. Hacer clic en "📧 Reenviar Email"
3. Email se envía con certificado actualizado

## 🔧 Configuración Avanzada

### Mapeo de Campos
Si tu PDF tiene campos diferentes, edita `data/field_mapping.json`:

```json
{
  "NOMBRE_COMPLETO": "[TU_CAMPO_NOMBRE]",
  "FECHA_BAUTISMO": "[TU_CAMPO_FECHA]",
  "NOMBRE_IGLESIA": "[TU_CAMPO_IGLESIA]"
}
```

### Template PDF
- Coloca tu template en `data/template.pdf`
- Asegúrate de que tenga campos de formulario válidos
- Los campos deben tener nombres específicos

## 📞 Soporte

- **Logs**: Revisa la consola para mensajes de error
- **Campos**: Verifica que el PDF tenga campos de formulario
- **Email**: Confirma configuración SMTP en `.env`

---

**¡Versión 2.0 completamente funcional!** 🎉
"""
        )
    print("✅ README v2.0 creado")

    # 10. Crear archivo de versiones
    versiones = paquete_dir / "VERSIONES.txt"
    with open(versiones, "w", encoding="utf-8") as f:
        f.write(
            """VERSIONES DEL CERTIFICADOR DE BAUTISMOS
===============================================

v2.0 (Actual) - {fecha}
✅ Formularios PDF funcionales
✅ Edición y reenvío de certificados
✅ Base de datos mejorada
✅ Interfaz gráfica completa
✅ Detección automática de campos
✅ Mapeo configurable de campos
✅ Regeneración de certificados
✅ Reenvío de emails
✅ Corrección PyPDF2 3.0.0

v1.0 (Anterior)
✅ Generación básica de certificados
✅ Envío de emails
✅ Interfaz gráfica básica
✅ Base de datos SQLite
⚠️ Problemas con formularios PDF
⚠️ Sin funcionalidad de edición

CAMBIOS PRINCIPALES v2.0:
- Corregido problema con PyPDF2 3.0.0
- Agregada funcionalidad de edición completa
- Mejorada detección de campos de formulario
- Agregado mapeo configurable de campos
- Implementada regeneración de certificados
- Agregado reenvío de emails
- Mejorada interfaz de usuario
- Agregada validación de datos
- Mejorado manejo de errores
"""
        )
    print("✅ Archivo de versiones creado")

    # 11. Crear ZIP del paquete
    zip_path = f"{nombre_paquete}_{fecha}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(paquete_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, paquete_dir)
                zipf.write(file_path, arcname)

    print(f"✅ Paquete ZIP creado: {zip_path}")

    # 12. Resumen final
    print("\n" + "=" * 50)
    print("🎉 PAQUETE DE DISTRIBUCIÓN v2.0 CREADO")
    print("=" * 50)
    print(f"📦 Directorio: {paquete_dir}")
    print(f"📦 ZIP: {zip_path}")
    print(f"📄 Ejecutable: {destino_ejecutable}")
    print(f"📁 Datos: {paquete_data_dir}")
    print(f"📁 Salida: {paquete_output_dir}")
    print("\n🚀 ¡Listo para distribuir!")

    return True


if __name__ == "__main__":
    crear_paquete_distribucion_v2()
