#!/usr/bin/env python3
"""
Función mejorada para reemplazo de texto que preserva las propiedades originales del texto.
"""

import fitz  # PyMuPDF
import os


def improved_text_replacement(
    template_path, output_path, name, formatted_date, church_name
):
    """
    Improved text replacement that preserves original font properties.
    """
    try:
        # Open the PDF
        doc = fitz.open(template_path)

        # Define the text to replace and their new values
        replacements = {
            "Certifico que:": f"Certifico que: {name}",
            "En la iglesia:": f"En la iglesia: {church_name}",
            "El día:": f"El día: {formatted_date}",
        }

        # Process each page
        for page in doc:
            # Get all text blocks with their properties
            text_blocks = page.get_text("dict")

            for block in text_blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            original_text = span["text"].strip()

                            # Check if this text needs to be replaced
                            for pattern, replacement in replacements.items():
                                if pattern in original_text:
                                    print(
                                        f"✅ Reemplazando: '{original_text}' -> '{replacement}'"
                                    )

                                    # Get original font properties
                                    font_name = span["font"]
                                    font_size = span["size"]
                                    font_color = span["color"]

                                    # Get the rectangle of this text
                                    rect = fitz.Rect(span["bbox"])

                                    # Remove the original text
                                    page.add_redact_annot(rect, fill=(1, 1, 1))
                                    page.apply_redactions()

                                    # Insert new text with original properties
                                    center_x = (rect.x0 + rect.x1) / 2
                                    center_y = (rect.y0 + rect.y1) / 2

                                    # Try to use original font, fallback to helv
                                    try:
                                        page.insert_text(
                                            (center_x, center_y),
                                            replacement,
                                            fontsize=font_size,
                                            fontname=font_name,
                                            color=font_color,
                                        )
                                    except:
                                        # Fallback to default font
                                        page.insert_text(
                                            (center_x, center_y),
                                            replacement,
                                            fontsize=font_size,
                                            fontname="helv",
                                            color=(0, 0, 0),
                                        )

        # Save the modified PDF
        doc.save(output_path)
        doc.close()

        print(f"✅ PDF mejorado generado: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Error en reemplazo mejorado: {e}")
        import traceback

        print(f"Error completo: {traceback.format_exc()}")
        return False


def test_improved_replacement():
    """Test the improved text replacement"""
    template_path = "data/template.pdf"
    output_path = "output/test_improved.pdf"

    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return False

    # Test data
    name = "Juan Carlos Pérez González"
    date = "15/12/2024"
    church = "Manantial de Bendiciones"

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    return improved_text_replacement(template_path, output_path, name, date, church)


if __name__ == "__main__":
    test_improved_replacement()
