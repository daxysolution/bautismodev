#!/usr/bin/env python3
"""
Ventana de edición para bautismos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from services.pdf_service import generate_certificate


class EditBautismoWindow:
    def __init__(self, parent, bautismo_data, db_service):
        """
        Initialize edit window

        :param parent: Parent window
        :param bautismo_data: Baptism data to edit
        :param db_service: Database service instance
        """
        self.parent = parent
        self.bautismo_data = bautismo_data
        self.db = db_service

        # Create new window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Editar Bautismo - {bautismo_data['nombre_completo']}")
        self.window.geometry("500x600")
        self.window.resizable(False, False)

        # Center window
        self.window.transient(parent)
        self.window.grab_set()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        """Create the widgets for the edit window"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(
            main_frame, text="Editar Datos del Bautismo", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Form fields
        row = 1

        # Nombre completo
        ttk.Label(main_frame, text="Nombre Completo:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.nombre_var = tk.StringVar()
        self.nombre_entry = ttk.Entry(
            main_frame, textvariable=self.nombre_var, width=40
        )
        self.nombre_entry.grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )
        row += 1

        # Email
        ttk.Label(main_frame, text="Email:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(main_frame, textvariable=self.email_var, width=40)
        self.email_entry.grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )
        row += 1

        # Fecha de bautismo
        ttk.Label(main_frame, text="Fecha de Bautismo (DD/MM/AAAA):").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.fecha_var = tk.StringVar()
        self.fecha_entry = ttk.Entry(main_frame, textvariable=self.fecha_var, width=40)
        self.fecha_entry.grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )
        row += 1

        # Iglesia
        ttk.Label(main_frame, text="Iglesia:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.iglesia_var = tk.StringVar()
        self.iglesia_entry = ttk.Entry(
            main_frame, textvariable=self.iglesia_var, width=40
        )
        self.iglesia_entry.grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )
        row += 1

        # Célula
        ttk.Label(main_frame, text="Célula:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.celula_var = tk.StringVar()
        self.celula_entry = ttk.Entry(
            main_frame, textvariable=self.celula_var, width=40
        )
        self.celula_entry.grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )
        row += 1

        # Líder
        ttk.Label(main_frame, text="Líder:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.lider_var = tk.StringVar()
        self.lider_entry = ttk.Entry(main_frame, textvariable=self.lider_var, width=40)
        self.lider_entry.grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )
        row += 1

        # Status info
        status_frame = ttk.LabelFrame(
            main_frame, text="Estado del Certificado", padding="10"
        )
        status_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        row += 1

        self.certificado_status = tk.StringVar()
        self.email_status = tk.StringVar()

        ttk.Label(status_frame, textvariable=self.certificado_status).grid(
            row=0, column=0, sticky=tk.W
        )
        ttk.Label(status_frame, textvariable=self.email_status).grid(
            row=1, column=0, sticky=tk.W
        )

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)

        # Save button
        self.save_btn = ttk.Button(
            buttons_frame, text="💾 Guardar Cambios", command=self.guardar_cambios
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # Regenerate certificate button
        self.regenerate_btn = ttk.Button(
            buttons_frame,
            text="🔄 Regenerar Certificado",
            command=self.regenerar_certificado,
        )
        self.regenerate_btn.pack(side=tk.LEFT, padx=5)

        # Send email button
        self.send_email_btn = ttk.Button(
            buttons_frame, text="📧 Reenviar Email", command=self.reenviar_email
        )
        self.send_email_btn.pack(side=tk.LEFT, padx=5)

        # Cancel button
        self.cancel_btn = ttk.Button(
            buttons_frame, text="❌ Cancelar", command=self.window.destroy
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

    def load_data(self):
        """Load baptism data into the form"""
        self.nombre_var.set(self.bautismo_data.get("nombre_completo", ""))
        self.email_var.set(self.bautismo_data.get("email", ""))
        self.fecha_var.set(self.bautismo_data.get("fecha_bautismo", ""))
        self.iglesia_var.set(self.bautismo_data.get("iglesia", ""))
        self.celula_var.set(self.bautismo_data.get("celula", ""))
        self.lider_var.set(self.bautismo_data.get("lider", ""))

        # Update status
        certificado_generado = self.bautismo_data.get("certificado_generado", 0)
        email_enviado = self.bautismo_data.get("email_enviado", 0)

        if certificado_generado:
            self.certificado_status.set("✅ Certificado: Generado")
        else:
            self.certificado_status.set("⏳ Certificado: Pendiente")

        if email_enviado:
            self.email_status.set("✅ Email: Enviado")
        else:
            self.email_status.set("⏳ Email: Pendiente")

    def validar_datos(self):
        """Validate form data"""
        nombre = self.nombre_var.get().strip()
        email = self.email_var.get().strip()
        fecha = self.fecha_var.get().strip()

        if not nombre:
            messagebox.showerror("Error", "El nombre completo es obligatorio")
            return False

        if not email:
            messagebox.showerror("Error", "El email es obligatorio")
            return False

        if not fecha:
            messagebox.showerror("Error", "La fecha de bautismo es obligatoria")
            return False

        # Validate date format
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe estar en formato DD/MM/AAAA")
            return False

        return True

    def guardar_cambios(self):
        """Save changes to database"""
        if not self.validar_datos():
            return

        try:
            success = self.db.actualizar_bautismo(
                self.bautismo_data["id"],
                self.nombre_var.get().strip(),
                self.email_var.get().strip(),
                self.fecha_var.get().strip(),
                self.iglesia_var.get().strip(),
                self.celula_var.get().strip(),
                self.lider_var.get().strip(),
            )

            if success:
                messagebox.showinfo("Éxito", "Datos actualizados correctamente")
                # Update local data
                self.bautismo_data.update(
                    {
                        "nombre_completo": self.nombre_var.get().strip(),
                        "email": self.email_var.get().strip(),
                        "fecha_bautismo": self.fecha_var.get().strip(),
                        "iglesia": self.iglesia_var.get().strip(),
                        "celula": self.celula_var.get().strip(),
                        "lider": self.lider_var.get().strip(),
                    }
                )
                # Refresh parent window
                if hasattr(self.parent, "load_bautismos"):
                    self.parent.load_bautismos()
            else:
                messagebox.showerror("Error", "No se pudieron actualizar los datos")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def regenerar_certificado(self):
        """Regenerate certificate"""
        if not self.validar_datos():
            return

        try:
            # Mark certificate as not generated
            self.db.regenerar_certificado(self.bautismo_data["id"])

            # Generate new certificate
            template_path = "data/template.pdf"
            if not os.path.exists(template_path):
                messagebox.showerror(
                    "Error", f"No se encontró la plantilla: {template_path}"
                )
                return

            # Create output directory
            os.makedirs("output", exist_ok=True)

            # Generate certificate with unique filename to avoid conflicts
            safe_name = "".join(
                c
                for c in self.nombre_var.get().strip()
                if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()

            # Add timestamp to avoid conflicts
            import time

            timestamp = int(time.time())
            output_path = f"output/certificado_{safe_name}_{timestamp}.pdf"

            # Remove old certificate if it exists
            old_certificate_path = f"output/certificado_{safe_name}.pdf"
            if os.path.exists(old_certificate_path):
                try:
                    os.remove(old_certificate_path)
                    print(f"✅ Archivo anterior eliminado: {old_certificate_path}")
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar archivo anterior: {e}")

            # Generate new certificate
            print(f"🔄 Generando certificado para: {self.nombre_var.get().strip()}")
            success = generate_certificate(
                self.nombre_var.get().strip(),
                self.fecha_var.get().strip(),
                self.iglesia_var.get().strip() or "Iglesia Default",
                template_path,
                output_path,
            )

            if success:
                # Rename to standard filename
                final_path = f"output/certificado_{safe_name}.pdf"
                try:
                    if os.path.exists(final_path):
                        os.remove(final_path)
                    os.rename(output_path, final_path)
                    output_path = final_path
                    print(f"✅ Archivo renombrado a: {final_path}")
                except Exception as e:
                    print(f"⚠️  No se pudo renombrar archivo: {e}")
                    # Use the timestamped file if rename fails
                    output_path = f"output/certificado_{safe_name}_{timestamp}.pdf"

                # Verify the file was created successfully
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    self.db.marcar_certificado_generado(self.bautismo_data["id"])
                    messagebox.showinfo(
                        "Éxito", f"Certificado regenerado exitosamente:\n{output_path}"
                    )
                    self.load_data()  # Refresh status
                    if hasattr(self.parent, "load_bautismos"):
                        self.parent.load_bautismos()
                else:
                    messagebox.showerror(
                        "Error",
                        "El certificado se generó pero el archivo está vacío o corrupto",
                    )
            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo regenerar el certificado. Revisa la consola para más detalles.",
                )

        except Exception as e:
            messagebox.showerror("Error", f"Error al regenerar certificado: {e}")
            import traceback

            print(f"Error completo: {traceback.format_exc()}")

    def reenviar_email(self):
        """Resend email"""
        if not self.validar_datos():
            return

        try:
            from services.mail_service import send_baptism_congratulations_email

            # Check if certificate exists
            safe_name = "".join(
                c
                for c in self.nombre_var.get().strip()
                if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            certificate_path = f"output/certificado_{safe_name}.pdf"

            if not os.path.exists(certificate_path):
                messagebox.showerror(
                    "Error",
                    "No se encontró el certificado. Regenera el certificado primero.",
                )
                return

            # Send email
            if send_baptism_congratulations_email(
                self.email_var.get().strip(),
                self.nombre_var.get().strip(),
                certificate_path,
            ):
                self.db.marcar_email_enviado(self.bautismo_data["id"])
                messagebox.showinfo("Éxito", "Email reenviado correctamente")
                self.load_data()  # Refresh status
                if hasattr(self.parent, "load_bautismos"):
                    self.parent.load_bautismos()
            else:
                messagebox.showerror("Error", "No se pudo enviar el email")

        except Exception as e:
            messagebox.showerror("Error", f"Error al reenviar email: {e}")
