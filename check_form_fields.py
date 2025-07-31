#!/usr/bin/env python3
"""
Script para verificar qué campos de formulario tiene el template PDF.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.pdf_service import get_pdf_form_fields


def main():
    template_path = "data/template.pdf"

    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return

    print("🔍 VERIFICANDO CAMPOS DE FORMULARIO")
    print("=" * 50)

    fields = get_pdf_form_fields(template_path)

    if fields:
        print(f"✅ Se encontraron {len(fields)} campos de formulario:")
        print()
        for field_name, field_info in fields.items():
            print(f"📋 Campo: '{field_name}'")
            print(f"   Tipo: {field_info['type']}")
            print(f"   Página: {field_info['page']}")
            print()

        # Check for specific field types
        text_fields = [name for name, info in fields.items() if info["type"] == "/Tx"]
        if text_fields:
            print(f"📝 Campos de texto ({len(text_fields)}): {text_fields}")

        # Suggest field mapping
        print("\n💡 SUGERENCIA DE MAPEO:")
        print("Actualiza el archivo data/field_mapping.json con los nombres exactos:")
        print("{")
        print('    "NOMBRE_COMPLETO": "NOMBRE_EXACTO_DEL_CAMPO",')
        print('    "FECHA_BAUTISMO": "FECHA_EXACTA_DEL_CAMPO",')
        print('    "NOMBRE_IGLESIA": "IGLESIA_EXACTA_DEL_CAMPO"')
        print("}")

    else:
        print("❌ No se encontraron campos de formulario")
        print(
            "💡 El PDF no tiene campos de formulario, necesitarás usar reemplazo de texto"
        )


if __name__ == "__main__":
    main()
