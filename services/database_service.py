import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseService:
    def __init__(self, db_path: str = "bautismos.db"):
        """Initialize database service"""
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Create database and tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create bautismos table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS bautismos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_completo TEXT NOT NULL,
                    email TEXT NOT NULL,
                    fecha_bautismo TEXT NOT NULL,
                    iglesia TEXT,
                    celula TEXT,
                    lider TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    certificado_generado BOOLEAN DEFAULT 0,
                    email_enviado BOOLEAN DEFAULT 0
                )
            """
            )

            conn.commit()

    def agregar_bautismo(
        self,
        nombre: str,
        email: str,
        fecha_bautismo: str,
        iglesia: str = "",
        celula: str = "",
        lider: str = "",
    ) -> bool:
        """Add a new baptism record"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO bautismos (nombre_completo, email, fecha_bautismo, iglesia, celula, lider)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (nombre, email, fecha_bautismo, iglesia, celula, lider),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error agregando bautismo: {e}")
            return False

    def obtener_bautismos(self, limit: int = 100) -> List[Dict]:
        """Get all baptism records"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM bautismos 
                    ORDER BY fecha_registro DESC 
                    LIMIT ?
                """,
                    (limit,),
                )

                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error obteniendo bautismos: {e}")
            return []

    def obtener_bautismos_pendientes(self) -> List[Dict]:
        """Get baptism records that need certificates generated"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM bautismos 
                    WHERE certificado_generado = 0 
                    ORDER BY fecha_bautismo
                """
                )

                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error obteniendo bautismos pendientes: {e}")
            return []

    def marcar_certificado_generado(self, bautismo_id: int, generated: bool = True) -> bool:
        """Mark certificate as generated or not generated"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE bautismos 
                    SET certificado_generado = ? 
                    WHERE id = ?
                """,
                    (1 if generated else 0, bautismo_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error marcando certificado: {e}")
            return False

    def marcar_email_enviado(self, bautismo_id: int) -> bool:
        """Mark email as sent"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE bautismos 
                    SET email_enviado = 1 
                    WHERE id = ?
                """,
                    (bautismo_id,),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error marcando email: {e}")
            return False

    def eliminar_bautismo(self, bautismo_id: int) -> bool:
        """Delete a baptism record"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bautismos WHERE id = ?", (bautismo_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error eliminando bautismo: {e}")
            return False

    def exportar_a_excel(self, excel_path: str) -> bool:
        """Export database to Excel format"""
        try:
            import pandas as pd
        except ImportError:
            print("Error: pandas no está instalado. Instale con: pip install pandas openpyxl")
            return False
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(
                    """
                    SELECT nombre_completo, email, fecha_bautismo, iglesia, celula, lider
                    FROM bautismos 
                    ORDER BY fecha_registro DESC
                """,
                    conn,
                )

                # Rename columns to match expected format
                df.columns = [
                    "Nombre Completo",
                    "Email",
                    "Fecha de Bautismo",
                    "Iglesia",
                    "Célula",
                    "Líder",
                ]
                df.to_excel(excel_path, index=False)
                return True
        except Exception as e:
            print(f"Error exportando a Excel: {e}")
            return False

    def obtener_estadisticas(self) -> Dict:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Total records
                cursor.execute("SELECT COUNT(*) FROM bautismos")
                total = cursor.fetchone()[0]

                # Pending certificates
                cursor.execute(
                    "SELECT COUNT(*) FROM bautismos WHERE certificado_generado = 0"
                )
                pendientes = cursor.fetchone()[0]

                # Sent emails
                cursor.execute("SELECT COUNT(*) FROM bautismos WHERE email_enviado = 1")
                emails_enviados = cursor.fetchone()[0]

                return {
                    "total": total,
                    "pendientes": pendientes,
                    "emails_enviados": emails_enviados,
                    "completados": total - pendientes,
                }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {"total": 0, "pendientes": 0, "emails_enviados": 0, "completados": 0}

    def obtener_bautismo_por_id(self, bautismo_id: int) -> Optional[Dict]:
        """Get a specific baptism record by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM bautismos WHERE id = ?",
                    (bautismo_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error obteniendo bautismo por ID: {e}")
            return None

    def actualizar_bautismo(
        self,
        bautismo_id: int,
        nombre: str,
        email: str,
        fecha_bautismo: str,
        iglesia: str = "",
        celula: str = "",
        lider: str = ""
    ) -> bool:
        """Update a baptism record"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE bautismos 
                    SET nombre_completo = ?, email = ?, fecha_bautismo = ?, 
                        iglesia = ?, celula = ?, lider = ?
                    WHERE id = ?
                    """,
                    (nombre, email, fecha_bautismo, iglesia, celula, lider, bautismo_id)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error actualizando bautismo: {e}")
            return False

    def regenerar_certificado(self, bautismo_id: int) -> bool:
        """Mark certificate as not generated to allow regeneration"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE bautismos SET certificado_generado = 0 WHERE id = ?",
                    (bautismo_id,)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error regenerando certificado: {e}")
            return False
