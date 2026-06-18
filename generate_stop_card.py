from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

OUTPUT = "/home/user/skillsfind/protocolo_STOP.pdf"

# ── Canvas-level draw: outer card border + header band ──────────────────────
def draw_card(c, doc):
    W, H = A4
    m = 12 * mm
    # outer border
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.roundRect(m, m, W - 2 * m, H - 2 * m, 6 * mm)
    # header band
    c.setFillColor(colors.black)
    c.roundRect(m, H - m - 22 * mm, W - 2 * m, 22 * mm, 6 * mm, fill=1, stroke=0)
    # fix bottom corners of header band (make them square)
    c.rect(m, H - m - 22 * mm, W - 2 * m, 6 * mm, fill=1, stroke=0)


def build():
    W, H = A4
    m = 12 * mm
    inner_w = W - 2 * m - 16 * mm   # content width inside card

    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=m + 8 * mm,
        leftMargin=m + 8 * mm,
        topMargin=m + 26 * mm,
        bottomMargin=m + 8 * mm,
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        W - doc.leftMargin - doc.rightMargin,
        H - doc.topMargin - doc.bottomMargin,
        id="main",
    )
    doc.addPageTemplates([PageTemplate(id="card", frames=[frame], onPage=draw_card)])

    # ── Styles ────────────────────────────────────────────────────────────────
    title_style = ParagraphStyle(
        "title", fontName="Helvetica-Bold", fontSize=16,
        textColor=colors.white, leading=20, alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=9,
        textColor=colors.white, leading=12, alignment=TA_CENTER, spaceBefore=1,
    )
    letter_style = ParagraphStyle(
        "letter", fontName="Helvetica-Bold", fontSize=26,
        textColor=colors.black, leading=30,
    )
    step_title_style = ParagraphStyle(
        "step_title", fontName="Helvetica-Bold", fontSize=10,
        textColor=colors.black, leading=13, spaceBefore=2,
    )
    quote_style = ParagraphStyle(
        "quote", fontName="Helvetica-Oblique", fontSize=8.5,
        textColor=colors.black, leading=11, leftIndent=4,
        spaceAfter=2,
    )
    body_style = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=7.5,
        textColor=colors.black, leading=10.5, leftIndent=8,
        bulletIndent=2,
    )
    note_style = ParagraphStyle(
        "note", fontName="Helvetica-Oblique", fontSize=7,
        textColor=colors.Color(0.3, 0.3, 0.3), leading=9, leftIndent=8,
    )
    footer_style = ParagraphStyle(
        "footer", fontName="Helvetica", fontSize=7,
        textColor=colors.Color(0.4, 0.4, 0.4), alignment=TA_CENTER, leading=9,
    )

    # ── Header (drawn on canvas) — add spacing placeholder ───────────────────
    # The canvas draws the header band; we push a title paragraph over it
    story = []

    # Title placed via absolute draw in onPage; we need a spacer to skip below band
    # Instead, draw title text here via a negatively-offset approach:
    # We use the canvas onPage for the band and draw the title there too.
    # So we just need the content below.

    def draw_header(c, doc):
        draw_card(c, doc)
        W2, H2 = A4
        m2 = 12 * mm
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(W2 / 2, H2 - m2 - 12 * mm, "Protocolo S.T.O.P.")
        c.setFont("Helvetica", 8.5)
        c.drawCentredString(W2 / 2, H2 - m2 - 19 * mm, "Parar · Respirar · Observar · Continuar con conciencia")

    doc.pageTemplates[0].onPage = draw_header

    # ── Step builder ─────────────────────────────────────────────────────────
    def divider():
        story.append(Spacer(1, 2 * mm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.Color(0.7,0.7,0.7)))
        story.append(Spacer(1, 2 * mm))

    def step(letter, name_es, name_en, quote, bullets, note=None):
        header_data = [[
            Paragraph(f"<b>{letter}</b>", letter_style),
            Paragraph(f"<b>{name_en}</b> / {name_es}", step_title_style),
        ]]
        tbl = Table(header_data, colWidths=[14*mm, inner_w - 14*mm])
        tbl.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 1),
        ]))
        story.append(tbl)
        story.append(Paragraph(f'"{quote}"', quote_style))
        for b in bullets:
            story.append(Paragraph(f"• {b}", body_style))
        if note:
            story.append(Spacer(1, 1*mm))
            story.append(Paragraph(note, note_style))

    # ── S ────────────────────────────────────────────────────────────────────
    step(
        "S", "Para", "STOP",
        "Detente justo donde estás. No hagas nada todavía.",
        [
            "Interrumpir físicamente la actividad o el hilo de pensamiento en curso.",
            "Puede implicar dejar de escribir, hablar o moverse.",
            "Señal interna: reconocer que hay activación emocional o cognitiva significativa.",
            "Objetivo: romper el automatismo reactivo.",
        ]
    )
    divider()

    # ── T ────────────────────────────────────────────────────────────────────
    step(
        "T", "Respira", "TAKE A BREATH",
        "Toma una respiración consciente, o varias.",
        [
            "Una respiración profunda y lenta, llevando atención al movimiento del abdomen.",
            "Opcional: técnica 4-4-4 (inhala 4 seg · retén 4 seg · exhala 4 seg).",
            "Objetivo neurofisiológico: activar el sistema nervioso parasimpático.",
        ],
        note="No forzar — observar la respiración tal como es también es válido."
    )
    divider()

    # ── O ────────────────────────────────────────────────────────────────────
    step(
        "O", "Observa", "OBSERVE",
        "¿Qué está pasando dentro y fuera de ti ahora mismo?",
        [],
    )
    # Table for O channels
    obs_data = [
        [Paragraph("<b>Canal</b>", body_style), Paragraph("<b>Preguntas guía</b>", body_style)],
        [Paragraph("Cuerpo", body_style), Paragraph("¿Dónde siento tensión? ¿Qué sensaciones físicas noto?", body_style)],
        [Paragraph("Emociones", body_style), Paragraph("¿Qué emoción está presente? ¿Intensidad (0-10)?", body_style)],
        [Paragraph("Pensamientos", body_style), Paragraph("¿Qué piensa mi mente? ¿Son hechos o interpretaciones?", body_style)],
    ]
    obs_tbl = Table(obs_data, colWidths=[26*mm, inner_w - 26*mm - 4*mm], hAlign="LEFT")
    obs_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.Color(0.15,0.15,0.15)),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("BACKGROUND", (0,1), (-1,1), colors.Color(0.93,0.93,0.93)),
        ("BACKGROUND", (0,2), (-1,2), colors.white),
        ("BACKGROUND", (0,3), (-1,3), colors.Color(0.93,0.93,0.93)),
        ("BOX", (0,0), (-1,-1), 0.5, colors.Color(0.6,0.6,0.6)),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.Color(0.7,0.7,0.7)),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(obs_tbl)
    story.append(Spacer(1, 1.5*mm))
    story.append(Paragraph(
        "Postura de testigo imparcial: observar sin identificarse ni suprimir. "
        "Nombrar la emoción internamente («noto que hay ansiedad»). "
        "Objetivo: distancia metacognitiva, defusión cognitiva incipiente.",
        note_style
    ))
    divider()

    # ── P ────────────────────────────────────────────────────────────────────
    step(
        "P", "Continúa con conciencia", "PROCEED",
        "Ahora, ¿qué quieres hacer? ¿Cuál es la respuesta más útil en este momento?",
        [
            "Retomar la actividad con mayor conciencia, o elegir una acción deliberada.",
            "Pregunta clave: «¿Qué haría la persona que quiero ser ahora?» (enlace con valores en ACT).",
            "Puede incluir: pedir tiempo, alejarse, comunicar la emoción, aplicar otra técnica.",
            "Objetivo: acción consciente vs. reacción automática.",
        ]
    )

    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=0.3, color=colors.Color(0.8,0.8,0.8)))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Basado en Mindfulness-Based Stress Reduction (MBSR) · Jon Kabat-Zinn", footer_style))

    doc.build(story)
    print(f"PDF generado: {OUTPUT}")


if __name__ == "__main__":
    build()
