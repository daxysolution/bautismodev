"""
Certificador de Bautismos - Interfaz de Línea de Comandos

Esta versión permite usar la aplicación desde la línea de comandos
sin necesidad de interfaz gráfica.
"""

import os
import sys
import pandas as pd
from datetime import datetime
from services.database_service import DatabaseService
from services.pdf_service import generate_certificate
from services.mail_service import (
    send_baptism_congratulations_email,
    test_email_configuration,
)


def get_data_path():
    """Get the path to the data directory"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "data")


def get_output_path():
    """Get the path to the output directory"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "output")


def validate_baptism_date(baptism_date_str):
    """
    Validate if baptism date has passed or is today.

    :param baptism_date_str: Date in DD/MM/YYYY format
    :return: True if date has passed or is today, False otherwise
    """
    try:
        # Handle NaN values
        if pd.isna(baptism_date_str):
            return False

        baptism_date = datetime.strptime(baptism_date_str, "%d/%m/%Y")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        return baptism_date <= today
    except Exception as e:
        print(f"❌ Error validando fecha {baptism_date_str}: {e}")
        return False


def process_baptism_certificates():
    """Main function to process baptism certificates"""
    print("🎯 Iniciando Certificador de Bautismos...")

    # Get paths
    data_path = get_data_path()
    output_path = get_output_path()

    # File paths
    excel_file = os.path.join(data_path, "liasta de certificados.xlsx")
    pdf_template = os.path.join(data_path, "template.pdf")

    # Check if files exist
    if not os.path.exists(excel_file):
        print(f"❌ Error: No se encontró el archivo Excel en {excel_file}")
        return

    if not os.path.exists(pdf_template):
        print(f"❌ Error: No se encontró la plantilla PDF en {pdf_template}")
        return

    # Test email configuration
    if not test_email_configuration():
        print(
            "⚠️  Configuración de email no válida. Los certificados se generarán pero no se enviarán emails."
        )

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    try:
        # Read Excel file
        print("📊 Leyendo datos del archivo Excel...")
        df = pd.read_excel(excel_file)
        print(f"✅ Datos leídos: {len(df)} registros encontrados")

        # Process each row
        for index, row in df.iterrows():
            try:
                # Extract data using correct column names
                name = row["nombre completo"]
                baptism_date = row["Fecha de bautizmo"]
                email = row["Email"]
                church_name = row.get(
                    "celula", "Iglesia Default"
                )  # Using 'celula' as church name

                print(f"\n👤 Procesando: {name}")

                # Skip if no baptism date
                if pd.isna(baptism_date):
                    print(f"📅 {name}: Sin fecha de bautismo, saltando...")
                    continue

                # Validate baptism date
                if not validate_baptism_date(baptism_date):
                    print(
                        f"📅 {name}: Fecha de bautismo futura ({baptism_date}), saltando..."
                    )
                    continue

                # Define output file path
                safe_name = "".join(
                    c for c in name if c.isalnum() or c in (" ", "-", "_")
                ).rstrip()
                certificate_filename = f"certificado_{safe_name}.pdf"
                certificate_path = os.path.join(output_path, certificate_filename)

                # Check if certificate already exists
                if os.path.exists(certificate_path):
                    print(f"📄 {name}: Certificado ya existe, saltando...")
                    continue

                # Generate certificate
                print(f"🖨️  Generando PDF para {name}...")
                if generate_certificate(
                    name, baptism_date, church_name, pdf_template, certificate_path
                ):
                    # Send email
                    print(f"📧 Enviando email a {email}...")
                    send_baptism_congratulations_email(email, name, certificate_path)
                else:
                    print(f"❌ Error generando certificado para {name}")

            except Exception as e:
                print(f"❌ Error procesando registro {index}: {e}")
                continue

        print("\n✅ Proceso completado!")

    except Exception as e:
        print(f"❌ Error leyendo archivo Excel: {e}")


def process_baptism_certificates_from_db():
    """Process baptism certificates from SQLite database"""
    print("🎯 Procesando certificados desde base de datos SQLite...")

    # Get paths
    output_path = get_output_path()
    pdf_template = os.path.join("data", "template.pdf")

    # Check if template exists
    if not os.path.exists(pdf_template):
        print(f"❌ Error: No se encontró la plantilla PDF en {pdf_template}")
        return

    # Test email configuration
    if not test_email_configuration():
        print(
            "⚠️  Configuración de email no válida. Los certificados se generarán pero no se enviarán emails."
        )

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Initialize database
    db = DatabaseService()
    bautismos_pendientes = db.obtener_bautismos_pendientes()

    if not bautismos_pendientes:
        print("✅ No hay certificados pendientes de generar")
        return

    print(f"📊 Procesando {len(bautismos_pendientes)} certificados pendientes...")

    # Process each baptism
    for bautismo in bautismos_pendientes:
        try:
            name = bautismo["nombre_completo"]
            baptism_date = bautismo["fecha_bautismo"]
            email = bautismo["email"]
            church_name = bautismo.get("iglesia", "Iglesia Default")

            print(f"\n👤 Procesando: {name}")

            # Validate baptism date
            if not validate_baptism_date(baptism_date):
                print(
                    f"📅 {name}: Fecha de bautismo futura ({baptism_date}), saltando..."
                )
                continue

            # Define output file path
            safe_name = "".join(
                c for c in name if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            certificate_filename = f"certificado_{safe_name}.pdf"
            certificate_path = os.path.join(output_path, certificate_filename)

            # Check if certificate already exists
            if os.path.exists(certificate_path):
                print(f"📄 {name}: Certificado ya existe, saltando...")
                continue

            # Generate certificate
            print(f"🖨️  Generando PDF para {name}...")
            if generate_certificate(
                name, baptism_date, church_name, pdf_template, certificate_path
            ):
                # Mark certificate as generated
                db.marcar_certificado_generado(bautismo["id"])

                # Send email
                print(f"📧 Enviando email a {email}...")
                if send_baptism_congratulations_email(email, name, certificate_path):
                    db.marcar_email_enviado(bautismo["id"])
                    print(f"✅ Email enviado exitosamente a {email}")
                else:
                    print(f"❌ Error enviando email a {email}")
            else:
                print(f"❌ Error generando certificado para {name}")

        except Exception as e:
            print(f"❌ Error procesando bautismo {bautismo.get('id', 'N/A')}: {e}")
            continue

    print("\n✅ Proceso completado!")


def run_cli():
    """Run the command line interface"""
    print("📋 Modo Línea de Comandos")
    print("=" * 40)

    # Check if we should use database or Excel
    if os.path.exists("bautismos.db"):
        print("🗄️  Base de datos SQLite detectada")
        print("💡 Para usar la interfaz gráfica, ejecuta: python main.py --gui")
        print()

        # Initialize database
        db = DatabaseService()
        stats = db.obtener_estadisticas()

        print(f"📊 Estadísticas actuales:")
        print(f"   Total registros: {stats['total']}")
        print(f"   Pendientes: {stats['pendientes']}")
        print(f"   Completados: {stats['completados']}")
        print(f"   Emails enviados: {stats['emails_enviados']}")
        print()

        # Process pending certificates
        if stats["pendientes"] > 0:
            print(f"🔄 Procesando {stats['pendientes']} certificados pendientes...")
            process_baptism_certificates_from_db()
        else:
            print("✅ No hay certificados pendientes")

    else:
        print("📊 Modo Excel detectado")
        print("💡 Procesando archivo Excel...")
        process_baptism_certificates()


if __name__ == "__main__":
    run_cli()
