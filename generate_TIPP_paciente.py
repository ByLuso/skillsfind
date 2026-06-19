from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, NextPageTemplate, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

OUTPUT = "/home/user/skillsfind/TIPP_paciente.pdf"
LOGO   = "/home/user/skillsfind/logo_luis_martinez_bw.png"

W, H   = A4
MARGIN = 14 * mm
INNER  = W - 2 * MARGIN

NEAR_BLK = colors.HexColor('#1A1A1A')
DARK     = colors.HexColor('#2E2E2E')
MID      = colors.HexColor('#555555')
GRAY60   = colors.HexColor('#666666')
GRAY80   = colors.HexColor('#CCCCCC')
GRAY88   = colors.HexColor('#E0E0E0')
GRAY95   = colors.HexColor('#F2F2F2')
WHITE    = colors.white


def draw_header(c, title, subtitle):
    c.setFillColor(NEAR_BLK)
    c.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)
    c.setFillColor(GRAY60)
    c.rect(0, H - 29.5*mm, W, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(W/2, H - 12*mm, title)
    c.setFont('Helvetica', 8.5); c.setFillColor(GRAY80)
    c.drawCentredString(W/2, H - 20*mm, subtitle)

def draw_footer(c, pg):
    try:
        logo = ImageReader(LOGO)
        c.drawImage(logo, MARGIN, 4*mm, width=46*mm, height=11*mm,
                    mask='auto', preserveAspectRatio=True, anchor='sw')
    except Exception:
        c.setFillColor(NEAR_BLK); c.setFont('Helvetica-Bold', 7)
        c.drawString(MARGIN, 9*mm, 'Luis Martínez · Enfermero')
    c.setFillColor(GRAY60); c.setFont('Helvetica', 6.5)
    c.drawRightString(W - MARGIN, 7*mm,
        f'Técnica TIPP · DBT (Linehan)   |   pág. {pg}')

def page1_canvas(c, doc):
    draw_header(c, 'Técnica TIPP',
        'Cómo calmar la emoción muy intensa actuando sobre tu cuerpo')
    draw_footer(c, 1)

def page2_canvas(c, doc):
    draw_header(c, 'Técnica TIPP — continuación', 'P · P')
    draw_footer(c, 2)


def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=9, leading=13, textColor=DARK)
    base.update(kw); return ParagraphStyle(name, **base)

def sp(h=2): return Spacer(1, h*mm)


INTRO = (
    'TIPP es una técnica para bajar la intensidad emocional muy rápido '
    'actuando directamente sobre tu cuerpo. '
    '<b>No necesitas pensar ni razonar para que funcione</b> — '
    'trabaja sobre tu sistema nervioso de forma automática. '
    'Es la técnica para cuando estás tan desbordado que no puedes hacer ninguna otra cosa.'
)

def build_intro():
    box = Table([[Paragraph(INTRO, S('i'))]], colWidths=[INNER])
    box.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), GRAY95),
        ('LEFTPADDING',  (0,0),(-1,-1), 7), ('RIGHTPADDING', (0,0),(-1,-1), 7),
        ('TOPPADDING',   (0,0),(-1,-1), 6), ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LINEBELOW',    (0,0),(-1,-1), 1.5, NEAR_BLK),
    ]))
    return [box]


def section(letter, name_en, name_es, why, how, warning=None, shade=False):
    bg = GRAY95 if shade else WHITE

    badge = Paragraph(
        f'<font name="Helvetica-Bold" size="24" color="white">{letter}</font>',
        S('ba', alignment=TA_CENTER, leading=28)
    )
    titles = [
        Paragraph(f'<font name="Helvetica-Bold" size="11" color="white">{name_en}</font>',
                  S('te', textColor=WHITE, leading=13)),
        Paragraph(f'<font size="8.5" color="#CCCCCC">{name_es}</font>',
                  S('ts', textColor=GRAY80, leading=10)),
    ]
    hdr = Table([[badge, titles]], colWidths=[13*mm, INNER - 13*mm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), NEAR_BLK),
        ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ('LEFTPADDING',  (0,0),(0,0),   3),
        ('LEFTPADDING',  (1,0),(1,0),   6),
        ('TOPPADDING',   (0,0),(-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ]))

    # Two-column: Por qué funciona | Cómo hacerlo
    col_w = (INNER - 2*mm) / 2

    def mini_label(txt):
        return Paragraph(
            f'<font name="Helvetica-Bold" size="7" color="#666666">{txt.upper()}</font>',
            S('ml', textColor=GRAY60, leading=9, spaceAfter=1)
        )

    left_col  = Table([[mini_label('Por qué funciona')],
                        [Paragraph(why, S('wy', fontSize=8, leading=11.5))]], colWidths=[col_w])
    right_col = Table([[mini_label('Cómo hacerlo')],
                        [Paragraph(how, S('hw', fontSize=8, leading=11.5))]], colWidths=[col_w])
    for tbl in (left_col, right_col):
        tbl.setStyle(TableStyle([
            ('TOPPADDING',  (0,0),(-1,-1), 1), ('BOTTOMPADDING',(0,0),(-1,-1), 1),
            ('LEFTPADDING', (0,0),(-1,-1), 0), ('RIGHTPADDING', (0,0),(-1,-1), 0),
        ]))

    two_col = Table([[left_col, right_col]], colWidths=[col_w, col_w])
    two_col.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), bg),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0),(-1,-1), 7), ('RIGHTPADDING', (0,0),(-1,-1), 7),
        ('TOPPADDING',   (0,0),(-1,-1), 5), ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LINEBEFORE',   (1,0),(1,-1),  0.5, GRAY80),
    ]))

    parts = [hdr, two_col]

    if warning:
        wi = Table([[Paragraph(
            f'<b>Ten en cuenta:</b> {warning}',
            S('wa', fontSize=7.5, textColor=MID, fontName='Helvetica-Oblique', leading=10.5)
        )]], colWidths=[INNER])
        wi.setStyle(TableStyle([
            ('LEFTPADDING',  (0,0),(-1,-1), 8), ('RIGHTPADDING', (0,0),(-1,-1), 8),
            ('TOPPADDING',   (0,0),(-1,-1), 3), ('BOTTOMPADDING',(0,0),(-1,-1), 3),
            ('LINEBEFORE',   (0,0),(0,-1),  3, GRAY80),
        ]))
        parts.append(wi)

    parts.append(sp(3))
    return KeepTogether(parts)


SECTIONS = [
    (
        'T', 'TEMPERATURE', 'Temperatura',
        'El frío activa una respuesta automática de tu sistema nervioso que reduce '
        'la frecuencia cardíaca entre un 10 y un 25 % en segundos. '
        'No tienes que creerlo ni entenderlo para que funcione.',
        'Sumerge la cara en agua fría 15-30 segundos, o sostén hielo en las manos. '
        'Sin acceso a agua: una lata fría o agua fría en la nuca o las muñecas. '
        '<b>Frío, pero no doloroso.</b>',
        'Consulta a tu médico si tienes problemas cardíacos antes de usar esta técnica.',
        False
    ),
    (
        'I', 'INTENSE EXERCISE', 'Ejercicio intenso',
        'Cuando estás muy activado, tu cuerpo está preparado para correr o pelear. '
        'El ejercicio intenso breve <b>completa ese ciclo</b> y la alarma se apaga sola.',
        'Dos minutos de alta intensidad: correr en el sitio, sentadillas, saltos, '
        'subir y bajar escaleras o flexiones. '
        '<b>La intensidad es lo que importa</b>, no la duración.',
        'Si tienes alguna lesión o condición médica, adapta la actividad '
        'a lo que tu cuerpo pueda hacer sin riesgo.',
        True
    ),
    (
        'P', 'PACED BREATHING', 'Respiración acompasada',
        'Exhalar más despacio que inhalar activa el nervio vago, '
        'que le dice a tu sistema nervioso que puede calmarse. '
        'No es sugestión — es regulación directa.',
        'Inhala 4 segundos · exhala 6-8 segundos. Repite 2-3 minutos. '
        'Si no puedes contar: exhala como si soplaras una vela muy despacio '
        'sin llegar a apagarla. '
        '<b>La clave es que la salida sea siempre más lenta que la entrada.</b>',
        'Si notas que prestar atención a la respiración te genera más ansiedad, '
        'pasa directamente a la estrategia de temperatura o de ejercicio.',
        False
    ),
    (
        'P', 'PROGRESSIVE RELAXATION', 'Relajación progresiva',
        'La tensión muscular sostenida mantiene a tu cuerpo en alerta. '
        'Tensar y soltar conscientemente interrumpe ese patrón y '
        'le envía a tu sistema nervioso una señal de seguridad.',
        'Aprieta un grupo muscular 5 segundos · suelta 10 segundos · '
        'nota el contraste. '
        'Versión rápida: manos → brazos → abdomen → piernas. '
        '<b>El efecto viene del contraste entre tensión y liberación.</b>',
        'Si hay zonas de tu cuerpo que se sienten incómodas o inseguras para trabajar, '
        'empieza solo por manos y pies, y avanza cuando te sientas listo.',
        True
    ),
]


def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 32*mm, bottomMargin=MARGIN + 10*mm,
    )
    f1 = Frame(doc.leftMargin, doc.bottomMargin,
               INNER, H - doc.topMargin - doc.bottomMargin, id='p1')
    f2 = Frame(MARGIN, MARGIN + 8*mm,
               INNER, H - MARGIN - 32*mm - MARGIN - 8*mm, id='p2')
    doc.addPageTemplates([
        PageTemplate(id='page1', frames=[f1], onPage=page1_canvas),
        PageTemplate(id='page2', frames=[f2], onPage=page2_canvas),
    ])

    s_sec = S('sec', fontName='Helvetica-Bold', fontSize=9, textColor=NEAR_BLK,
              leading=12, spaceAfter=2)

    story = []
    story += build_intro()
    story.append(sp(3))
    story.append(Paragraph('LAS CUATRO ESTRATEGIAS', s_sec))
    story.append(HRFlowable(width='100%', thickness=1, color=NEAR_BLK,
                             spaceAfter=3, spaceBefore=1))

    for i, args in enumerate(SECTIONS):
        if i == 2:
            story.append(NextPageTemplate('page2'))
            story.append(PageBreak())
        story.append(section(*args))

    doc.build(story)
    print(f'PDF generado: {OUTPUT}')


if __name__ == '__main__':
    build()
