#!/usr/bin/env python3
"""
Script para verificar qué fuentes están configuradas en los campos de formulario del PDF.
"""

import fitz  # PyMuPDF
import os


def check_pdf_fonts():
    template_path = "data/template.pdf"

    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return

    print("🔍 VERIFICANDO FUENTES DEL PDF")
    print("=" * 50)

    try:
        doc = fitz.open(template_path)

        for page_num, page in enumerate(doc):
            print(f"\n📄 PÁGINA {page_num + 1}:")
            print("-" * 30)

            # Check form fields
            if page.widgets():
                print("📋 Campos de formulario encontrados:")
                for widget in page.widgets():
                    field_name = widget.field_name
                    field_type = widget.field_type
                    field_value = widget.field_value

                    print(f"  Campo: '{field_name}'")
                    print(f"    Tipo: {field_type}")
                    print(f"    Valor actual: '{field_value}'")

                    # Try to get font properties
                    try:
                        # Get the annotation object
                        annot = widget._annot
                        if hasattr(annot, "get_text"):
                            text_info = annot.get_text()
                            print(f"    Propiedades de texto: {text_info}")
                    except:
                        print(f"    No se pudieron obtener propiedades de fuente")

                    print()
            else:
                print("⚠️  No se encontraron campos de formulario")

            # Check all text with font properties
            print("📝 Todo el texto con propiedades de fuente:")
            text_blocks = page.get_text("dict")

            for block in text_blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                print(f"  Texto: '{text}'")
                                print(f"    Fuente: {span['font']}")
                                print(f"    Tamaño: {span['size']}")
                                print(f"    Color: {span['color']}")
                                print(
                                    f"    Posición: x={span['bbox'][0]:.1f}, y={span['bbox'][1]:.1f}"
                                )
                                print()

        doc.close()

    except Exception as e:
        print(f"❌ Error analizando PDF: {e}")
        import traceback

        print(f"Error completo: {traceback.format_exc()}")


if __name__ == "__main__":
    check_pdf_fonts()
