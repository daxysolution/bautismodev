# 🎯 Certificador de Bautismos v2.0

## 📧 **CONFIGURACIÓN DE EMAIL (IMPORTANTE)**

### ¿Por qué configurar email?
Para enviar automáticamente los certificados por email a los bautizados.

### Paso a Paso:

#### 1. **Preparar tu cuenta de Gmail**
- Ve a tu cuenta de Google
- Activa la **"Verificación en dos pasos"**
- Ve a **"Seguridad"** → **"Contraseñas de aplicación"**
- Genera una nueva contraseña para **"Correo"**
- **Guarda esta contraseña** (NO es tu contraseña normal)

#### 2. **Configurar la aplicación**
- Copia el archivo `.env.ejemplo` y renómbralo a `.env`
- Abre el archivo `.env` con el Bloc de notas
- Cambia estas líneas:
  ```
  EMAIL_SENDER=tu_email@gmail.com
  EMAIL_PASSWORD=la_contraseña_de_aplicación_que_generaste
  ```
- Guarda el archivo

#### 3. **Probar la configuración**
- Ejecuta la aplicación
- Haz clic en **"🔧 Probar Email"**
- Si aparece "✅ Conexión exitosa", ¡está listo!

## 🚀 **CÓMO USAR LA APLICACIÓN**

### **Agregar un nuevo bautismo:**
1. Llena el formulario con los datos
2. Haz clic en **"💾 Guardar"**
3. ¡Listo! El bautismo queda registrado

### **Generar certificados:**
1. Haz clic en **"🖨️ Generar Certificados"**
2. Los certificados se guardan en la carpeta `output/`
3. Cada certificado tendrá el nombre de la persona

### **Enviar emails automáticamente:**
1. Asegúrate de que el email esté configurado (ver arriba)
2. Haz clic en **"📧 Enviar Emails"**
3. Los certificados se envían automáticamente

### **Editar un bautismo:**
1. Selecciona el bautismo en la lista
2. Haz doble clic o presiona **"✏️ Editar Seleccionado"**
3. Modifica los datos que necesites
4. Guarda los cambios

### **Exportar a Excel:**
1. Haz clic en **"📊 Exportar a Excel"**
2. Elige dónde guardar el archivo
3. ¡Listo! Tienes todos los datos en Excel

## 📊 **ESTADÍSTICAS**

La aplicación te muestra:
- **Total de registros**
- **Certificados pendientes**
- **Certificados completados**
- **Emails enviados**

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **"Error de configuración de email"**
- Verifica que el archivo `.env` existe
- Confirma que la contraseña de aplicación es correcta
- Asegúrate de que la verificación en dos pasos esté activada

### **"No se pueden generar certificados"**
- Verifica que existe el archivo `data/template.pdf`
- Asegúrate de que el PDF tenga campos de formulario

### **"Error al enviar emails"**
- Prueba la configuración con **"🔧 Probar Email"**
- Verifica tu conexión a internet
- Confirma que las credenciales son correctas

### **"La aplicación no abre"**
- Asegúrate de ejecutar `CertificadorBautismos.exe`
- Verifica que Windows Defender no bloquee la aplicación

## 📁 **ARCHIVOS IMPORTANTES**

- **`CertificadorBautismos.exe`** - La aplicación principal
- **`.env`** - Configuración de email (crear desde `.env.ejemplo`)
- **`data/template.pdf`** - Plantilla de certificado
- **`output/`** - Carpeta donde se guardan los certificados
- **`bautismos.db`** - Base de datos (se crea automáticamente)

## 🎉 **¡LISTO PARA USAR!**

**Solo ejecuta `CertificadorBautismos.exe` y comienza a registrar bautismos.**

---

**¿Necesitas ayuda?** Revisa la sección "Solución de Problemas" arriba.
