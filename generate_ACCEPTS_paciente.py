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

OUTPUT = "/home/user/skillsfind/ACCEPTS_paciente.pdf"
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
        f'Técnica ACCEPTS · DBT (Linehan)   |   pág. {pg}')

def page1_canvas(c, doc):
    draw_header(c, 'Técnica ACCEPTS',
        'Qué hacer cuando el malestar es muy intenso')
    draw_footer(c, 1)

def page2_canvas(c, doc):
    draw_header(c, 'Técnica ACCEPTS — continuación', 'E · P · T · S')
    draw_footer(c, 2)


def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=9, leading=13, textColor=DARK)
    base.update(kw); return ParagraphStyle(name, **base)

def sp(h=2): return Spacer(1, h*mm)


INTRO = (
    'ACCEPTS es una técnica para ayudarte a atravesar momentos de malestar muy intenso '
    'sin hacer algo que luego puedas lamentar. '
    'No elimina el problema ni la emoción — '
    '<b>crea el espacio suficiente para que la intensidad baje por sí sola</b>, '
    'y así poder abordarlo después con más calma y más recursos.'
)
NOTE = (
    '<b>Recuerda:</b> usar ACCEPTS no es evitar el problema. '
    'Es sobrevivir al momento más difícil para poder afrontarlo después en mejores condiciones.'
)

def build_intro():
    box = Table([[Paragraph(INTRO, S('i'))]], colWidths=[INNER])
    box.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), GRAY95),
        ('LEFTPADDING',  (0,0),(-1,-1), 7), ('RIGHTPADDING', (0,0),(-1,-1), 7),
        ('TOPPADDING',   (0,0),(-1,-1), 6), ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LINEBELOW',    (0,0),(-1,-1), 1.5, NEAR_BLK),
    ]))
    note = Table([[Paragraph(NOTE, S('n', fontSize=8.5, textColor=MID,
                                     fontName='Helvetica-Oblique', leading=12))]], colWidths=[INNER])
    note.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0),(-1,-1), 7), ('RIGHTPADDING', (0,0),(-1,-1), 7),
        ('TOPPADDING',   (0,0),(-1,-1), 4), ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ('LINEBEFORE',   (0,0),(0,-1),  3, GRAY60),
    ]))
    return [box, sp(1.5), note]


def section(letter, name_en, name_es, body, tip, shade=False):
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

    body_cell = Table([[Paragraph(body, S('bd', leading=13))]], colWidths=[INNER])
    body_cell.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), bg),
        ('LEFTPADDING',  (0,0),(-1,-1), 8), ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('TOPPADDING',   (0,0),(-1,-1), 5), ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ]))

    tip_cell = Table([[Paragraph(
        f'<b>Ejemplos:</b> {tip}',
        S('ti', fontSize=8, leading=11.5, textColor=MID, fontName='Helvetica-Oblique')
    )]], colWidths=[INNER])
    tip_cell.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), GRAY88),
        ('LEFTPADDING',  (0,0),(-1,-1), 8), ('RIGHTPADDING', (0,0),(-1,-1), 8),
        ('TOPPADDING',   (0,0),(-1,-1), 4), ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LINEBEFORE',   (0,0),(0,-1),  3, DARK),
    ]))

    return KeepTogether([hdr, body_cell, tip_cell, sp(2.5)])


SECTIONS = [
    (
        'A', 'ACTIVITIES', 'Actividades',
        'Haz algo que ocupe tu cabeza lo suficiente para que la emoción intensa baje. '
        'No tienes que resolver nada ahora. La emoción intensa <b>siempre baja</b> — '
        'nunca se queda al mismo nivel para siempre. '
        'La clave es elegir algo que realmente absorba tu atención, '
        'no algo que hagas por encima mientras sigues rumiando.',
        'Videojuegos, dibujo, música, lectura, series, ejercicio, cocinar, manualidades — '
        'lo que de verdad ocupe tu mente.',
        False
    ),
    (
        'C', 'CONTRIBUTING', 'Contribuir',
        'Haz algo útil para otra persona o para algo más grande que tú. '
        'Salir un momento del propio dolor hacia el exterior '
        'activa una parte diferente de ti y puede cambiar algo en cómo te sientes. '
        '<b>No tiene que ser algo grande.</b>',
        'Mandar un mensaje de ánimo, dar de comer a un animal, ordenar algo para alguien, '
        'hacer una tarea útil para tu entorno.',
        True
    ),
    (
        'C', 'COMPARISONS', 'Comparaciones',
        'Busca un momento de perspectiva: recuerda situaciones anteriores en las que sentiste '
        'algo parecido de intenso y lo atravesaste. '
        'No estamos minimizando tu dolor — '
        '<b>estamos buscando evidencia de tu propia capacidad de supervivencia.</b>',
        '¿Ha habido momentos anteriores así? ¿Qué te ayudó entonces? '
        '¿Qué hiciste para salir adelante?',
        False
    ),
    (
        'E', 'EMOTIONS', 'Emociones opuestas',
        'Expón tu sistema emocional a algo diferente durante un rato — '
        'no para fingir que estás bien, sino para que la emoción que te desborda '
        '<b>tenga un poco menos de espacio</b>. '
        'Es como abrir una ventana cuando hay demasiado humo.',
        'Vídeos que te provoquen risa o ternura, música que cambie tu estado, '
        'imágenes que activen curiosidad o admiración.',
        True
    ),
    (
        'P', 'PUSH AWAY', 'Apartar',
        'Toma la decisión <b>activa y temporal</b> de no pensar en el problema ahora mismo. '
        'No es negarlo ni ignorarlo — es reconocer que en este momento '
        'tienes demasiada activación para abordarlo de forma segura. '
        'Lo guardas, sabiendo que sigue ahí, y lo retomas cuando estés en mejor disposición.',
        'Visualiza que metes el problema en una caja con cierre, en una estantería '
        'o detrás de una puerta. Siempre puedes volver a él.',
        False
    ),
    (
        'T', 'THOUGHTS', 'Pensamientos',
        'Dale a tu mente otra tarea durante un rato. No pensamientos positivos forzados — '
        'simplemente algo que <b>ocupe el espacio cognitivo</b> y reduzca la rumiación '
        'por competición: dos procesos no pueden ocupar el mismo espacio mental a la vez.',
        'Contar hacia atrás desde 100 de 3 en 3 · recitar letras de canciones · '
        'describir mentalmente un lugar familiar con todo el detalle posible.',
        True
    ),
    (
        'S', 'SENSATIONS', 'Sensaciones',
        'Genera una sensación física intensa pero inocua que compita con el malestar '
        'y ancle tu atención al presente. '
        'Especialmente útil si sientes el impulso de hacerte daño: '
        '<b>actúa sobre el mismo sistema sin producir daño.</b>',
        'Sostener hielo · masticar algo con sabor fuerte (chile, limón) · '
        'oler algo muy intenso · ducha de agua fría o caliente · '
        'música a volumen alto con auriculares.',
        False
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
    story.append(Paragraph('LAS SIETE ESTRATEGIAS', s_sec))
    story.append(HRFlowable(width='100%', thickness=1, color=NEAR_BLK,
                             spaceAfter=3, spaceBefore=1))

    for i, args in enumerate(SECTIONS):
        if i == 4:
            story.append(NextPageTemplate('page2'))
            story.append(PageBreak())
        story.append(section(*args))

    doc.build(story)
    print(f'PDF generado: {OUTPUT}')


if __name__ == '__main__':
    build()
