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
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/home/user/skillsfind/guia_TIPP.pdf"
LOGO   = "/home/user/skillsfind/logo_luis_martinez_bw.png"

W, H   = A4
MARGIN = 14 * mm
INNER  = W - 2 * MARGIN

# ── Greyscale palette ─────────────────────────────────────────────────────────
NEAR_BLK = colors.HexColor('#1A1A1A')
DARK     = colors.HexColor('#2E2E2E')
MID      = colors.HexColor('#555555')
GRAY60   = colors.HexColor('#666666')
GRAY80   = colors.HexColor('#CCCCCC')
GRAY88   = colors.HexColor('#E0E0E0')
GRAY95   = colors.HexColor('#F2F2F2')
WHITE    = colors.white


# ── Canvas ────────────────────────────────────────────────────────────────────
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
        f'Técnica TIPP · DBT (Linehan) · Uso clínico interno   |   pág. {pg}')

def page1_canvas(c, doc):
    draw_header(c,
        'GUÍA DE APLICACIÓN CLÍNICA — Técnica TIPP',
        'Regulación emocional fisiológica rápida · DBT · Para uso del terapeuta en sesión')
    draw_footer(c, 1)

def page2_canvas(c, doc):
    draw_header(c,
        'Técnica TIPP — continuación',
        'P · P')
    draw_footer(c, 2)


# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=DARK)
    base.update(kw); return ParagraphStyle(name, **base)

def sp(h=2): return Spacer(1, h*mm)

def mini_label(txt):
    return Paragraph(
        f'<font name="Helvetica-Bold" size="7" color="#666666">{txt.upper()}</font>',
        S('ml', textColor=GRAY60, leading=9, spaceAfter=1)
    )


# ── Intro ─────────────────────────────────────────────────────────────────────
INTRO = (
    'TIPP es un conjunto de cuatro estrategias de <b>regulación emocional rápida</b> '
    'desarrolladas por Marsha Linehan dentro de la DBT. Su objetivo es reducir la '
    'intensidad emocional extrema actuando directamente sobre la fisiología del paciente, '
    '<b>sin requerir capacidad reflexiva ni cognitiva para funcionar</b>. '
    'Es la habilidad de elección cuando la activación emocional es tan alta que el paciente '
    'no puede acceder a ninguna otra técnica.'
)

def build_intro():
    box = Table([[Paragraph(INTRO, S('i', fontSize=9, leading=13.5))]], colWidths=[INNER])
    box.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), GRAY95),
        ('LEFTPADDING',  (0,0),(-1,-1), 7), ('RIGHTPADDING', (0,0),(-1,-1), 7),
        ('TOPPADDING',   (0,0),(-1,-1), 5), ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LINEBELOW',    (0,0),(-1,-1), 1.5, NEAR_BLK),
    ]))
    return [box]


# ── Section builder ────────────────────────────────────────────────────────────
def section(letter, name_en, name_es, fisiologia, aplicacion, script,
            contraindication=None, shade=False):
    bg = GRAY95 if shade else WHITE

    # ── Header ──
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

    # ── Two-column body: base fisiológica | aplicación ──
    col_w = (INNER - 2*mm) / 2
    left_items = [
        mini_label('Base fisiológica'),
        Paragraph(fisiologia, S('fi', fontSize=8, leading=11.5, textColor=DARK)),
    ]
    right_items = [
        mini_label('Aplicación'),
        Paragraph(aplicacion, S('ap', fontSize=8, leading=11.5, textColor=DARK)),
    ]
    left_col  = Table([[i] for i in left_items],  colWidths=[col_w])
    right_col = Table([[i] for i in right_items], colWidths=[col_w])
    left_col.setStyle(TableStyle([
        ('TOPPADDING',  (0,0),(-1,-1), 1), ('BOTTOMPADDING',(0,0),(-1,-1), 1),
        ('LEFTPADDING', (0,0),(-1,-1), 0), ('RIGHTPADDING', (0,0),(-1,-1), 0),
    ]))
    right_col.setStyle(TableStyle([
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

    # ── Guión ──
    guion_label = Paragraph('<b>Guión para el terapeuta:</b>',
        S('gl', fontSize=7.5, textColor=NEAR_BLK, leading=10, spaceAfter=1))
    guion_text  = Paragraph(f'<i>«{script}»</i>',
        S('gt', fontName='Helvetica-Oblique', fontSize=8, leading=12,
          textColor=MID, leftIndent=4))
    guion_box = Table([[guion_label], [guion_text]], colWidths=[INNER])
    guion_box.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), GRAY88),
        ('LEFTPADDING',  (0,0),(-1,-1), 8), ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('TOPPADDING',   (0,0),(-1,-1), 4), ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LINEBEFORE',   (0,0),(0,-1),  3, DARK),
    ]))

    parts = [hdr, two_col, guion_box]

    # ── Contraindication / clinical note ──
    if contraindication:
        label_txt, note_txt = contraindication
        ci = Table([[
            Paragraph(f'<b>{label_txt}:</b> {note_txt}',
                      S('ci', fontSize=7.5, textColor=GRAY60,
                        fontName='Helvetica-Oblique', leading=10.5))
        ]], colWidths=[INNER])
        ci.setStyle(TableStyle([
            ('LEFTPADDING',  (0,0),(-1,-1), 8), ('RIGHTPADDING', (0,0),(-1,-1), 8),
            ('TOPPADDING',   (0,0),(-1,-1), 3), ('BOTTOMPADDING',(0,0),(-1,-1), 3),
            ('LINEBEFORE',   (0,0),(0,-1),  3, GRAY80),
        ]))
        parts.append(ci)

    parts.append(sp(3))
    return KeepTogether(parts)


SECTIONS = [
    (
        'T', 'TEMPERATURE', 'Temperatura',
        'El frío activa el reflejo de buceo de los mamíferos: respuesta autonómica que reduce '
        'la frecuencia cardíaca entre un 10 y un 25 % en segundos y disminuye la activación '
        'del sistema nervioso simpático de forma inmediata.',
        'Sumergir la cara en agua fría 15-30 segundos, o sostener hielo en manos o muñecas. '
        'Sin acceso a agua: bolsa fría, lata fría o agua fría en la nuca. '
        'El agua debe ser fría pero no causar dolor.',
        'Cuando la emoción sea tan intensa que no puedas pensar con claridad, el frío le dice '
        'a tu cuerpo que se calme sin que tengas que hacer nada mental. No necesitas creerlo '
        'ni entenderlo — es una respuesta automática de tu sistema nervioso.',
        ('Contraindicaciones',
         'Trastornos cardiovasculares que contraindiquen cambios bruscos de temperatura. '
         'Consultar con el equipo médico en caso de duda.'),
        False
    ),
    (
        'I', 'INTENSE EXERCISE', 'Ejercicio intenso',
        'La activación emocional extrema genera preparación corporal para luchar o huir. '
        'Si no encuentra salida, el sistema nervioso permanece en alarma. '
        'El ejercicio intenso breve metaboliza esa activación completando el ciclo de respuesta de estrés.',
        'Dos minutos de alta intensidad son suficientes: correr en el sitio, sentadillas, '
        'saltos, subir y bajar escaleras o flexiones. '
        'La intensidad es el factor determinante — la actividad moderada no produce el mismo efecto.',
        'Tu cuerpo está preparado para correr o pelear aunque no haya ningún peligro real. '
        'Si le damos esa salida física durante dos minutos, la alarma se apaga sola. '
        'No tienes que entender por qué funciona — solo probar.',
        ('Contraindicaciones',
         'Lesiones físicas activas o condiciones médicas que limiten el ejercicio intenso. '
         'Adaptar la actividad al estado físico del paciente.'),
        True
    ),
    (
        'P', 'PACED BREATHING', 'Respiración acompasada',
        'Exhalar más lento que inhalar activa el nervio vago y el sistema nervioso parasimpático, '
        'produciendo reducción real de la frecuencia cardíaca y de la activación simpática. '
        'No es relajación sugestiva — es regulación autonómica directa.',
        'Inhalar 4 segundos · exhalar 6-8 segundos. Repetir 2-3 minutos. '
        'La exhalación debe ser siempre más larga — ese es el mecanismo activo. '
        'Si el paciente no puede contar: exhalar como si soplara una vela muy despacio sin apagarla.',
        'No tienes que vaciar los pulmones ni hacer nada especial. Solo deja que el aire salga '
        'más despacio de lo que entró. Tu sistema nervioso hace el resto de forma automática.',
        ('Consideración clínica',
         'En pánico o hipocondría la atención a la respiración puede aumentar la ansiedad. '
         'Introducir con ojos abiertos orientados al exterior, o sustituir temporalmente por temperatura.'),
        False
    ),
    (
        'P', 'PROGRESSIVE RELAXATION', 'Relajación progresiva',
        'La tensión muscular crónica es una respuesta somática frecuente en alta activación sostenida. '
        'La tensión y liberación muscular consciente interrumpe ese patrón y devuelve al sistema '
        'nervioso información de seguridad desde el cuerpo.',
        'Tensar cada grupo muscular 5 segundos y soltar 10, atendiendo al contraste. '
        'Versión breve (4 grupos): manos, brazos, abdomen, piernas — menos de 5 minutos. '
        'Versión completa: 8-16 grupos según protocolo de Jacobson.',
        'Vamos a tensar y soltar grupos de músculos. Primero aprieta los puños todo lo que puedas '
        'durante cinco segundos. Ahora suelta completamente y nota la diferencia. '
        'Tu cuerpo aprende así cómo se siente realmente relajado, y ese contraste es el que produce el efecto.',
        ('Consideración clínica',
         'En trauma corporal o disociación somática, empezar por extremidades distales '
         '(manos y pies) antes de zonas centrales. Preguntar qué zonas se sienten seguras para trabajar.'),
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
