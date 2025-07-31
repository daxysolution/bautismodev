import os
import sys
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject

# Try to import PyMuPDF for better text replacement
try:
    import fitz  # PyMuPDF

    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print(
        "⚠️  PyMuPDF no disponible. Instalando funcionalidad básica de reemplazo de texto."
    )


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def format_date(date_str):
    """Convert date from DD/MM/AAAA format to 'día de mes de año' format"""
    try:
        # Parse the date
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")

        # Spanish month names
        months = {
            1: "enero",
            2: "febrero",
            3: "marzo",
            4: "abril",
            5: "mayo",
            6: "junio",
            7: "julio",
            8: "agosto",
            9: "septiembre",
            10: "octubre",
            11: "noviembre",
            12: "diciembre",
        }

        day = date_obj.day
        month = months[date_obj.month]
        year = date_obj.year

        return f"{day} de {month} de {year}"
    except Exception as e:
        print(f"Error formatting date {date_str}: {e}")
        return date_str


def get_pdf_form_fields(template_path):
    """
    Get all form fields from a PDF template.

    :param template_path: Path to the PDF template
    :return: Dictionary with field names and their types
    """
    try:
        reader = PdfReader(template_path)
        fields = {}

        for page_num, page in enumerate(reader.pages):
            if "/Annots" in page:
                for field in page["/Annots"]:
                    field_object = field.get_object()
                    field_name = field_object.get("/T")
                    field_type = field_object.get("/FT")

                    if field_name:
                        fields[field_name] = {"type": field_type, "page": page_num + 1}

        return fields
    except Exception as e:
        print(f"❌ Error obteniendo campos del formulario: {e}")
        return {}


def fill_pdf_template(template_path, output_path, data):
    """
    Fill a PDF template with data using form fields.

    :param template_path: Path to the PDF template
    :param output_path: Path to save the filled PDF
    :param data: Dictionary containing data to fill in the PDF
    """
    try:
        # Read the template PDF
        reader = PdfReader(template_path)
        writer = PdfWriter()

        # Get form fields for debugging
        fields = get_pdf_form_fields(template_path)
        if fields:
            print(f"📋 Campos encontrados en el formulario: {list(fields.keys())}")
        else:
            print("⚠️  No se encontraron campos de formulario en el PDF")

        # Track filled fields
        filled_fields = 0

        # Iterate over all pages
        for page in reader.pages:
            # Update the fields with data
            if "/Annots" in page:
                for field in page["/Annots"]:
                    field_object = field.get_object()
                    field_name = field_object.get("/T")

                    if field_name in data:
                        # Set the field value
                        field_object.update(
                            {NameObject("/V"): TextStringObject(str(data[field_name]))}
                        )
                        print(
                            f"✅ Campo '{field_name}' rellenado con: {data[field_name]}"
                        )
                        filled_fields += 1
                    elif field_name:
                        print(
                            f"⚠️  Campo '{field_name}' no tiene datos correspondientes"
                        )

            writer.add_page(page)

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Write the filled PDF to a new file
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        if filled_fields > 0:
            print(
                f"✅ PDF generado con {filled_fields} campos rellenados: {output_path}"
            )
            return True
        else:
            print("⚠️  No se rellenaron campos de formulario")
            return False

    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        import traceback

        print(f"Error completo: {traceback.format_exc()}")
        return False


def improved_text_replacement(
    template_path, output_path, name, formatted_date, church_name
):
    """
    Improved text replacement that preserves original font properties.
    """
    if not PYMUPDF_AVAILABLE:
        print("❌ PyMuPDF no disponible para reemplazo de texto mejorado")
        return False

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

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

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


def create_form_template(template_path):
    """
    Create a PDF template with form fields for baptism certificate.

    :param template_path: Path to save the template
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfbase

        # Create the PDF
        c = canvas.Canvas(template_path, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 1 * inch, "CERTIFICADO DE BAUTISMO")

        # Decorative line
        c.line(1 * inch, height - 1.3 * inch, width - 1 * inch, height - 1.3 * inch)

        # Certificate text
        c.setFont("Helvetica", 12)
        y_position = height - 2.5 * inch

        # Main text with form fields
        text_lines = [
            "Por medio del presente se certifica que:",
            "",
            "_____ fue bautizado/a el ___de ___ de___ en el nombre del Padre,",
            "del Hijo y del Espíritu Santo, según el mandamiento de nuestro",
            "Señor Jesucristo.",
            "",
            "Este certificado es un testimonio de su compromiso con Cristo",
            "y su nueva vida en la fe cristiana.",
            "",
            "Que Dios bendiga su caminar en esta nueva etapa de su vida espiritual.",
        ]

        for line in text_lines:
            if line.strip():
                c.drawString(1 * inch, y_position, line.strip())
                y_position -= 0.4 * inch
            else:
                y_position -= 0.2 * inch

        # Signature space
        y_position -= 0.5 * inch
        c.line(1 * inch, y_position, 3 * inch, y_position)
        c.drawString(1 * inch, y_position - 0.3 * inch, "Firma del Pastor")

        # Date
        c.drawString(
            width - 3 * inch, y_position - 0.3 * inch, "Fecha: _______________"
        )

        # Save the PDF
        c.save()
        print(f"✅ Template simple creado: {template_path}")
        return True

    except Exception as e:
        print(f"❌ Error creando template: {e}")
        return False


def fill_pdf_with_text_replacement(
    template_path, output_path, name, formatted_date, church_name
):
    """
    Fill PDF template by replacing text patterns with custom font sizes.

    :param template_path: Path to the PDF template
    :param output_path: Path to save the filled PDF
    :param name: Full name of the person
    :param formatted_date: Formatted date string
    :param church_name: Name of the church
    """
    if not PYMUPDF_AVAILABLE:
        print("❌ PyMuPDF no disponible para reemplazo de texto")
        return False

    try:
        # Check if template exists and has the right patterns
        if not os.path.exists(template_path):
            print("📝 Template no encontrado, creando uno nuevo...")
            if not create_form_template(template_path):
                return False

        # Open the PDF
        doc = fitz.open(template_path)

        # Define replacements with their font sizes and positions
        replacements = {
            # Specific text patterns found in the template with exact positioning
            "Certifico que:": (f"Certifico que: {name}", 40, "center"),
            "En la iglesia:": (f"En la iglesia: {church_name}", 40, "center"),
            "El día:": (f"El día: {formatted_date}", 40, "center"),
        }

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Process each page
        for page in doc:
            total_replacements = 0

            for key, (replacement_text, fontsize, alignment) in replacements.items():
                # Find all instances of the pattern
                instances = page.search_for(key)

                if instances:
                    print(
                        f"✅ Encontrado patrón '{key}' - {len(instances)} instancia(s)"
                    )

                # Replace text by first removing original, then inserting new
                for inst in instances:
                    # Get the original text rectangle
                    rect = fitz.Rect(inst.x0, inst.y0, inst.x1, inst.y1)

                    # First, redact (remove) the original text completely
                    page.add_redact_annot(rect, fill=(1, 1, 1))  # White background

                    # Apply redaction to remove original text
                    page.apply_redactions()

                    # Calculate position for new text
                    if alignment == "center":
                        center_x = (inst.x0 + inst.x1) / 2
                        center_y = (inst.y0 + inst.y1) / 2
                    else:
                        center_x = inst.x0
                        center_y = inst.y0

                    # Insert the new text with proper formatting
                    page.insert_text(
                        (center_x, center_y),
                        replacement_text,
                        fontsize=fontsize,
                        fontname="helv",
                        color=(0, 0, 0),  # Black color
                    )
                    total_replacements += 1

            if total_replacements == 0:
                print("⚠️  No se encontraron patrones para reemplazar en esta página")
            else:
                print(f"✅ Total de reemplazos realizados: {total_replacements}")

        # Save the modified PDF
        try:
            doc.save(output_path)
            doc.close()

            # Verify the file was created and has content
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ PDF generado con reemplazo de texto: {output_path}")
                return True
            else:
                print(f"❌ El archivo PDF no se creó correctamente: {output_path}")
                return False

        except Exception as save_error:
            print(f"❌ Error guardando PDF: {save_error}")
            return False

    except Exception as e:
        print(f"❌ Error en reemplazo de texto: {e}")
        import traceback

        print(f"Error completo: {traceback.format_exc()}")
        return False


def generate_certificate(name, baptism_date, church_name, template_path, output_path):
    """
    Generate a baptism certificate PDF.

    :param name: Full name of the person
    :param baptism_date: Baptism date in DD/MM/YYYY format
    :param church_name: Name of the church
    :param template_path: Path to the PDF template
    :param output_path: Path to save the generated certificate
    """
    # Format the date
    formatted_date = format_date(baptism_date)

    # Use the correct template path
    correct_template_path = os.path.join("data", "template.pdf")

    # Check if correct template exists
    if os.path.exists(correct_template_path):
        template_path = correct_template_path
        print(f"✅ Usando template correcto: {template_path}")
    else:
        print(f"⚠️  Template correcto no encontrado, usando: {template_path}")

    # Try to load field mapping
    field_mapping = None
    mapping_path = os.path.join("data", "field_mapping.json")
    if os.path.exists(mapping_path):
        try:
            import json

            with open(mapping_path, "r", encoding="utf-8") as f:
                field_mapping = json.load(f)
            print("✅ Cargando mapeo de campos configurado")
        except Exception as e:
            print(f"⚠️  Error cargando mapeo: {e}")

    # Prepare data for the PDF
    if field_mapping:
        # Use configured mapping
        data = {}
        for standard_field, mapped_field in field_mapping.items():
            if mapped_field:
                if standard_field == "NOMBRE_COMPLETO":
                    data[mapped_field] = name
                elif standard_field == "FECHA_BAUTISMO":
                    data[mapped_field] = formatted_date
                elif standard_field == "NOMBRE_IGLESIA":
                    data[mapped_field] = church_name
        print(f"📋 Usando mapeo de campos: {list(data.keys())}")
    else:
        # Use default field name variations
        data = {
            "NOMBRE_COMPLETO": name,
            "NOMBRE": name,
            "NOMBRE_PERSONA": name,
            "FECHA_BAUTISMO": formatted_date,
            "FECHA": formatted_date,
            "FECHA_CEREMONIA": formatted_date,
            "NOMBRE_IGLESIA": church_name,
            "IGLESIA": church_name,
            "NOMBRE_TEMPLO": church_name,
            "TEMPLO": church_name,
            "PARROQUIA": church_name,
            "CONGREGACION": church_name,
        }
        print("📋 Usando nombres de campos por defecto")

    # Add additional variations for church name field
    church_field_variations = [
        "NOMBRE_IGLESIA",
        "IGLESIA",
        "NOMBRE_TEMPLO",
        "TEMPLO",
        "PARROQUIA",
        "CONGREGACION",
        "IGLESIA_NOMBRE",
        "NOMBRE_PARROQUIA",
    ]

    # If we have a mapping but the church field might not be found, add variations
    if field_mapping and "NOMBRE_IGLESIA" in field_mapping:
        mapped_church_field = field_mapping["NOMBRE_IGLESIA"]
        # Add the mapped field and common variations
        for variation in church_field_variations:
            if variation not in data:
                data[variation] = church_name
        print(f"🔄 Agregando variaciones del campo iglesia: {church_field_variations}")

        # First try form field method (more reliable)
    print("🔄 Usando método de campos de formulario...")
    if fill_pdf_template(template_path, output_path, data):
        return True

    # Fallback to improved text replacement method if form fields fail
    if PYMUPDF_AVAILABLE:
        print(
            "⚠️  Campos de formulario fallaron, intentando reemplazo de texto mejorado..."
        )
        if improved_text_replacement(
            template_path, output_path, name, formatted_date, church_name
        ):
            return True

        # If improved method fails, try original text replacement
        print("⚠️  Reemplazo mejorado falló, intentando método original...")
        if fill_pdf_with_text_replacement(
            template_path, output_path, name, formatted_date, church_name
        ):
            return True

    return False


def analyze_template(template_path):
    """
    Analyze a PDF template to show its structure and available fields.

    :param template_path: Path to the PDF template
    """
    try:
        if not os.path.exists(template_path):
            print(f"❌ Template no encontrado: {template_path}")
            return

        print(f"🔍 Analizando template: {template_path}")

        # Get form fields
        fields = get_pdf_form_fields(template_path)

        if fields:
            print("📋 Campos de formulario encontrados:")
            for field_name, field_info in fields.items():
                print(
                    f"  - {field_name} (tipo: {field_info['type']}, página: {field_info['page']})"
                )

            # Check for church-related fields specifically
            church_fields = [
                name
                for name in fields.keys()
                if any(
                    keyword in name.upper()
                    for keyword in ["IGLESIA", "TEMPLO", "PARROQUIA", "CONGREGACION"]
                )
            ]
            if church_fields:
                print(
                    f"🏛️  Campos relacionados con iglesia encontrados: {church_fields}"
                )
            else:
                print("⚠️  No se encontraron campos específicos de iglesia")
        else:
            print("⚠️  No se encontraron campos de formulario")

        # Check for text patterns if PyMuPDF is available
        if PYMUPDF_AVAILABLE:
            try:
                doc = fitz.open(template_path)
                text_content = ""
                for page in doc:
                    text_content += page.get_text()

                # Look for common patterns
                patterns = [
                    "[NOMBRE",
                    "[FECHA",
                    "[IGLESIA",
                    "NOMBRE_COMPLETO",
                    "FECHA_BAUTISMO",
                ]
                found_patterns = []
                for pattern in patterns:
                    if pattern.lower() in text_content.lower():
                        found_patterns.append(pattern)

                if found_patterns:
                    print("📝 Patrones de texto encontrados:")
                    for pattern in found_patterns:
                        print(f"  - {pattern}")
                else:
                    print("⚠️  No se encontraron patrones de texto comunes")

                doc.close()
            except Exception as e:
                print(f"⚠️  Error analizando texto: {e}")

    except Exception as e:
        print(f"❌ Error analizando template: {e}")
