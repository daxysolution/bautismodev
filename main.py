#!/usr/bin/env python3
"""
Certificador de Bautismos - Aplicación Principal

Esta aplicación automatiza la generación de certificados de bautismo
y el envío de emails con certificados adjuntos.

Autor: Certificador de Bautismos
Versión: 1.0
"""

import sys
import os


def main():
    """Main entry point for the application"""
    print("🎯 Certificador de Bautismos v1.0")
    print("=" * 40)

    # Check if GUI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        # Run GUI version
        try:
            from gui_app import BautismoApp

            app = BautismoApp()
            app.run()
        except ImportError as e:
            print(f"❌ Error: No se pudo cargar la interfaz gráfica: {e}")
            print("💡 Asegúrate de tener tkinter instalado")
            return 1
    else:
        # Run command line version
        try:
            from cli_app import run_cli

            run_cli()
        except ImportError as e:
            print(f"❌ Error: No se pudo cargar la versión CLI: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
