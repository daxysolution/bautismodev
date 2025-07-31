import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
import threading
from services.database_service import DatabaseService
from services.pdf_service import generate_certificate
from services.mail_service import (
    send_baptism_congratulations_email,
    test_email_configuration,
    test_email_connection,
)


def check_excel_dependencies():
    """Check if required packages for Excel export are installed"""
    try:
        import pandas
        import openpyxl

        return True, None
    except ImportError as e:
        return False, str(e)


class BautismoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Certificador de Bautismos")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Initialize database
        self.db = DatabaseService()

        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

        self.create_widgets()
        self.load_bautismos()
        self.update_stats()

    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="🎯 Certificador de Bautismos",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Form Frame
        form_frame = ttk.LabelFrame(
            self.main_frame, text="📝 Nuevo Bautismo", padding="10"
        )
        form_frame.grid(
            row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        # Form fields
        ttk.Label(form_frame, text="Nombre completo:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.nombre_var = tk.StringVar()
        self.nombre_entry = ttk.Entry(
            form_frame, textvariable=self.nombre_var, width=30
        )
        self.nombre_entry.grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
        )

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=30)
        self.email_entry.grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
        )

        ttk.Label(form_frame, text="Fecha de bautismo:").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.fecha_var = tk.StringVar()
        self.fecha_entry = ttk.Entry(form_frame, textvariable=self.fecha_var, width=30)
        self.fecha_entry.grid(
            row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
        )
        ttk.Label(form_frame, text="(DD/MM/AAAA)").grid(
            row=2, column=2, sticky=tk.W, padx=(5, 0), pady=2
        )

        ttk.Label(form_frame, text="Iglesia:").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.iglesia_var = tk.StringVar()
        self.iglesia_entry = ttk.Entry(
            form_frame, textvariable=self.iglesia_var, width=30
        )
        self.iglesia_entry.grid(
            row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
        )

        ttk.Label(form_frame, text="Célula:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.celula_var = tk.StringVar()
        self.celula_entry = ttk.Entry(
            form_frame, textvariable=self.celula_var, width=30
        )
        self.celula_entry.grid(
            row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
        )

        ttk.Label(form_frame, text="Líder:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.lider_var = tk.StringVar()
        self.lider_entry = ttk.Entry(form_frame, textvariable=self.lider_var, width=30)
        self.lider_entry.grid(
            row=5, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2
        )

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))

        ttk.Button(button_frame, text="💾 Guardar", command=self.guardar_bautismo).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(
            button_frame, text="🔄 Limpiar", command=self.limpiar_formulario
        ).pack(side=tk.LEFT, padx=5)

        # Stats Frame
        stats_frame = ttk.LabelFrame(
            self.main_frame, text="📊 Estadísticas", padding="10"
        )
        stats_frame.grid(row=1, column=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))

        self.stats_text = tk.Text(stats_frame, height=8, width=25, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.BOTH, expand=True)

        # Action Buttons
        action_frame = ttk.Frame(self.main_frame)
        action_frame.grid(
            row=2, column=3, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0)
        )

        ttk.Button(
            action_frame,
            text="🖨️ Generar Certificados",
            command=self.generar_certificados_threaded,
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            action_frame, text="📧 Enviar Emails", command=self.enviar_emails_threaded
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            action_frame, text="🔧 Probar Email", command=self.probar_email
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            action_frame, text="📊 Exportar a Excel", command=self.exportar_excel
        ).pack(fill=tk.X, pady=2)

        # Edit button
        ttk.Button(
            action_frame, text="✏️ Editar Seleccionado", command=self.editar_seleccionado
        ).pack(fill=tk.X, pady=2)

        # Progress bar
        self.progress_var = tk.StringVar(value="Listo")
        self.progress_label = ttk.Label(action_frame, textvariable=self.progress_var)
        self.progress_label.pack(fill=tk.X, pady=(5, 0))

        # Bautismos List
        list_frame = ttk.LabelFrame(
            self.main_frame, text="📋 Bautismos Registrados", padding="10"
        )
        list_frame.grid(
            row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )

        # Create Treeview
        columns = ("ID", "Nombre", "Email", "Fecha", "Iglesia", "Certificado", "Email")
        self.tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=10
        )

        # Define headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Fecha", text="Fecha Bautismo")
        self.tree.heading("Iglesia", text="Iglesia")
        self.tree.heading("Certificado", text="Certificado")
        self.tree.heading("Email", text="Email Enviado")

        # Define columns
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=150)
        self.tree.column("Email", width=150)
        self.tree.column("Fecha", width=100)
        self.tree.column("Iglesia", width=100)
        self.tree.column("Certificado", width=80)
        self.tree.column("Email", width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double click to edit
        self.tree.bind("<Double-1>", self.editar_bautismo)

    def guardar_bautismo(self):
        """Save new baptism record"""
        nombre = self.nombre_var.get().strip()
        email = self.email_var.get().strip()
        fecha = self.fecha_var.get().strip()
        iglesia = self.iglesia_var.get().strip()
        celula = self.celula_var.get().strip()
        lider = self.lider_var.get().strip()

        # Validation
        if not nombre or not email or not fecha:
            messagebox.showerror("Error", "Nombre, email y fecha son obligatorios")
            return

        # Validate date format
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Fecha debe estar en formato DD/MM/AAAA")
            return

        # Save to database
        if self.db.agregar_bautismo(nombre, email, fecha, iglesia, celula, lider):
            messagebox.showinfo("Éxito", "Bautismo registrado correctamente")
            self.limpiar_formulario()
            self.load_bautismos()
            self.update_stats()
        else:
            messagebox.showerror("Error", "Error al guardar el bautismo")

    def limpiar_formulario(self):
        """Clear form fields"""
        self.nombre_var.set("")
        self.email_var.set("")
        self.fecha_var.set("")
        self.iglesia_var.set("")
        self.celula_var.set("")
        self.lider_var.set("")
        self.nombre_entry.focus()

    def load_bautismos(self):
        """Load baptism records into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load from database
        bautismos = self.db.obtener_bautismos()
        for bautismo in bautismos:
            certificado = "✅" if bautismo["certificado_generado"] else "❌"
            email = "✅" if bautismo["email_enviado"] else "❌"

            self.tree.insert(
                "",
                "end",
                values=(
                    bautismo["id"],
                    bautismo["nombre_completo"],
                    bautismo["email"],
                    bautismo["fecha_bautismo"],
                    bautismo["iglesia"] or "",
                    certificado,
                    email,
                ),
            )

    def update_stats(self):
        """Update statistics display"""
        stats = self.db.obtener_estadisticas()

        stats_text = f"""
📊 ESTADÍSTICAS

👥 Total registros: {stats['total']}
📄 Certificados pendientes: {stats['pendientes']}
✅ Certificados completados: {stats['completados']}
📧 Emails enviados: {stats['emails_enviados']}
        """

        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state=tk.DISABLED)

    def editar_bautismo(self, event):
        """Edit baptism record"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            bautismo_id = item["values"][0]

            # Get baptism data from database
            bautismo_data = self.db.obtener_bautismo_por_id(bautismo_id)

            if bautismo_data:
                # Import and open edit window
                try:
                    from edit_window import EditBautismoWindow

                    EditBautismoWindow(self.root, bautismo_data, self.db)
                except ImportError as e:
                    messagebox.showerror(
                        "Error", f"No se pudo cargar la ventana de edición: {e}"
                    )
            else:
                messagebox.showerror(
                    "Error", "No se pudo obtener los datos del bautismo"
                )
        else:
            messagebox.showwarning(
                "Advertencia", "Por favor selecciona un bautismo para editar"
            )

    def editar_seleccionado(self):
        """Edit selected baptism record (button click)"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            bautismo_id = item["values"][0]

            # Get baptism data from database
            bautismo_data = self.db.obtener_bautismo_por_id(bautismo_id)

            if bautismo_data:
                # Import and open edit window
                try:
                    from edit_window import EditBautismoWindow

                    EditBautismoWindow(self.root, bautismo_data, self.db)
                except ImportError as e:
                    messagebox.showerror(
                        "Error", f"No se pudo cargar la ventana de edición: {e}"
                    )
            else:
                messagebox.showerror(
                    "Error", "No se pudo obtener los datos del bautismo"
                )
        else:
            messagebox.showwarning(
                "Advertencia", "Por favor selecciona un bautismo para editar"
            )

    def generar_certificados_threaded(self):
        """Generate certificates in a separate thread"""
        thread = threading.Thread(target=self.generar_certificados)
        thread.daemon = True
        thread.start()

    def generar_certificados(self):
        """Generate certificates for pending baptisms"""
        self.progress_var.set("🔄 Generando certificados...")
        self.root.update()

        bautismos_pendientes = self.db.obtener_bautismos_pendientes()

        if not bautismos_pendientes:
            self.progress_var.set("ℹ️ No hay certificados pendientes")
            messagebox.showinfo("Info", "No hay certificados pendientes de generar")
            return

        # Check if template exists
        template_path = "data/template.pdf"
        if not os.path.exists(template_path):
            self.progress_var.set("❌ Plantilla no encontrada")
            messagebox.showerror(
                "Error", f"No se encontró la plantilla: {template_path}"
            )
            return

        # Create output directory
        os.makedirs("output", exist_ok=True)

        generados = 0
        total = len(bautismos_pendientes)

        for i, bautismo in enumerate(bautismos_pendientes, 1):
            try:
                self.progress_var.set(
                    f"🔄 Generando {i}/{total}: {bautismo['nombre_completo']}"
                )
                self.root.update()

                # Generate certificate
                safe_name = "".join(
                    c
                    for c in bautismo["nombre_completo"]
                    if c.isalnum() or c in (" ", "-", "_")
                ).rstrip()
                output_path = f"output/certificado_{safe_name}.pdf"

                if generate_certificate(
                    bautismo["nombre_completo"],
                    bautismo["fecha_bautismo"],
                    bautismo["iglesia"] or "Iglesia Default",
                    template_path,
                    output_path,
                ):
                    self.db.marcar_certificado_generado(bautismo["id"])
                    generados += 1

            except Exception as e:
                print(
                    f"Error generando certificado para {bautismo['nombre_completo']}: {e}"
                )

        self.progress_var.set(f"✅ Generados {generados}/{total} certificados")
        messagebox.showinfo(
            "Completado", f"Se generaron {generados} de {total} certificados"
        )
        self.load_bautismos()
        self.update_stats()

    def enviar_emails_threaded(self):
        """Send emails in a separate thread"""
        thread = threading.Thread(target=self.enviar_emails)
        thread.daemon = True
        thread.start()

    def enviar_emails(self):
        """Send emails for generated certificates"""
        self.progress_var.set("🔄 Verificando configuración de email...")
        self.root.update()

        # Test email configuration
        if not test_email_configuration():
            self.progress_var.set("❌ Configuración de email inválida")
            messagebox.showerror("Error", "Configuración de email no válida")
            return

        # Test connection
        success, message = test_email_connection()
        if not success:
            self.progress_var.set("❌ Error de conexión")
            messagebox.showerror(
                "Error de Conexión",
                f"No se pudo conectar al servidor de email:\n{message}",
            )
            return

        bautismos = self.db.obtener_bautismos()
        enviados = 0
        total_enviables = 0

        # Count sendable emails
        for bautismo in bautismos:
            if bautismo["certificado_generado"] and not bautismo["email_enviado"]:
                total_enviables += 1

        if total_enviables == 0:
            self.progress_var.set("ℹ️ No hay emails para enviar")
            messagebox.showinfo("Info", "No hay emails pendientes de envío")
            return

        for i, bautismo in enumerate(bautismos, 1):
            if bautismo["certificado_generado"] and not bautismo["email_enviado"]:
                try:
                    self.progress_var.set(
                        f"📧 Enviando {enviados + 1}/{total_enviables}: {bautismo['email']}"
                    )
                    self.root.update()

                    safe_name = "".join(
                        c
                        for c in bautismo["nombre_completo"]
                        if c.isalnum() or c in (" ", "-", "_")
                    ).rstrip()
                    certificate_path = f"output/certificado_{safe_name}.pdf"

                    if os.path.exists(certificate_path):
                        if send_baptism_congratulations_email(
                            bautismo["email"],
                            bautismo["nombre_completo"],
                            certificate_path,
                        ):
                            self.db.marcar_email_enviado(bautismo["id"])
                            enviados += 1

                except Exception as e:
                    print(f"Error enviando email a {bautismo['email']}: {e}")

        self.progress_var.set(f"✅ Enviados {enviados}/{total_enviables} emails")
        messagebox.showinfo(
            "Completado", f"Se enviaron {enviados} de {total_enviables} emails"
        )
        self.load_bautismos()
        self.update_stats()

    def probar_email(self):
        """Test email configuration and connection"""
        self.progress_var.set("🔄 Probando configuración de email...")
        self.root.update()

        if not test_email_configuration():
            self.progress_var.set("❌ Configuración inválida")
            messagebox.showerror("Error", "Configuración de email no válida")
            return

        self.progress_var.set("🔄 Probando conexión...")
        self.root.update()

        success, message = test_email_connection()
        if success:
            self.progress_var.set("✅ Conexión exitosa")
            messagebox.showinfo(
                "Éxito", "Configuración de email correcta\nSe envió un email de prueba"
            )
        else:
            self.progress_var.set("❌ Error de conexión")
            messagebox.showerror("Error", f"Error de conexión:\n{message}")

    def exportar_excel(self):
        """Export database to Excel"""
        # Check dependencies first
        deps_ok, error_msg = check_excel_dependencies()
        if not deps_ok:
            messagebox.showerror(
                "Error de Dependencias",
                f"Faltan dependencias para exportar a Excel:\n{error_msg}\n\n"
                "Instale con: pip install pandas openpyxl",
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )

        if filename:
            self.progress_var.set("🔄 Exportando a Excel...")
            self.root.update()

            try:
                if self.db.exportar_a_excel(filename):
                    self.progress_var.set("✅ Exportación completada")
                    messagebox.showinfo("Éxito", f"Archivo exportado a: {filename}")
                else:
                    self.progress_var.set("❌ Error en exportación")
                    messagebox.showerror(
                        "Error",
                        "Error al exportar el archivo. Verifique que pandas y openpyxl estén instalados.",
                    )
            except Exception as e:
                self.progress_var.set("❌ Error en exportación")
                messagebox.showerror("Error", f"Error inesperado al exportar: {str(e)}")

    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = BautismoApp()
    app.run()
