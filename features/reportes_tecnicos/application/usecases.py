import os
import requests
from typing import List
from fpdf import FPDF
from datetime import datetime
from features.reportes_tecnicos.domain.ports import ReporteTecnicoRepository
from features.reportes_tecnicos.domain.entities import ReporteTecnicoSolicitar, ReporteTecnicoResponse, WebhookPayload
from features.reportes_tecnicos.infrastructure.models import ReporteTecnicoModel
from core.clients.implementations.auth_service_client import auth_client

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://pyroguard_ml_api:8000")
BACKEND_WEBHOOK_URL = os.getenv("BACKEND_WEBHOOK_URL", "http://pyroguard_back:8001/api/v1/reportes_tecnicos/webhook")

class ReporteTecnicoUseCase:
    def __init__(self, repo: ReporteTecnicoRepository): 
        self.repo = repo
        
    def solicitar_generacion(self, r: ReporteTecnicoSolicitar, id_coord: str) -> ReporteTecnicoResponse:
        # 1. Llamar al Microservicio de ML
        payload = {
            "id_zona": str(r.id_zona),
            "webhook_url": BACKEND_WEBHOOK_URL
        }
        
        try:
            resp = requests.post(f"{ML_SERVICE_URL}/api/v1/reportes/generar", json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            task_id = data.get("task_id")
        except Exception as e:
            raise Exception(f"No se pudo contactar al servicio de ML: {e}")

        # 2. Guardar estado pendiente en BD
        m = self.repo.create_pending(str(r.id_zona), id_coord, task_id)
        return self._build(m)

    def procesar_webhook(self, payload: WebhookPayload):
        # 1. Extraer JSON del LLM
        reporte_json = payload.reporte_json
        
        # 2. Generar el PDF
        pdf_path = self._generar_pdf(payload.id_zona, reporte_json)
        
        # 3. Actualizar la base de datos
        # Intentamos extraer el nivel de riesgo
        nivel_riesgo = "DESCONOCIDO"
        if "CRÍTICO" in reporte_json.analisis_de_riesgo.upper(): nivel_riesgo = "CRÍTICO"
        elif "ALTO" in reporte_json.analisis_de_riesgo.upper(): nivel_riesgo = "ALTO"
        elif "MEDIO" in reporte_json.analisis_de_riesgo.upper(): nivel_riesgo = "MEDIO"
        elif "BAJO" in reporte_json.analisis_de_riesgo.upper(): nivel_riesgo = "BAJO"
        
        self.repo.update_completed(payload.task_id, pdf_path, nivel_riesgo)

    def _generar_pdf(self, id_zona: str, reporte) -> str:
        pdf = FPDF()
        pdf.set_margins(10, 10, 10)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        epw = pdf.w - 20 # Ancho efectivo de la página
        
        # Helper interno para evitar caídas por acentos o comillas tipográficas del LLM
        def safe_text(texto):
            if not texto: return ""
            # Reemplazar explícitamente algunos caracteres problemáticos comunes del LLM
            t = str(texto).replace('"', '"').replace('"', '"').replace("'", "'").replace("'", "'").replace('—', '-')
            return t.encode('latin-1', 'replace').decode('latin-1')

        pdf.set_font("helvetica", "B", 16)
        pdf.cell(epw, 10, safe_text("Reporte Técnico de Protección Civil"), new_x="LMARGIN", new_y="NEXT", align='C')
        
        pdf.set_font("helvetica", "", 10)
        pdf.cell(epw, 10, safe_text(f"Fecha de Emisión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), new_x="LMARGIN", new_y="NEXT", align='R')
        pdf.ln(10)
        
        # Resumen Ejecutivo
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(epw, 10, safe_text("Resumen Ejecutivo"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(epw, 8, safe_text(reporte.resumen_ejecutivo))
        pdf.ln(5)
        
        # Análisis de Riesgo
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(epw, 10, safe_text("Análisis de Riesgo"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(epw, 8, safe_text(reporte.analisis_de_riesgo))
        pdf.ln(5)
        
        # Justificación
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(epw, 10, safe_text("Justificación del Protocolo"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(epw, 8, safe_text(reporte.justificacion_protocolo))
        pdf.ln(5)
        
        # Acciones Tácticas
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(epw, 10, safe_text("Acciones Tácticas Recomendadas"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        for i, accion in enumerate(reporte.acciones_tacticas):
            pdf.multi_cell(epw, 8, safe_text(f"{i+1}. {accion.accion}"))
            if accion.fuente:
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(epw, 6, safe_text(f"   Fuente: {accion.fuente}"))
                pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
        
        # Usar la carpeta uploads que ya está mapeada en el servidor web (FastAPI static files)
        os.makedirs("/app/uploads/reportes_pdf", exist_ok=True)
        filename = f"reporte_{id_zona}_{int(datetime.now().timestamp())}.pdf"
        filepath = f"/app/uploads/reportes_pdf/{filename}"
        
        pdf.output(filepath)
        
        return f"/uploads/reportes_pdf/{filename}"

    def listar(self, id_zona: str) -> List[ReporteTecnicoResponse]:
        return [self._build(m) for m in self.repo.get_by_zona(id_zona)]
        
    def _build(self, m: ReporteTecnicoModel) -> ReporteTecnicoResponse:
        nombre = None
        if m.id_coordinador:
            try:
                info = auth_client.get_user_info(m.id_coordinador)
                if info: nombre = info.get("nombre")
            except: pass
        return ReporteTecnicoResponse(
            id_reporte=m.id_reporte, 
            id_zona=m.id_zona, 
            id_coordinador=m.id_coordinador, 
            coordinador_nombre=nombre,
            estado=m.estado,
            task_id=m.task_id,
            nivel_riesgo_registrado=m.nivel_riesgo_registrado, 
            archivo_pdf_path=m.archivo_pdf_path, 
            creado_en=m.creado_en
        )