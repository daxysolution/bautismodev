import fitz  # PyMuPDF
import os


def analyze_pdf_content():
    template_path = "data/template.pdf"

    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return

    print("🔍 ANALIZANDO CONTENIDO DEL PDF")
    print("=" * 50)

    try:
        doc = fitz.open(template_path)

        for page_num, page in enumerate(doc):
            print(f"\n📄 PÁGINA {page_num + 1}:")
            print("-" * 30)

            # Get all text blocks
            text_blocks = page.get_text("dict")

            for block in text_blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                print(f"Texto: '{text}'")
                                print(
                                    f"  Posición: x={span['bbox'][0]:.1f}, y={span['bbox'][1]:.1f}"
                                )
                                print(f"  Fuente: {span['font']}")
                                print(f"  Tamaño: {span['size']:.1f}")
                                print()

        doc.close()

    except Exception as e:
        print(f"❌ Error analizando PDF: {e}")


if __name__ == "__main__":
    analyze_pdf_content()
