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

OUTPUT = "/home/user/skillsfind/guia_ACCEPTS.pdf"
LOGO   = "/home/user/skillsfind/logo_luis_martinez_bw.png"

W, H   = A4
MARGIN = 14 * mm
INNER  = W - 2 * MARGIN

# ── Greyscale palette ─────────────────────────────────────────────────────────
BLACK    = colors.HexColor('#000000')
NEAR_BLK = colors.HexColor('#1A1A1A')
DARK     = colors.HexColor('#2E2E2E')
MID      = colors.HexColor('#555555')
GRAY60   = colors.HexColor('#666666')
GRAY80   = colors.HexColor('#CCCCCC')
GRAY90   = colors.HexColor('#E0E0E0')
GRAY95   = colors.HexColor('#F2F2F2')
WHITE    = colors.white


# ── Canvas ────────────────────────────────────────────────────────────────────
def draw_header_band(c, title, subtitle):
    c.setFillColor(NEAR_BLK)
    c.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)
    # thin rule below
    c.setFillColor(GRAY60)
    c.rect(0, H - 29.5*mm, W, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(W/2, H - 12*mm, title)
    c.setFont('Helvetica', 8.5)
    c.setFillColor(GRAY80)
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
        f'Técnica ACCEPTS · DBT (Linehan) · Uso clínico interno   |   pág. {pg}')

def page1_canvas(c, doc):
    draw_header_band(c,
        'GUÍA DE APLICACIÓN CLÍNICA — Técnica ACCEPTS',
        'Tolerancia al malestar · DBT (Dialectical Behavior Therapy) · Para uso del terapeuta en sesión')
    draw_footer(c, 1)

def page2_canvas(c, doc):
    draw_header_band(c,
        'Técnica ACCEPTS — continuación',
        'E · P · T · S')
    draw_footer(c, 2)


# ── Style helpers ─────────────────────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=DARK)
    base.update(kw); return ParagraphStyle(name, **base)

def sp(h=2): return Spacer(1, h*mm)


# ── Intro block ───────────────────────────────────────────────────────────────
INTRO = (
    'ACCEPTS es una habilidad de <b>tolerancia al malestar</b> de la DBT. '
    'Su función es ayudar al paciente a atravesar momentos de alta intensidad emocional '
    'sin llevar a cabo conductas dañinas, distrayendo la atención del malestar el tiempo '
    'suficiente para que la intensidad emocional disminuya por sí sola. '
    'No resuelve el problema de fondo ni elimina la emoción — '
    '<b>actúa en el intervalo entre el impulso y la conducta</b>, '
    'ampliando ese espacio para que el pico emocional baje.'
)
NOTE = (
    '<b>Nota clínica:</b> usar ACCEPTS no es evitar el problema, '
    'sino sobrevivir al momento de mayor intensidad para poder abordarlo '
    'después con más recursos.'
)

def build_intro():
    box = Table([[Paragraph(INTRO, S('i', fontSize=9, leading=13.5))]], colWidths=[INNER])
    box.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), GRAY95),
        ('LEFTPADDING',  (0,0),(-1,-1), 7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',   (0,0),(-1,-1), 5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LINEBELOW',    (0,0),(-1,-1), 1.5, NEAR_BLK),
    ]))
    note = Table([[Paragraph(NOTE, S('n', fontSize=8, leading=11.5, textColor=MID,
                                     fontName='Helvetica-Oblique'))]], colWidths=[INNER])
    note.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0),(-1,-1), 7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',   (0,0),(-1,-1), 4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LINEBEFORE',   (0,0),(0,-1),  3, GRAY60),
    ]))
    return [box, sp(1.5), note]


# ── Section builder ───────────────────────────────────────────────────────────
def section(letter, name_en, name_es, body, script, shade=False):
    bg = GRAY95 if shade else WHITE

    # Header: big letter + name
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

    # Body text
    body_cell = Table(
        [[Paragraph(body, S('bd', fontSize=8.5, leading=13, textColor=DARK))]],
        colWidths=[INNER]
    )
    body_cell.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), bg),
        ('LEFTPADDING',  (0,0),(-1,-1), 8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',   (0,0),(-1,-1), 5),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))

    # Guión box
    guion_label = Paragraph(
        '<b>Guión para el terapeuta:</b>',
        S('gl', fontSize=7.5, textColor=NEAR_BLK, leading=10, spaceAfter=1)
    )
    guion_text = Paragraph(
        f'<i>«{script}»</i>',
        S('gt', fontName='Helvetica-Oblique', fontSize=8, leading=12, textColor=MID, leftIndent=4)
    )
    guion_box = Table(
        [[guion_label], [guion_text]],
        colWidths=[INNER]
    )
    guion_box.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), GRAY90),
        ('LEFTPADDING',  (0,0),(-1,-1), 8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',   (0,0),(-1,-1), 4),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LINEBEFORE',   (0,0),(0,-1),  3, DARK),
        ('LINEBELOW',    (0,0),(-1,-1), 0.5, GRAY80),
    ]))

    return KeepTogether([hdr, body_cell, guion_box, sp(2.5)])


SECTIONS = [
    (
        'A', 'ACTIVITIES', 'Actividades',
        'Realizar cualquier actividad que requiera atención suficiente para competir con el pensamiento '
        'rumiativo o el impulso. La eficacia depende del grado de absorción que produce la actividad en '
        'ese paciente concreto. <b>En sesión se construye con el paciente una lista personalizada</b> — '
        'videojuegos, dibujo, música, lectura, series, ejercicio, cocinar — no una lista genérica.',
        'Cuando el malestar sea muy grande, no tienes que resolverlo ahora mismo. Solo tienes que '
        'hacer algo que ocupe tu cabeza el tiempo suficiente para que la ola de emoción baje. '
        'La emoción intensa siempre baja — nunca se queda al mismo nivel para siempre.',
        False
    ),
    (
        'C', 'CONTRIBUTING', 'Contribuir',
        'Realizar algo útil para otra persona o para algo más grande que uno mismo: ayudar a alguien, '
        'cuidar un animal, hacer algo por el entorno. Activa sistemas de afiliación y recompensa que '
        'contrarrestan el aislamiento y la desesperanza, desplazando el foco desde el dolor propio hacia '
        'el exterior. <b>No tiene que ser algo grande</b>: mandar un mensaje, dar de comer a un animal '
        'o hacer una tarea útil para el entorno inmediato son suficientes.',
        'Cuando estamos muy dentro de nuestro propio dolor, salir un momento hacia fuera — aunque sea '
        'hacer algo pequeño por alguien — puede cambiar algo en cómo nos sentimos. No porque el '
        'problema desaparezca, sino porque activa una parte diferente de nosotros.',
        True
    ),
    (
        'C', 'COMPARISONS', 'Comparaciones',
        'Ampliar temporalmente la perspectiva comparando la situación actual con momentos propios '
        'anteriores en los que el malestar era igual o mayor y se superó. El objetivo no es minimizar '
        'el dolor sino generar distancia cognitiva temporal. '
        '<b>Debe introducirse con cuidado</b> para evitar que se convierta en invalidación del dolor '
        'presente: el foco debe orientarse siempre hacia la propia historia de supervivencia del paciente.',
        'No estamos diciendo que tu dolor no sea real o que no importe. Estamos buscando un momento '
        'de perspectiva. ¿Ha habido momentos anteriores en los que sentiste algo parecido y lo '
        'atravesaste? ¿Qué te ayudó entonces?',
        False
    ),
    (
        'E', 'EMOTIONS', 'Emociones opuestas',
        'Generar intencionalmente una emoción diferente a la que está causando el malestar — '
        'no para suprimirla sino para crear un contrapeso temporal que reduzca su intensidad. '
        'Ver algo que provoque risa, escuchar música que genere otro estado, ver imágenes que activen '
        'ternura o admiración. <b>En sesión se identifica con el paciente qué contenido produce '
        'emociones distintas</b>, construyendo una lista de recursos personalizados de acceso rápido.',
        'No te estamos pidiendo que finjas sentirte bien. Te estamos pidiendo que expongas tu sistema '
        'emocional a algo diferente durante un rato, para que la emoción que te desborda tenga un poco '
        'menos de espacio. Es como abrir una ventana cuando hay demasiado humo.',
        True
    ),
    (
        'P', 'PUSH AWAY', 'Apartar',
        'Apartar temporalmente el pensamiento o la situación dolorosa de forma deliberada, '
        'con la intención explícita de volver a ello cuando haya más recursos disponibles. '
        'Se puede visualizar como poner el problema en una caja, en una estantería o detrás de '
        'una puerta. <b>Es fundamental dejar claro que apartar no es negar</b>: es una decisión '
        'activa y temporal de no procesar ese material ahora mismo.',
        'No estamos diciendo que el problema no existe. Estamos diciendo que ahora mismo no es '
        'el momento de mirarlo, porque tienes demasiada activación para hacerlo de forma segura. '
        'Lo guardamos por ahora y lo retomamos cuando estés en mejor disposición.',
        False
    ),
    (
        'T', 'THOUGHTS', 'Pensamientos',
        'Sustituir temporalmente los pensamientos rumiativos por otros que ocupen la mente de '
        'forma neutral, <b>sin combatir los pensamientos dolorosos directamente</b>. '
        'Contar hacia atrás desde cien de tres en tres, recitar letras de canciones conocidas, '
        'describir en detalle un lugar familiar, resolver mentalmente un problema sencillo. '
        'No se trata de pensamientos positivos forzados sino de competición atencional.',
        'No te pido que pienses en positivo ni que ignores lo que sientes. Te pido que des a '
        'tu mente otra tarea durante un rato. Algo que la mantenga ocupada — contar hacia atrás, '
        'recitar algo que te sepas de memoria, describir mentalmente un lugar que conozcas bien.',
        True
    ),
    (
        'S', 'SENSATIONS', 'Sensaciones',
        'Generar sensaciones físicas intensas pero inocuas que compitan con el malestar emocional: '
        'sostener hielo, masticar algo con sabor fuerte, oler algo intenso, ducharse con agua fría, '
        'escuchar música a volumen alto. '
        '<b>Especialmente relevante en pacientes con conductas autolesivas</b>: actúa sobre el mismo '
        'sistema de regulación que la autolesión — la necesidad de sensación física intensa — '
        'sin producir daño.',
        'A veces lo que el cuerpo busca es una sensación física fuerte que interrumpa el malestar '
        'emocional. Podemos darle eso de formas que no dañen. El hielo, el sabor intenso, la música '
        'fuerte producen una sensación real e intensa que cumple esa función sin dejar consecuencias.',
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

    # First 3 on page 1 (A, C, C), last 4 on page 2 (E, P, T, S)
    for i, (letter, name_en, name_es, body, script, shade) in enumerate(SECTIONS):
        if i == 3:
            story.append(NextPageTemplate('page2'))
            story.append(PageBreak())
        story.append(section(letter, name_en, name_es, body, script, shade))

    doc.build(story)
    print(f'PDF generado: {OUTPUT}')


if __name__ == '__main__':
    build()
