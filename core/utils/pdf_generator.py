from fpdf import FPDF
from pathlib import Path
import datetime
from uuid import uuid4

# Directorio donde se guardarán los PDFs generados
REPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "storage" / "reportes_pdf"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_technical_report(id_zona: str, nivel_riesgo: str, coordinador_nombre: str) -> str:
    """
    Genera un PDF técnico con los datos de la alerta y devuelve la ruta del archivo.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'PyroGuard AI - Reporte Tecnico de Alerta', ln=1, align='C')
    pdf.ln(10)
    
    # Content
    pdf.set_font('Arial', '', 12)
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    pdf.cell(0, 10, f'Fecha de Generacion: {fecha_actual}', ln=1)
    pdf.cell(0, 10, f'ID de Zona Protegida: {id_zona}', ln=1)
    pdf.cell(0, 10, f'Nivel de Riesgo Registrado: {nivel_riesgo}', ln=1)
    pdf.cell(0, 10, f'Generado por (Coordinador): {coordinador_nombre}', ln=1)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.multi_cell(0, 10, 'Este documento certifica que el coordinador ha revisado la alerta correspondiente al nivel de riesgo emitido por el microservicio de Machine Learning y ha tomado conocimiento de la misma para el despacho de brigadas preventivas.')
    
    # Save
    file_name = f"Reporte_{id_zona}_{uuid4().hex[:6]}.pdf"
    file_path = REPORTS_DIR / file_name
    pdf.output(str(file_path))
    
    return str(file_path)
