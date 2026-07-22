import os
import requests
from typing import List, Optional
from fpdf import FPDF
from datetime import datetime
from features.reportes_tecnicos.domain.ports import ReporteTecnicoRepository
from features.reportes_tecnicos.domain.entities import ReporteTecnicoSolicitar, ReporteTecnicoResponse, WebhookPayload
from features.reportes_tecnicos.infrastructure.models import ReporteTecnicoModel
from core.clients.implementations.auth_service_client import auth_client
from features.notificaciones.domain.ports import DeviceTokenRepository
from core.clients.implementations.firebase_client import firebase_client

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://pyroguard.inode.cloud/ml:8000")
BACKEND_WEBHOOK_URL = os.getenv("BACKEND_WEBHOOK_URL", "http://pyroguard.inode.cloud/api:8001/api/v1/reportes_tecnicos/webhook")

class ReportePDF(FPDF):
    """PDF con identidad visual propia para los reportes de Protección Civil."""

    COLORS = {
        "primary": (18, 46, 92),          
        "primary_light": (235, 241, 250),
        "text": (35, 35, 35),
        "muted": (110, 110, 110),
        "line": (220, 224, 230),
        "CRITICO": (192, 57, 43),
        "ALTO": (211, 84, 0),
        "MEDIO": (230, 160, 20),
        "BAJO": (39, 174, 96),
        "DESCONOCIDO": (127, 140, 141),
    }

    def __init__(self, id_zona: str, nivel_riesgo: str = "DESCONOCIDO"):
        super().__init__(format="A4")
        self.id_zona = id_zona
        self.nivel_riesgo = nivel_riesgo if nivel_riesgo in self.COLORS else "DESCONOCIDO"
        self.set_margins(15, 26, 15)
        self.set_auto_page_break(auto=True, margin=22)
        self.alias_nb_pages()

    @property
    def epw(self) -> float:
        return self.w - self.l_margin - self.r_margin

    @staticmethod
    def _safe(texto) -> str:
        if not texto:
            return ""
        t = (
            str(texto)
            .replace("\u201c", '"').replace("\u201d", '"')
            .replace("\u2018", "'").replace("\u2019", "'")
            .replace("\u2014", "-").replace("\u2013", "-")
            .replace("\u2026", "...")
        )
        return t.encode("latin-1", "replace").decode("latin-1")

    def _risk_color(self):
        return self.COLORS.get(self.nivel_riesgo, self.COLORS["DESCONOCIDO"])

    def header(self):
        self.set_fill_color(*self.COLORS["primary"])
        self.rect(0, 0, self.w, 24, style="F")

        self.set_xy(15, 6)
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 14)
        self.cell(120, 6, self._safe("Reporte Técnico"), new_x="LMARGIN", new_y="NEXT")
        self.set_x(15)
        self.set_font("helvetica", "", 9)
        self.cell(120, 6, self._safe("Sistema de Protección Civil"))

        self.set_xy(-80, 6)
        self.set_font("helvetica", "", 9)
        self.cell(65, 6, self._safe(f"Zona: {self.id_zona}"), align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(-80, 13)
        self.cell(65, 6, self._safe(datetime.now().strftime("%d/%m/%Y %H:%M")), align="R")

        self.set_text_color(*self.COLORS["text"])
        self.set_y(30)

    def footer(self):
        self.set_y(-16)
        self.set_draw_color(*self.COLORS["line"])
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_y(-13)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(*self.COLORS["muted"])
        self.cell(0, 8, self._safe("Documento generado automáticamente - Uso interno"), align="L")
        self.set_y(-13)
        self.cell(0, 8, f"Página {self.page_no()}/{{nb}}", align="R")

    def risk_badge(self):
        """Píldora de color con el nivel de riesgo, alineada a la derecha."""
        color = self._risk_color()
        self.set_font("helvetica", "B", 10)
        label = f"NIVEL DE RIESGO: {self.nivel_riesgo}"
        w = self.get_string_width(label) + 10
        x = self.w - self.r_margin - w
        y = self.get_y()
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.rect(x, y, w, 8, style="F")
        self.set_xy(x, y)
        self.cell(w, 8, self._safe(label), align="C")
        self.set_text_color(*self.COLORS["text"])
        self.set_xy(self.l_margin, y + 12)

    def section_title(self, texto: str):
        self.ln(3)
        x, y = self.get_x(), self.get_y()
        self.set_fill_color(*self.COLORS["primary"])
        self.rect(x, y + 1, 3, 6, style="F")
        self.set_xy(x + 6, y)
        self.set_font("helvetica", "B", 12.5)
        self.set_text_color(*self.COLORS["primary"])
        self.cell(0, 8, self._safe(texto), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.COLORS["text"])
        self.set_x(x)
        self.ln(1)

    def body_text(self, texto: str):
        self.set_font("helvetica", "", 10.5)
        self.set_text_color(*self.COLORS["text"])
        self.multi_cell(self.epw, 6.2, self._safe(texto), align="J")
        self.ln(4)

    def accion_card(self, numero, accion: str, fuente: Optional[str] = None):
        pad = 4
        num_col = 10
        text_w = self.epw - num_col - pad * 2
        line_h = 5.5

        self.set_font("helvetica", "", 10)
        lineas_accion = self.multi_cell(text_w, line_h, self._safe(accion), dry_run=True, output="LINES")
        alto = len(lineas_accion) * line_h

        lineas_fuente = []
        if fuente:
            self.set_font("helvetica", "I", 8.5)
            lineas_fuente = self.multi_cell(text_w, 4.8, self._safe(f"Fuente: {fuente}"), dry_run=True, output="LINES")
            alto += len(lineas_fuente) * 4.8 + 2

        alto += pad * 2

        if self.get_y() + alto > self.page_break_trigger:
            self.add_page()

        x, y = self.l_margin, self.get_y()
        self.set_fill_color(*self.COLORS["primary_light"])
        self.rect(x, y, self.epw, alto, style="F")
        self.set_draw_color(*self._risk_color())
        self.rect(x, y, 1.5, alto, style="F")

        self.set_xy(x + pad, y + pad)
        self.set_font("helvetica", "B", 11)
        self.set_text_color(*self.COLORS["primary"])
        self.cell(num_col, line_h, str(numero), align="L")

        self.set_xy(x + pad + num_col, y + pad)
        self.set_font("helvetica", "", 10)
        self.set_text_color(*self.COLORS["text"])
        self.multi_cell(text_w, line_h, self._safe(accion))

        if fuente:
            self.set_x(x + pad + num_col)
            self.set_font("helvetica", "I", 8.5)
            self.set_text_color(*self.COLORS["muted"])
            self.multi_cell(text_w, 4.8, self._safe(f"Fuente: {fuente}"))

        self.set_text_color(*self.COLORS["text"])
        self.set_xy(x, y + alto + 4)
class ReporteTecnicoUseCase:
    def __init__(self, repo: ReporteTecnicoRepository, token_repo: DeviceTokenRepository = None):
        self.repo = repo
        self.token_repo = token_repo

    def solicitar_generacion(self, r: ReporteTecnicoSolicitar, id_coord: str) -> ReporteTecnicoResponse:
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

        m = self.repo.create_pending(str(r.id_zona), id_coord, task_id)
        return self._build(m)

    def procesar_webhook(self, payload: WebhookPayload):
        reporte_json = payload.reporte_json

        nivel_riesgo = self._extraer_nivel_riesgo(reporte_json.analisis_de_riesgo)

        pdf_path = self._generar_pdf(payload.id_zona, reporte_json, nivel_riesgo)

        reporte_db = self.repo.update_completed(payload.task_id, pdf_path, nivel_riesgo)
        
        if reporte_db and reporte_db.id_coordinador and getattr(self, 'token_repo', None):
            token_model = self.token_repo.get_token(str(reporte_db.id_coordinador))
            if token_model and token_model.fcm_token:
                firebase_client.send_notification(
                    token_model.fcm_token,
                    "Reporte Técnico Generado",
                    f"El reporte técnico que solicitaste ya está listo para descargarse en formato PDF."
                )

    @staticmethod
    def _extraer_nivel_riesgo(analisis: str) -> str:
        texto = (analisis or "").upper()
        for nivel in ("CRÍTICO", "CRITICO", "ALTO", "MEDIO", "BAJO"):
            if nivel in texto:
                return "CRITICO" if "CR" in nivel else nivel
        return "DESCONOCIDO"

    def _generar_pdf(self, id_zona: str, reporte, nivel_riesgo: str) -> str:
        pdf = ReportePDF(id_zona=id_zona, nivel_riesgo=nivel_riesgo)
        pdf.add_page()

        pdf.risk_badge()

        pdf.section_title("Resumen Ejecutivo")
        pdf.body_text(reporte.resumen_ejecutivo)

        pdf.section_title("Análisis de Riesgo")
        pdf.body_text(reporte.analisis_de_riesgo)

        pdf.section_title("Justificación del Protocolo")
        pdf.body_text(reporte.justificacion_protocolo)

        pdf.section_title("Acciones Tácticas Recomendadas")
        acciones = sorted(
            reporte.acciones_tacticas,
            key=lambda a: getattr(a, "orden", None) if getattr(a, "orden", None) is not None else 0
        )
        for i, accion in enumerate(acciones, start=1):
            pdf.accion_card(i, accion.accion, getattr(accion, "fuente", None))

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
                if info:
                    nombre = info.get("nombre")
            except Exception:
                pass
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