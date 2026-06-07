#!/usr/bin/env python3
"""
Generates a personalized clinical PDF card for a 14-year-old patient.
Interests: boxing, river, hairdressing — used as design theme elements.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
import os

OUTPUT_PATH = "/home/user/skillsfind/plan_clinico_intervencion.pdf"

# ── Color palette inspired by her interests ──────────────────────────────────
# Boxing → strong reds / burgundy
# River  → teal / steel blue
# Hairdressing → soft violet / rose
C_BOXING_RED    = colors.HexColor("#C0392B")   # strong red
C_BOXING_DARK   = colors.HexColor("#7B241C")   # dark burgundy
C_RIVER_TEAL    = colors.HexColor("#1A7A8A")   # deep teal
C_RIVER_LIGHT   = colors.HexColor("#AED6F1")   # light sky blue
C_HAIR_VIOLET   = colors.HexColor("#7D3C98")   # violet
C_HAIR_ROSE     = colors.HexColor("#F5CBA7")   # warm rose/peach
C_ALERT         = colors.HexColor("#E74C3C")   # alert red
C_ALERT_BG      = colors.HexColor("#FDEDEC")   # alert background
C_SECTION_BG    = colors.HexColor("#EBF5FB")   # section background
C_DARK_TEXT     = colors.HexColor("#1C2833")   # main text
C_SUBTEXT       = colors.HexColor("#566573")   # secondary text
C_WHITE         = colors.white
C_GOLD          = colors.HexColor("#D4AC0D")   # accent gold
C_PHASE1        = colors.HexColor("#1ABC9C")   # phase 1 emerald
C_PHASE2        = colors.HexColor("#E67E22")   # phase 2 orange
C_PHASE3        = colors.HexColor("#8E44AD")   # phase 3 purple
C_BORDER_LIGHT  = colors.HexColor("#D5D8DC")

W, H = A4  # 210 x 297 mm


# ── Custom canvas decorator (header + footer + watermark) ────────────────────
class CardCanvas(canvas.Canvas):
    def __init__(self, filename, doc=None, **kwargs):
        kwargs.setdefault("pagesize", A4)
        super().__init__(filename, **kwargs)
        self._card_doc = doc
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_page(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_page(self, total_pages):
        self.saveState()
        self._draw_header()
        self._draw_footer(total_pages)
        self._draw_interest_stripe()
        self.restoreState()

    def _draw_header(self):
        # Top gradient bar (boxing red → teal)
        self.setFillColor(C_BOXING_DARK)
        self.rect(0, H - 22*mm, W, 22*mm, fill=1, stroke=0)

        # Accent stripe (violet — hairdressing)
        self.setFillColor(C_HAIR_VIOLET)
        self.rect(0, H - 25*mm, W, 3*mm, fill=1, stroke=0)

        # Title
        self.setFillColor(C_WHITE)
        self.setFont("Helvetica-Bold", 13)
        self.drawString(12*mm, H - 13*mm, "PLAN CLÍNICO DE INTERVENCIÓN")

        # Subtitle / classification
        self.setFont("Helvetica", 7.5)
        self.setFillColor(C_HAIR_ROSE)
        self.drawString(12*mm, H - 19*mm,
            "Paciente: Adolescente — 14 años  |  CPTSD + Trauma Sexual Intrafamiliar  |  "
            "USO EXCLUSIVO PROFESIONALES SALUD MENTAL  ·  Documento anonimizado")

        # Interest icons (text symbols)
        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(C_GOLD)
        self.drawRightString(W - 12*mm, H - 12*mm, "🥊 Boxeo  🌊 Río  ✂️ Peluquería")

    def _draw_footer(self, total_pages):
        self.setFillColor(C_BORDER_LIGHT)
        self.rect(0, 0, W, 12*mm, fill=1, stroke=0)
        self.setFillColor(C_BOXING_RED)
        self.rect(0, 12*mm, W, 1*mm, fill=1, stroke=0)

        self.setFont("Helvetica-Oblique", 7)
        self.setFillColor(C_SUBTEXT)
        self.drawString(12*mm, 5*mm,
            "Este documento es un apoyo clínico y NO sustituye el juicio profesional. "
            "Notificación mandatoria a protección de menores obligatoria.")
        page_num = getattr(self, '_pageNumber', 1)
        self.drawRightString(W - 12*mm, 5*mm, f"Página {page_num} / {total_pages}")

    def _draw_interest_stripe(self):
        # Left vertical stripe with interest colors
        stripe_w = 4*mm
        third = (H - 37*mm) / 3
        y0 = 13*mm
        self.setFillColor(C_BOXING_RED)
        self.rect(0, y0 + 2*third, stripe_w, third, fill=1, stroke=0)
        self.setFillColor(C_RIVER_TEAL)
        self.rect(0, y0 + third, stripe_w, third, fill=1, stroke=0)
        self.setFillColor(C_HAIR_VIOLET)
        self.rect(0, y0, stripe_w, third, fill=1, stroke=0)


def build_doc(path):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=18*mm,
        rightMargin=12*mm,
        topMargin=30*mm,
        bottomMargin=16*mm,
        title="Plan Clínico de Intervención",
        author="Equipo Clínico",
        subject="CPTSD – Adolescente 14 años",
    )
    story = []
    styles = _build_styles()
    _add_patient_banner(story, styles)
    _add_priority_section(story, styles)
    _add_diagnosis_section(story, styles)
    _add_multidisciplinary_section(story, styles)
    _add_phase1_section(story, styles)
    _add_phase2_section(story, styles)
    _add_phase3_section(story, styles)
    _add_evidence_section(story, styles)

    def make_canvas(filename, **kwargs):
        return CardCanvas(filename, doc=doc, **kwargs)

    doc.build(story, canvasmaker=make_canvas)
    print(f"✅  PDF generado: {path}")


# ── Style helpers ─────────────────────────────────────────────────────────────
def _build_styles():
    base = getSampleStyleSheet()
    s = {}

    s["section_title"] = ParagraphStyle(
        "section_title", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=10,
        textColor=C_WHITE, leading=14,
        spaceAfter=2*mm, spaceBefore=4*mm,
    )
    s["body"] = ParagraphStyle(
        "body", parent=base["Normal"],
        fontName="Helvetica", fontSize=8,
        textColor=C_DARK_TEXT, leading=12,
        leftIndent=3*mm, spaceAfter=1.5*mm,
    )
    s["bullet"] = ParagraphStyle(
        "bullet", parent=base["Normal"],
        fontName="Helvetica", fontSize=7.8,
        textColor=C_DARK_TEXT, leading=11.5,
        leftIndent=6*mm, bulletIndent=2*mm,
        spaceAfter=1.2*mm,
    )
    s["bullet_bold"] = ParagraphStyle(
        "bullet_bold", parent=s["bullet"],
        fontName="Helvetica-Bold",
    )
    s["note"] = ParagraphStyle(
        "note", parent=base["Normal"],
        fontName="Helvetica-Oblique", fontSize=7.5,
        textColor=C_SUBTEXT, leading=11,
        leftIndent=3*mm, spaceAfter=2*mm,
    )
    s["alert"] = ParagraphStyle(
        "alert", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=8,
        textColor=C_ALERT, leading=12,
        leftIndent=3*mm, spaceAfter=1.5*mm,
    )
    s["phase_label"] = ParagraphStyle(
        "phase_label", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=7.5,
        textColor=C_WHITE, leading=10,
    )
    s["sub_header"] = ParagraphStyle(
        "sub_header", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=8.5,
        textColor=C_RIVER_TEAL, leading=12,
        spaceBefore=2*mm, spaceAfter=1*mm, leftIndent=3*mm,
    )
    return s


def _section_header(title, color, story, styles):
    """Colored section header bar."""
    header_table = Table(
        [[Paragraph(f"■  {title}", styles["section_title"])]],
        colWidths=[W - 30*mm],
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(header_table)


def _bullet(text, styles, bold_label=None):
    """Single bullet item, optionally with bold prefix."""
    if bold_label:
        full = f"<b>{bold_label}</b> {text}"
    else:
        full = text
    return Paragraph(f"•  {full}", styles["bullet"])


def _add_patient_banner(story, styles):
    data = [
        [
            Paragraph("<b>Paciente</b>", styles["body"]),
            Paragraph("Adolescente · 14 años", styles["body"]),
            Paragraph("<b>Dx principal</b>", styles["body"]),
            Paragraph("CPTSD (CIE-11: 6B41)", styles["body"]),
        ],
        [
            Paragraph("<b>Intereses</b>", styles["body"]),
            Paragraph("Boxeo 🥊 · Río 🌊 · Peluquería ✂️", styles["body"]),
            Paragraph("<b>Antec. suicidio</b>", styles["body"]),
            Paragraph("3 intentos previos — RIESGO MÁXIMO", styles["alert"]),
        ],
    ]
    t = Table(data, colWidths=[32*mm, 60*mm, 35*mm, 53*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_ALERT_BG),
        ("BACKGROUND", (2, 1), (3, 1), colors.HexColor("#FDEDEC")),
        ("BOX", (0, 0), (-1, -1), 1, C_BOXING_RED),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    story.append(t)
    story.append(Spacer(1, 3*mm))


def _add_priority_section(story, styles):
    _section_header("PRIORIDAD ABSOLUTA — RIESGO VITAL ACTIVO", C_BOXING_RED, story, styles)

    items = [
        ("Riesgo de reintento:", "La paciente presenta 3 intentos de suicidio previos, situándola en el grupo de máximo riesgo estadístico."),
        ("Evaluación:", "Evaluación del riesgo suicida en cada contacto mediante la escala Columbia C-SSRS para adolescentes."),
        ("Plan de Seguridad (Stanley-Brown SPI):", "Identificación de señales de alerta, personas de confianza, estrategias de distracción y retirada de medios letales."),
        ("Obligación Legal:", "Notificación mandatoria a protección de menores por presunto delito de abuso sexual intrafamiliar."),
        ("Soporte Farmacológico:", "Valoración psiquiátrica urgente, considerando ISRS y vigilancia de activación conductual."),
    ]

    rows = []
    for label, text in items:
        rows.append([
            Paragraph(f"<b>{label}</b>", styles["bullet"]),
            Paragraph(text, styles["bullet"]),
        ])

    t = Table(rows, colWidths=[52*mm, 126*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_ALERT_BG),
        ("BOX", (0, 0), (-1, -1), 0.7, C_BOXING_RED),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(KeepTogether(t))
    story.append(Spacer(1, 2*mm))


def _add_diagnosis_section(story, styles):
    _section_header("DIAGNÓSTICO Y FORMULACIÓN CLÍNICA", C_BOXING_DARK, story, styles)

    items = [
        _bullet("TEPT Complejo (CPTSD) según CIE-11 (6B41).", styles, "Diagnóstico Principal:"),
        _bullet("Trastorno Depresivo Mayor severo · Trastorno de Ansiedad reactivo al trauma.", styles, "Comorbilidades:"),
        _bullet("Posible TDI (inicio abusos a los 6 años, crisis disociativas) y TLP emergente.", styles, "A explorar:"),
        _bullet("Trauma relacional primario con el agresor como figura de apego · inicio preverbal-temprano con daño en el desarrollo del self · autolesiones como regulación disfuncional.", styles, "Factores de mantenimiento:"),
    ]

    content_table = Table(
        [[item] for item in items],
        colWidths=[W - 30*mm],
    )
    content_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_SECTION_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(KeepTogether(content_table))
    story.append(Spacer(1, 2*mm))


def _add_multidisciplinary_section(story, styles):
    _section_header("COORDINACIÓN MULTIDISCIPLINAR", C_RIVER_TEAL, story, styles)

    disciplines = [
        ("Psiquiatría infanto-juvenil", "Seguimiento farmacológico"),
        ("Psicología clínica", "Intervención psicoterapéutica principal"),
        ("Enfermería salud mental", "Psicoeducación y plan de seguridad"),
        ("Trabajo social", "Coordinación protección de menores y familia extensa"),
        ("Centro educativo", "Protocolo de apoyo y vigilancia con escolarización activa"),
    ]

    rows = [[
        Paragraph(f"<b>{d}</b>", styles["bullet"]),
        Paragraph(role, styles["bullet"]),
    ] for d, role in disciplines]

    t = Table(rows, colWidths=[65*mm, 113*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D6EAF8")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#EBF5FB")),
        ("BOX", (0, 0), (-1, -1), 0.7, C_RIVER_TEAL),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(KeepTogether(t))
    story.append(Spacer(1, 2*mm))


def _add_phase1_section(story, styles):
    _section_header("FASE 1 — ESTABILIZACIÓN (PRIORITARIA)", C_PHASE1, story, styles)

    meta = [
        [Paragraph("<b>Duración:</b> 3-6 meses mínimo, sesiones semanales o más frecuentes.", styles["body"]),
         Paragraph("<b>Modalidad:</b> DBT-A (Terapia Dialéctica Conductual para Adolescentes).", styles["body"])],
        [Paragraph("<b>Objetivo:</b> Establecer seguridad y regulación del SN <i>sin</i> procesar contenido traumático.", styles["body"]),
         Paragraph("<b>Entorno:</b> Inclusión de un adulto protector en el módulo familiar de DBT-A.", styles["body"])],
    ]
    meta_t = Table(meta, colWidths=[95*mm, 83*mm])
    meta_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F8F5")),
        ("BOX", (0, 0), (-1, -1), 0.5, C_PHASE1),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(meta_t)
    story.append(Spacer(1, 1.5*mm))

    story.append(Paragraph("Técnicas de primera elección:", styles["sub_header"]))
    techniques = [
        ("Tolerancia al malestar", "Habilidades TIPP, ACCEPTS, IMPROVE."),
        ("Regulación emocional", "Identificación de emociones, PLEASE, Opuestos a la acción."),
        ("Grounding 5-4-3-2-1", "Herramienta central para crisis disociativas. Ancla al presente mediante los 5 sentidos."),
        ("Técnica STOP", "Intervención en crisis agudas: Stop, Take a step back, Observe, Proceed mindfully."),
        ("Psicoeducación disociación", "Trabajo suave con partes (IFS) — no procesar trauma todavía."),
    ]
    rows = [[
        Paragraph(f"<b>{t}</b>", styles["bullet"]),
        Paragraph(desc, styles["bullet"]),
    ] for t, desc in techniques]

    t = Table(rows, colWidths=[55*mm, 123*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D5F5E3")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F0FBF6")),
        ("BOX", (0, 0), (-1, -1), 0.7, C_PHASE1),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(KeepTogether(t))

    story.append(Paragraph(
        "⚠ Nota Crítica: El vínculo terapéutico es el principal instrumento de reparación ante el daño profundo en la confianza.",
        styles["note"]
    ))
    story.append(Spacer(1, 2*mm))


def _add_phase2_section(story, styles):
    _section_header("FASE 2 — PROCESAMIENTO TRAUMÁTICO", C_PHASE2, story, styles)

    meta_rows = [[
        Paragraph("<b>Inicio:</b> Solo tras alcanzar estabilidad mínima sostenida.", styles["body"]),
        Paragraph("<b>Duración:</b> 6-18 meses adicionales.", styles["body"]),
    ]]
    meta_t = Table(meta_rows, colWidths=[95*mm, 83*mm])
    meta_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FEF9E7")),
        ("BOX", (0, 0), (-1, -1), 0.5, C_PHASE2),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_t)
    story.append(Spacer(1, 1.5*mm))

    story.append(Paragraph("Opciones terapéuticas:", styles["sub_header"]))
    options = [
        ("TF-CBT", "Terapia cognitivo-conductual centrada en el trauma. Primera línea para abuso sexual en adolescentes."),
        ("EMDR adaptado", "Requiere estabilización previa sólida y formación específica. Procesamiento titulado."),
        ("Terapia de Esquemas", "Trabajo en esquemas nucleares de desconfianza/abuso. Útil si TLP emergente confirmado."),
    ]
    rows = [[
        Paragraph(f"<b>{o}</b>", styles["bullet"]),
        Paragraph(desc, styles["bullet"]),
    ] for o, desc in options]
    t = Table(rows, colWidths=[42*mm, 136*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#FAD7A0")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#FEF9E7")),
        ("BOX", (0, 0), (-1, -1), 0.7, C_PHASE2),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(KeepTogether(t))
    story.append(Paragraph(
        "Evaluación obligatoria antes de iniciar fase 2: aplicar escalas disociativas A-DES o MID-C.",
        styles["note"]
    ))
    story.append(Spacer(1, 2*mm))


def _add_phase3_section(story, styles):
    _section_header("FASE 3 — INTEGRACIÓN Y RECONEXIÓN", C_PHASE3, story, styles)

    items = [
        _bullet("Reconstrucción identitaria y reconexión vital.", styles, "Objetivo:"),
        _bullet("ACT adaptada · Terapia Narrativa para reconstruir la historia vital · Trabajo en vínculos seguros e identidad futura.", styles, "Intervenciones:"),
        _bullet("Planificado con atención a posibles reacciones de abandono y cierre gradual.", styles, "Cierre:"),
    ]
    content_t = Table([[item] for item in items], colWidths=[W - 30*mm])
    content_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5EEF8")),
        ("BOX", (0, 0), (-1, -1), 0.5, C_PHASE3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(KeepTogether(content_t))
    story.append(Spacer(1, 2*mm))


def _add_evidence_section(story, styles):
    _section_header("EVIDENCIA CIENTÍFICA Y CUIDADO DEL EQUIPO", C_RIVER_TEAL, story, styles)

    evid_data = [
        [
            Paragraph("<b>DBT-A</b>", styles["bullet"]),
            Paragraph("Nivel A — Alta evidencia para autolesiones y regulación emocional en adolescentes.", styles["bullet"]),
        ],
        [
            Paragraph("<b>TF-CBT</b>", styles["bullet"]),
            Paragraph("Nivel A — Primera línea en trauma sexual infanto-juvenil (Cohen et al.).", styles["bullet"]),
        ],
        [
            Paragraph("<b>EMDR</b>", styles["bullet"]),
            Paragraph("Nivel A — OMS recomienda para PTSD; adaptación requerida en CPTSD.", styles["bullet"]),
        ],
    ]
    ev_t = Table(evid_data, colWidths=[28*mm, 150*mm])
    ev_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D6EAF8")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#EBF5FB")),
        ("BOX", (0, 0), (-1, -1), 0.7, C_RIVER_TEAL),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, C_BORDER_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(ev_t)
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("Autocuidado del equipo:", styles["sub_header"]))
    self_care = [
        _bullet("Riesgo de fatiga por compasión y trauma vicario: obligatorio el autocuidado activo.", styles),
        _bullet("Supervisión clínica regular — individual y grupal — con esp. en casos de trauma sexual y riesgo suicida.", styles),
        _bullet("El equipo que cuida a esta paciente también necesita ser cuidado.", styles),
    ]
    care_t = Table([[item] for item in self_care], colWidths=[W - 30*mm])
    care_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EBF5FB")),
        ("BOX", (0, 0), (-1, -1), 0.5, C_RIVER_TEAL),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(KeepTogether(care_t))


if __name__ == "__main__":
    build_doc(OUTPUT_PATH)
