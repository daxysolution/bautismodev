# Certificador de Bautismos - Sistema de Formularios PDF

## 🎯 Descripción

Este sistema ha sido adaptado para trabajar con formularios PDF que contienen campos rellenables. El script puede detectar automáticamente los campos del formulario y mapearlos a los datos correspondientes.

## 📋 Características Principales

- ✅ **Detección automática de campos**: Analiza tu PDF y encuentra todos los campos de formulario
- ✅ **Mapeo configurable**: Permite configurar qué campo del formulario corresponde a cada dato
- ✅ **Múltiples métodos de relleno**: Soporta tanto campos de formulario como reemplazo de texto
- ✅ **Análisis de templates**: Herramientas para analizar la estructura de tu PDF

## 🚀 Instalación y Configuración

### 1. Preparar el Template PDF

Coloca tu template PDF con campos de formulario en:
```
data/template.pdf
```

### 2. Analizar el Template

Ejecuta el script de análisis para ver qué campos tiene tu formulario:

```bash
python probar_formulario_pdf.py
```

### 3. Configurar el Mapeo de Campos

Si tu formulario tiene nombres de campos diferentes a los estándar, configura el mapeo:

```bash
python configurar_campos_formulario.py
```

Este script te ayudará a:
- Ver todos los campos disponibles en tu formulario
- Asignar cada campo a su función (nombre, fecha, iglesia)
- Guardar la configuración para uso futuro

## 📝 Uso del Sistema

### Opción 1: Interfaz Gráfica
```bash
python main.py --gui
```

### Opción 2: Línea de Comandos
```bash
python main.py
```

### Opción 3: Script de Prueba
```bash
python probar_formulario_pdf.py
```

## 🔧 Configuración Avanzada

### Estructura del Mapeo de Campos

El archivo `data/field_mapping.json` contiene la configuración:

```json
{
  "NOMBRE_COMPLETO": "campo_nombre_formulario",
  "FECHA_BAUTISMO": "campo_fecha_formulario", 
  "NOMBRE_IGLESIA": "campo_iglesia_formulario"
}
```

### Nombres de Campos Estándar

Si no configuras un mapeo, el sistema intentará usar estos nombres:

**Para el nombre:**
- `NOMBRE_COMPLETO`
- `NOMBRE`
- `NOMBRE_PERSONA`

**Para la fecha:**
- `FECHA_BAUTISMO`
- `FECHA`
- `FECHA_CEREMONIA`

**Para la iglesia:**
- `NOMBRE_IGLESIA`
- `IGLESIA`
- `NOMBRE_TEMPLO`

## 🛠️ Herramientas Disponibles

### 1. `probar_formulario_pdf.py`
- Analiza tu template PDF
- Muestra todos los campos encontrados
- Genera certificados de prueba
- Verifica el funcionamiento del sistema

### 2. `configurar_campos_formulario.py`
- Crea mapeo de campos
- Visualiza configuración actual
- Analiza estructura del template

### 3. `services/pdf_service.py`
- Funciones principales del sistema
- Detección automática de campos
- Múltiples métodos de relleno

## 📊 Flujo de Trabajo

1. **Preparación**: Coloca tu template PDF en `data/template.pdf`
2. **Análisis**: Ejecuta `probar_formulario_pdf.py` para ver los campos
3. **Configuración**: Si es necesario, ejecuta `configurar_campos_formulario.py`
4. **Uso**: Usa la aplicación principal para generar certificados

## 🔍 Solución de Problemas

### El PDF no se rellena correctamente

1. **Verifica los nombres de campos**:
   ```bash
   python configurar_campos_formulario.py
   ```

2. **Analiza el template**:
   ```bash
   python probar_formulario_pdf.py
   ```

3. **Revisa los logs**: El sistema muestra qué campos encuentra y rellena

### No se encuentran campos de formulario

- Asegúrate de que tu PDF tenga campos de formulario (no solo texto)
- Usa un editor PDF como Adobe Acrobat o similar para crear campos
- Verifica que los campos no estén bloqueados o protegidos

### Error de mapeo

- Elimina el archivo `data/field_mapping.json` para usar nombres por defecto
- Reconfigura el mapeo con `configurar_campos_formulario.py`

## 📁 Estructura de Archivos

```
certificado bautizmo app/
├── data/
│   ├── template.pdf              # Tu template PDF
│   └── field_mapping.json       # Configuración de campos (opcional)
├── output/                      # Certificados generados
├── services/
│   └── pdf_service.py           # Servicio principal
├── probar_formulario_pdf.py     # Script de prueba
├── configurar_campos_formulario.py  # Configurador
└── main.py                      # Aplicación principal
```

## 🎨 Personalización

### Agregar Nuevos Campos

Para agregar nuevos tipos de campos, edita `services/pdf_service.py`:

1. Agrega el campo al mapeo estándar
2. Actualiza la función `generate_certificate`
3. Modifica `configurar_campos_formulario.py` si es necesario

### Cambiar el Formato de Fecha

Modifica la función `format_date` en `services/pdf_service.py` para cambiar el formato de fecha.

## 📞 Soporte

Si tienes problemas:

1. Ejecuta `probar_formulario_pdf.py` y revisa la salida
2. Verifica que tu PDF tenga campos de formulario válidos
3. Revisa los logs para identificar errores específicos

---

**¡El sistema está listo para trabajar con tu formulario PDF!** 🎉 