from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, NextPageTemplate, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/home/user/skillsfind/guia_clinica_grounding.pdf"
LOGO   = "/home/user/skillsfind/logo_luis_martinez.png"

W, H   = A4
MARGIN = 14 * mm
INNER  = W - 2 * MARGIN

# ── Palette ──────────────────────────────────────────────────────────────────
DARK_BLUE  = colors.HexColor('#002D5F')
MED_BLUE   = colors.HexColor('#1565C0')
LIGHT_BLUE = colors.HexColor('#EBF3FB')
TEAL       = colors.HexColor('#00695C')
TEAL_L     = colors.HexColor('#E0F5F1')
PURPLE     = colors.HexColor('#5C3D8F')
PURPLE_L   = colors.HexColor('#F0EBF8')
INDIGO     = colors.HexColor('#283593')
INDIGO_L   = colors.HexColor('#E8EAF6')
BLUE_GREY  = colors.HexColor('#37474F')
DARK_RED   = colors.HexColor('#B71C1C')
LIGHT_RED  = colors.HexColor('#FDECEA')
GRAY_M     = colors.HexColor('#90A4AE')
GRAY_L     = colors.HexColor('#F4F6F8')
WHITE      = colors.white
BLACK      = colors.black

# Sense step colours (5→1, distinct but healthcare palette)
STEP_COLS = [
    (colors.HexColor('#01579B'), colors.HexColor('#E3F2FD')),  # 5 Vista — deep blue
    (colors.HexColor('#00695C'), colors.HexColor('#E0F5F1')),  # 4 Tacto — teal
    (colors.HexColor('#4527A0'), colors.HexColor('#EDE7F6')),  # 3 Oído  — purple
    (colors.HexColor('#1B5E20'), colors.HexColor('#E8F5E9')),  # 2 Olfato — green
    (colors.HexColor('#BF360C'), colors.HexColor('#FBE9E7')),  # 1 Gusto  — deep orange
]


# ── Canvas decorators ─────────────────────────────────────────────────────────
def _logo_footer(c, pg):
    try:
        logo = ImageReader(LOGO)
        c.drawImage(logo, MARGIN, 4*mm, width=46*mm, height=11*mm,
                    mask='auto', preserveAspectRatio=True, anchor='sw')
    except Exception:
        c.setFillColor(DARK_BLUE); c.setFont('Helvetica-Bold', 7)
        c.drawString(MARGIN, 9*mm, 'Luis Martínez · Enfermero')
    c.setFillColor(GRAY_M); c.setFont('Helvetica', 6.5)
    c.drawRightString(W - MARGIN, 7*mm,
        f'Técnica Grounding 5-4-3-2-1 · Uso clínico interno   |   pág. {pg}')

def page1_canvas(c, doc):
    c.setFillColor(DARK_BLUE)
    c.rect(0, H - 30*mm, W, 30*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 32*mm, W, 2*mm, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 15)
    c.drawCentredString(W/2, H - 13*mm, 'GUÍA DE APLICACIÓN CLÍNICA — Técnica Grounding 5-4-3-2-1')
    c.setFont('Helvetica', 9)
    c.setFillColor(colors.HexColor('#AECBF0'))
    c.drawCentredString(W/2, H - 21*mm, 'Anclaje sensorial al momento presente · Para uso del terapeuta en sesión')
    _logo_footer(c, 1)

def page2_canvas(c, doc):
    c.setFillColor(DARK_BLUE)
    c.rect(0, H - 16*mm, W, 16*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 18*mm, W, 2*mm, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(W/2, H - 11*mm, 'Grounding 5-4-3-2-1 — Resolución de Dificultades')
    _logo_footer(c, 2)


# ── Style helper ──────────────────────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=8.5, leading=12, textColor=BLUE_GREY)
    base.update(kw); return ParagraphStyle(name, **base)

def sp(h=2): return Spacer(1, h*mm)
def hr(col=GRAY_M, t=0.4): return HRFlowable(width='100%', thickness=t, color=col,
                                               spaceAfter=2, spaceBefore=2)


# ── Page 1 content ────────────────────────────────────────────────────────────
def build_intro():
    text = (
        'El grounding sensorial 5-4-3-2-1 ancla al paciente al momento presente '
        'redirigiendo la atención desde el mundo interno (pensamientos, recuerdos, '
        'sensaciones amenazantes) hacia el entorno externo seguro y concreto. '
        'Interrumpe estados de hiperactivación, disociación leve-moderada y desbordamiento emocional.'
    )
    cuando = (
        '<b>Indicaciones:</b> '
        'Crisis de ansiedad · Flashbacks iniciales · Disociación leve · Pánico · '
        'Desbordamiento emocional agudo'
    )
    box = Table([[Paragraph(text, S('i', fontSize=9, leading=13))]], colWidths=[INNER])
    box.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), LIGHT_BLUE),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING', (0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LINEBELOW',  (0,0),(-1,-1),1.5, TEAL),
    ]))
    caja = Table([[Paragraph(cuando, S('c', fontSize=7.5, textColor=BLUE_GREY, leading=11))]],
                 colWidths=[INNER])
    caja.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), GRAY_L),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING', (0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    return [box, sp(1), caja]


SENSES = [
    (5, 'VISTA',   'Ve',  'Mira a tu alrededor y nombra cinco cosas que puedas ver ahora mismo. '
                          'No tiene que ser nada importante — una silla, una ventana, el color de la pared.'),
    (4, 'TACTO',   'Toca','Cuatro cosas que puedas tocar. Nota la textura de tu ropa, el asiento, '
                          'tus propias manos. Nota cómo se siente cada superficie.'),
    (3, 'OÍDO',    'Oye', 'Tres sonidos que puedas escuchar ahora. Cercanos o lejanos — '
                          'el aire, voces fuera, tu propia respiración.'),
    (2, 'OLFATO',  'Huele','Dos cosas que puedas oler. Si no percibes nada claro, simplemente '
                          'inhala y nota el aire tal como es.'),
    (1, 'GUSTO',   'Saborea','Una cosa que puedas saborear ahora mismo — '
                          'el sabor que tienes en la boca en este momento.'),
]

CLOSING = (
    '<b>Cierre:</b> «¿Dónde estás? ¿Qué año es? ¿Estás a salvo en este momento?» '
    '— Esta verificación final consolida el retorno al presente.'
)


def build_senses():
    result = []
    for i, (num, sense, verb, script) in enumerate(SENSES):
        col, light = STEP_COLS[i]

        # Number badge + sense name
        badge = Paragraph(
            f'<font name="Helvetica-Bold" size="26" color="white">{num}</font>',
            S('b', alignment=TA_CENTER, leading=30)
        )
        title_lines = [
            Paragraph(f'<font name="Helvetica-Bold" size="11" color="white">{sense}</font>',
                      S('sn', textColor=WHITE, leading=13)),
            Paragraph(f'<font size="8.5" color="#DDEEFF">{verb}</font>',
                      S('sv', textColor=WHITE, leading=11)),
        ]
        hdr = Table([[badge, title_lines]], colWidths=[13*mm, INNER - 13*mm])
        hdr.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), col),
            ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
            ('LEFTPADDING',  (0,0),(0,0),   3),
            ('LEFTPADDING',  (1,0),(1,0),   6),
            ('TOPPADDING',   (0,0),(-1,-1), 4),
            ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ]))

        # Script
        body = Table(
            [[Paragraph(f'«{script}»',
                        S('sc', fontName='Helvetica-Oblique', fontSize=8.5,
                          leading=12.5, textColor=BLUE_GREY, leftIndent=4))]],
            colWidths=[INNER]
        )
        body.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), light),
            ('LEFTPADDING',  (0,0),(-1,-1), 8),('RIGHTPADDING',(0,0),(-1,-1),8),
            ('TOPPADDING',   (0,0),(-1,-1), 4),('BOTTOMPADDING',(0,0),(-1,-1),5),
            ('LINEBELOW',    (0,0),(-1,-1), 1.5, col),
        ]))

        result.append(KeepTogether([hdr, body, sp(2)]))

    # Closing verification
    closing = Table([[Paragraph(CLOSING, S('cl', fontSize=8, leading=12, textColor=DARK_BLUE))]],
                    colWidths=[INNER])
    closing.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), LIGHT_BLUE),
        ('LEFTPADDING',  (0,0),(-1,-1), 8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',   (0,0),(-1,-1), 5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('BOX',          (0,0),(-1,-1), 1, MED_BLUE),
    ]))
    result.append(closing)
    return result


# ── Page 2 content ─────────────────────────────────────────────────────────────
PROBLEMS = [
    {
        'n': '1', 'title': 'Se desconecta más — la técnica aumenta la disociación',
        'why': 'En trauma complejo o disociación estructural, focalizar la atención puede profundizar la desconexión si no hay suficiente base de seguridad.',
        'actions': [
            'Añadir estímulo físico intenso previo: «Apoya los dos pies en el suelo, nota el peso, aprieta las manos 3 segundos y suelta.»',
            'Usar temperatura como ancla: sostener un vaso de agua fría o poner las manos bajo agua fría.',
            'Añadir movimiento orientativo: girar la cabeza lentamente mirando la sala como si fuera la primera vez.',
            'Reducir a dos o tres sentidos (empezando siempre por tacto y vista).',
        ]
    },
    {
        'n': '2', 'title': 'La ansiedad aumenta al focalizar la atención',
        'why': 'En hipervigilancia o pánico, «prestar atención» se interpreta como señal de peligro, disparando más activación.',
        'actions': [
            'Dirigir la atención exclusivamente hacia el exterior, evitando sensaciones internas: «Solo mira la sala conmigo. ¿Qué ves?»',
            'Usar un objeto concreto como ancla principal: describir color, forma, sombra, brillo.',
            'Introducir movimiento suave primero: caminar tres pasos, sentir el suelo y volver a sentarse.',
        ]
    },
    {
        'n': '3', 'title': 'Se bloquea, no puede nombrar nada',
        'why': 'La activación muy alta estrecha el campo atencional; el paciente no puede generar respuestas verbales.',
        'actions': [
            'El terapeuta lidera activamente: «Mira — esa lámpara. ¿La ves tú también? Bien. Ahora esa ventana.»',
            'Eliminar la necesidad de contar: «No hace falta llegar a cinco. Dime solo una cosa que veas.»',
            'Usar contacto físico si hay permiso explícito previo: «¿Puedo ponerte la mano en el hombro? Nota ese peso.»',
        ]
    },
    {
        'n': '4', 'title': 'Lo hace mecánicamente, sin efecto real',
        'why': 'El paciente ejecuta la técnica de forma automática sin anclar realmente la atención; se convierte en un ritual vacío.',
        'actions': [
            'Añadir curiosidad genuina: «No me digas el nombre. Descríbemelo como si yo no pudiera verlo.»',
            'Pedir detalle sensorial real en lugar de etiquetas: color exacto, temperatura al tacto, dureza.',
            'Introducir novedad: «Busca algo en esta sala que nunca hayas mirado de verdad antes.»',
            'Alterar el orden de los sentidos para romper la automatización.',
        ]
    },
    {
        'n': '5', 'title': 'Le parece artificial o infantil, no se engancha',
        'why': 'Alta capacidad intelectual, desconfianza hacia técnicas psicológicas o adolescentes: la brecha con el autoconcepto genera resistencia.',
        'actions': [
            'Reformular en lenguaje neurocientífico: la técnica activa el córtex prefrontal e inhibe la amígdala, recuperando capacidad de pensar.',
            'Ofrecer como experimento sin expectativas: «Solo pruébalo una vez y cuéntame qué notaste.»',
            'Adaptar el lenguaje: «Vamos a hacer un escaneo sensorial del entorno.»',
        ]
    },
    {
        'n': '6', 'title': 'Funciona en sesión pero no en casa o en crisis real',
        'why': 'La activación en contexto real supera a la de sesión; la técnica no está automatizada para competir con la respuesta de estrés agudo.',
        'actions': [
            'Practicar en sesión con activación progresiva real, no solo en calma.',
            'Crear tarjeta física plastificada (5 pasos) que el paciente lleve siempre encima.',
            'Establecer un disparador corporal personalizado: la primera señal de activación = sacar la tarjeta.',
            'Versión de emergencia (30 seg): mira 3 cosas · toca 2 · respira 1.',
        ]
    },
]

SUMMARY = [
    ['Dificultad', 'Adaptación clave'],
    ['Mayor disociación',        'Estímulo físico intenso previo + reducir sentidos'],
    ['Ansiedad aumenta',         'Solo exterior + objeto concreto + movimiento suave'],
    ['Bloqueo sin respuesta',    'Terapeuta lidera + reducir demanda a 1 elemento'],
    ['Ejecución mecánica',       'Detalle sensorial + novedad + variar orden'],
    ['Resistencia / no se cree', 'Marco neurocientífico + enfoque experimental'],
    ['No funciona en casa',      'Tarjeta física + disparador corporal + versión 30 seg'],
]


def build_problems():
    s_why    = S('wy', fontSize=7.5, textColor=BLUE_GREY, leading=10.5,
                 fontName='Helvetica-Oblique', leftIndent=4)
    s_bullet = S('bu', fontSize=7.5, textColor=BLUE_GREY, leading=10.5, leftIndent=8)
    s_qh     = S('qh', fontSize=7.5, textColor=DARK_RED,
                 fontName='Helvetica-Bold', leading=10, leftIndent=4)

    result = []
    for p in PROBLEMS:
        hdr = Table([[
            Paragraph(f'<font name="Helvetica-Bold" size="10" color="white">P{p["n"]}</font>',
                      S('ph', alignment=TA_CENTER, leading=12)),
            Paragraph(f'<font name="Helvetica-Bold" size="8.5" color="white">{p["title"]}</font>',
                      S('pt', textColor=WHITE, leading=11)),
        ]], colWidths=[9*mm, INNER - 9*mm])
        hdr.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), DARK_RED),
            ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
            ('LEFTPADDING',  (0,0),(-1,-1), 4),('RIGHTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',   (0,0),(-1,-1), 3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ]))

        items = [Paragraph(f'<b>Por qué ocurre:</b> {p["why"]}', s_why),
                 Paragraph('<b>Qué hacer:</b>', s_qh)]
        for b in p['actions']:
            items.append(Paragraph(f'• {b}', s_bullet))

        body = Table([[item] for item in items], colWidths=[INNER])
        body.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), LIGHT_RED),
            ('LEFTPADDING',  (0,0),(-1,-1), 4),('RIGHTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',   (0,0),(-1,-1), 1),('BOTTOMPADDING',(0,0),(-1,-1),1),
        ]))

        result.append(KeepTogether([hdr, body, sp(2)]))
    return result


def build_summary():
    s_h  = S('sh', fontName='Helvetica-Bold', fontSize=8, textColor=WHITE, leading=11)
    s_b  = S('sb', fontSize=7.5, textColor=BLUE_GREY, leading=10.5)
    s_bb = S('sbb', fontName='Helvetica-Bold', fontSize=7.5, textColor=DARK_BLUE, leading=10.5)

    data = []
    for i, row in enumerate(SUMMARY):
        if i == 0:
            data.append([Paragraph(c, s_h) for c in row])
        else:
            data.append([Paragraph(row[0], s_bb), Paragraph(row[1], s_b)])

    tbl = Table(data, colWidths=[54*mm, INNER - 54*mm])
    style = [
        ('BACKGROUND', (0,0),(-1,0), DARK_BLUE),
        ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
        ('BOX',        (0,0),(-1,-1), 0.8, DARK_BLUE),
        ('INNERGRID',  (0,0),(-1,-1), 0.3, GRAY_M),
        ('LEFTPADDING', (0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',  (0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]
    for i in range(1, len(SUMMARY), 2):
        style.append(('BACKGROUND', (0,i),(-1,i), LIGHT_BLUE))
    tbl.setStyle(TableStyle(style))

    title = Table([[Paragraph(
        '<font name="Helvetica-Bold" size="9" color="white">RESUMEN RÁPIDO DE ADAPTACIONES</font>',
        S('rt', alignment=TA_CENTER, textColor=WHITE, leading=12))
    ]], colWidths=[INNER])
    title.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), DARK_BLUE),
        ('LEFTPADDING',  (0,0),(-1,-1), 4),
        ('TOPPADDING',   (0,0),(-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ]))
    return [title, tbl]


# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 34*mm, bottomMargin=MARGIN + 10*mm,
    )
    f1 = Frame(doc.leftMargin, doc.bottomMargin,
               INNER, H - doc.topMargin - doc.bottomMargin, id='p1')
    f2 = Frame(MARGIN, MARGIN + 8*mm,
               INNER, H - MARGIN - 20*mm - MARGIN - 8*mm, id='p2')
    doc.addPageTemplates([
        PageTemplate(id='page1', frames=[f1], onPage=page1_canvas),
        PageTemplate(id='page2', frames=[f2], onPage=page2_canvas),
    ])

    s_sec = S('sec', fontName='Helvetica-Bold', fontSize=9, textColor=DARK_BLUE,
              leading=12, spaceBefore=2, spaceAfter=2)

    story = []
    story += build_intro()
    story.append(sp(3))
    story.append(Paragraph('GUIÓN BASE — PASO A PASO', s_sec))
    story.append(hr(DARK_BLUE, 0.8))
    story.append(sp(1))
    story += build_senses()

    story.append(NextPageTemplate('page2'))
    story.append(PageBreak())
    story += build_problems()
    story.append(sp(3))
    story += build_summary()

    doc.build(story)
    print(f'PDF generado: {OUTPUT}')


if __name__ == '__main__':
    build()
