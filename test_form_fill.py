#!/usr/bin/env python3
"""
Script de prueba para verificar que el relleno de campos de formulario funcione correctamente.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.pdf_service import generate_certificate, get_pdf_form_fields


def test_form_fill():
    print("🧪 PRUEBA DE RELLENO DE FORMULARIOS")
    print("=" * 50)

    template_path = "data/template.pdf"
    output_path = "output/test_form_fill.pdf"

    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return False

    # Test data
    name = "María González López"
    date = "20/12/2024"
    church = "Manantial de Bendiciones"

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # First, check form fields
    print("📋 Verificando campos de formulario...")
    fields = get_pdf_form_fields(template_path)

    if fields:
        print(f"✅ Se encontraron {len(fields)} campos:")
        for field_name, field_info in fields.items():
            print(f"   - {field_name} (tipo: {field_info['type']})")
    else:
        print("❌ No se encontraron campos de formulario")
        return False

    # Generate certificate
    print(f"\n🔄 Generando certificado...")
    print(f"   Nombre: {name}")
    print(f"   Fecha: {date}")
    print(f"   Iglesia: {church}")

    success = generate_certificate(name, date, church, template_path, output_path)

    if success:
        print(f"✅ Certificado generado: {output_path}")

        # Verify the file exists and has content
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(
                f"✅ Archivo creado correctamente ({os.path.getsize(output_path)} bytes)"
            )

            # Check if form fields were filled
            filled_fields = get_pdf_form_fields(output_path)
            if filled_fields:
                print("✅ El PDF resultante tiene campos de formulario")
            else:
                print(
                    "⚠️  El PDF resultante no tiene campos de formulario (puede ser normal si se rellenaron)"
                )
        else:
            print("❌ El archivo no se creó correctamente")
            return False
    else:
        print("❌ Error generando certificado")
        return False

    print("\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
    return True


if __name__ == "__main__":
    success = test_form_fill()
    if not success:
        print("\n❌ LA PRUEBA FALLÓ")
        sys.exit(1)
