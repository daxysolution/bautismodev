#!/usr/bin/env python3
"""
Script para analizar el template PDF y mostrar todos los campos de formulario disponibles.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.pdf_service import analyze_template


def main():
    template_path = "data/template.pdf"

    print("🔍 ANALIZANDO TEMPLATE PDF")
    print("=" * 50)

    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado en: {template_path}")
        return

    analyze_template(template_path)

    print("\n" + "=" * 50)
    print("💡 CONSEJOS:")
    print("1. Busca en la lista de arriba el campo relacionado con la iglesia")
    print("2. Copia el nombre exacto del campo")
    print("3. Actualiza el archivo data/field_mapping.json con el nombre correcto")
    print("4. Ejemplo: si el campo se llama 'IGLESIA_NOMBRE', cambia:")
    print('   "NOMBRE_IGLESIA": "NOMBRE_IGLESIA"')
    print("   por:")
    print('   "NOMBRE_IGLESIA": "IGLESIA_NOMBRE"')


if __name__ == "__main__":
    main()
