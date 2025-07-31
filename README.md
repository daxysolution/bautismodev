# 🎯 Certificador de Bautismos

Aplicación completa para automatizar la generación de certificados de bautismo y el envío de emails con certificados adjuntos.

## 📋 Características

- ✅ **Interfaz gráfica** con Tkinter para fácil uso
- ✅ **Base de datos SQLite** para almacenar registros
- ✅ **Generación automática** de certificados PDF
- ✅ **Envío de emails** con certificados adjuntos
- ✅ **Validación de fechas** (solo procesa bautismos pasados)
- ✅ **Evita duplicados** automáticamente
- ✅ **Exportación a Excel** para compatibilidad
- ✅ **Modo línea de comandos** para automatización
- ✅ **Compatibilidad PyInstaller** para crear ejecutables

## 🏗️ Estructura del Proyecto

```
certificador_bautismos/
├── main.py                 # Punto de entrada principal
├── gui_app.py              # Interfaz gráfica
├── cli_app.py              # Interfaz línea de comandos
├── services/
│   ├── database_service.py # Servicio de base de datos
│   ├── pdf_service.py      # Servicio de generación PDF
│   └── mail_service.py     # Servicio de envío emails
├── data/                   # Archivos de entrada
│   └── Texto del párrafo.pdf  # Template PDF para certificados
├── output/                 # Certificados generados
├── bautismos.db           # Base de datos SQLite
├── .env                   # Configuración de email
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- pip

### Pasos de instalación

1. **Clonar o descargar** el proyecto
2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar email** (opcional):
   - Copiar `env_example.txt` como `.env`
   - Editar con tus credenciales SMTP

## 🎯 Uso

### Interfaz Gráfica (Recomendado)
```bash
python main.py --gui
```

### Línea de Comandos (SQLite)
```bash
python main.py
# o
python cli_app.py
```

### Ejecutable Compilado
```bash
# Usar el ejecutable ya compilado
./paquete_compartir/CertificadorBautismos.exe
```

### Crear Ejecutable
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

## 📊 Funcionalidades

### 1. Gestión de Bautismos
- **Agregar registros** con formulario intuitivo
- **Validación automática** de datos
- **Búsqueda y filtrado** de registros
- **Estadísticas en tiempo real**

### 2. Generación de Certificados
- **Plantilla personalizable** en PDF
- **Formato de fecha** en español
- **Nombres de archivo** seguros
- **Evita duplicados** automáticamente

### 3. Envío de Emails
- **Configuración SMTP** flexible
- **Emails personalizados** con nombre
- **Certificados adjuntos** automáticamente
- **Seguimiento** de envíos

### 4. Base de Datos SQLite
- **Almacenamiento local** con SQLite
- **Gestión completa** de registros
- **Exportación** a Excel (opcional)
- **Estadísticas** detalladas
- **Sin dependencias** externas

## ⚙️ Configuración

### Archivo .env
```env
EMAIL_SENDER=tu_email@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_aplicación
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Para Gmail
1. Activar verificación en dos pasos
2. Generar contraseña de aplicación
3. Usar esa contraseña en `.env`

## 📁 Archivos de Datos

### Excel (Modo tradicional)
- **nombre completo**: Nombre de la persona
- **Email**: Dirección de correo
- **Fecha de bautizmo**: Formato DD/MM/AAAA
- **celula**: Nombre de la iglesia (opcional)

### Base de Datos (Modo moderno)
- Datos almacenados automáticamente
- Validaciones integradas
- Búsquedas avanzadas
- Exportación flexible

## 🔧 Solución de Problemas

### Error de configuración de email
- Verificar archivo `.env` existe
- Confirmar credenciales correctas
- Para Gmail, usar contraseña de aplicación

### Error de archivos
- Verificar archivos en carpeta `data/`
- Confirmar nombres exactos
- Verificar permisos de escritura

### Error de PyInstaller
- Instalar todas las dependencias
- Verificar archivos de datos en ubicación correcta
- Usar `--onefile` para ejecutable único

## 📈 Estadísticas

La aplicación proporciona estadísticas en tiempo real:
- **Total de registros**
- **Certificados pendientes**
- **Certificados completados**
- **Emails enviados**

## 🎨 Personalización

### Plantilla PDF
- Editar `data/Texto del párrafo.pdf`
- Mantener campos de formulario
- Usar nombres de campos específicos

### Emails
- Personalizar mensaje en `mail_service.py`
- Cambiar asunto y contenido
- Agregar firmas personalizadas

### Verificación de instalación
```bash
python -c "import tkinter; print('✅ Tkinter disponible')"
python -c "import pandas; print('✅ Pandas disponible')"
python -c "import PyPDF2; print('✅ PyPDF2 disponible')"
```

### Logs de error
- Revisar consola para mensajes de error
- Verificar archivos de configuración
- Comprobar permisos de archivos

## 🔄 Actualizaciones

### Versión 1.0
- ✅ Interfaz gráfica completa
- ✅ Base de datos SQLite
- ✅ Generación de certificados
- ✅ Envío de emails
- ✅ Exportación a Excel
- ✅ Modo línea de comandos
- ✅ Compatibilidad PyInstaller
