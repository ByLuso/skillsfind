from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/home/user/skillsfind/guia_clinica_STOP.pdf"

# ── Palette (all contrast-safe in B&W) ──────────────────────────────────────
DARK_BLUE  = colors.HexColor('#002D5F')
MED_BLUE   = colors.HexColor('#1565C0')
LIGHT_BLUE = colors.HexColor('#EBF3FB')
TEAL       = colors.HexColor('#00695C')
LIGHT_TEAL = colors.HexColor('#E0F5F1')
DARK_RED   = colors.HexColor('#B71C1C')
LIGHT_RED  = colors.HexColor('#FDECEA')
GRAY_D     = colors.HexColor('#37474F')
GRAY_M     = colors.HexColor('#90A4AE')
GRAY_L     = colors.HexColor('#F4F6F8')
WHITE      = colors.white
BLACK      = colors.black

W, H = A4
MARGIN = 14 * mm
INNER  = W - 2 * MARGIN


# ── Page canvas decorators ───────────────────────────────────────────────────
def page1_canvas(c, doc):
    # header band
    c.setFillColor(DARK_BLUE)
    c.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)
    # accent stripe
    c.setFillColor(MED_BLUE)
    c.rect(0, H - 30*mm, W, 2*mm, fill=1, stroke=0)
    # titles
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 15)
    c.drawCentredString(W/2, H - 13*mm, 'GUÍA DE APLICACIÓN CLÍNICA — Técnica S.T.O.P.')
    c.setFont('Helvetica', 9)
    c.drawCentredString(W/2, H - 21*mm, 'Herramienta de pausa consciente · Para uso del terapeuta en sesión')
    # footer
    _footer(c, doc, 1)

def page2_canvas(c, doc):
    # thinner header
    c.setFillColor(DARK_BLUE)
    c.rect(0, H - 16*mm, W, 16*mm, fill=1, stroke=0)
    c.setFillColor(MED_BLUE)
    c.rect(0, H - 18*mm, W, 2*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(W/2, H - 11*mm, 'Técnica S.T.O.P. — Resolución de Dificultades')
    _footer(c, doc, 2)

def _footer(c, doc, pg):
    c.setFillColor(GRAY_M)
    c.setFont('Helvetica', 6.5)
    c.drawCentredString(W/2, 7*mm,
        f'Técnica S.T.O.P. · Uso clínico interno · Adaptado de MBSR (Kabat-Zinn) y ACT (Hayes)   |   pág. {pg}')


# ── Style factory ────────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName='Helvetica', fontSize=8.5, leading=12,
                    textColor=BLACK, spaceAfter=0, spaceBefore=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

bold = lambda s, size=8.5: f'<font name="Helvetica-Bold" size="{size}">{s}</font>'
it   = lambda s: f'<font name="Helvetica-Oblique">{s}</font>'


# ── Helpers ──────────────────────────────────────────────────────────────────
def hr(color=GRAY_M, thick=0.4):
    return HRFlowable(width='100%', thickness=thick, color=color, spaceAfter=2, spaceBefore=2)

def sp(h=2):
    return Spacer(1, h*mm)

def section_tag(letter, color_bg, color_text=WHITE):
    """Big coloured letter badge."""
    return Table(
        [[Paragraph(f'<font name="Helvetica-Bold" size="22" color="{color_text.hexval() if hasattr(color_text,"hexval") else "white"}">{letter}</font>',
                    S('lt', alignment=TA_CENTER, leading=26))]],
        colWidths=[12*mm], rowHeights=[12*mm]
    )


# ── Content builders ─────────────────────────────────────────────────────────
def build_intro(inner):
    s_body  = S('body', fontSize=8.5, leading=12, textColor=GRAY_D)
    s_label = S('label', fontName='Helvetica-Bold', fontSize=7.5, textColor=MED_BLUE)

    intro_text = (
        'La técnica S.T.O.P. interrumpe el piloto automático emocional o cognitivo '
        'en el momento en que se detecta activación. Sus cuatro pasos permiten al paciente '
        'pasar de la reacción automática a la respuesta consciente en menos de dos minutos.'
    )
    cuando = (
        bold('Indicaciones: ') +
        'Rumiación · Impulsos reactivos · Escalada emocional · Craving · '
        'Conflictos interpersonales · Estrés agudo situacional'
    )

    box_data = [[
        Paragraph(intro_text, s_body),
    ]]
    box = Table(box_data, colWidths=[inner])
    box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE),
        ('LEFTPADDING',  (0,0), (-1,-1), 5), ('RIGHTPADDING',  (0,0), (-1,-1), 5),
        ('TOPPADDING',   (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW',  (0,0), (-1,-1), 1.5, MED_BLUE),
    ]))

    cuando_row = Table([[Paragraph(cuando, S('c', fontSize=7.5, textColor=GRAY_D, leading=11))]],
                       colWidths=[inner])
    cuando_row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GRAY_L),
        ('LEFTPADDING',  (0,0), (-1,-1), 5), ('RIGHTPADDING',  (0,0), (-1,-1), 5),
        ('TOPPADDING',   (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return [box, sp(1), cuando_row]


def build_steps(inner):
    steps = [
        {
            'letter': 'S',
            'en': 'STOP',
            'es': 'Para',
            'color': DARK_BLUE,
            'light': LIGHT_BLUE,
            'quote': '«Detente justo donde estás. No hagas nada todavía.»',
            'bullets': [
                'Interrumpir físicamente la actividad o el pensamiento en curso.',
                'Señal interna: reconocer activación emocional o cognitiva significativa.',
                bold('Objetivo:') + ' romper el automatismo reactivo.',
            ]
        },
        {
            'letter': 'T',
            'en': 'TAKE A BREATH',
            'es': 'Respira',
            'color': TEAL,
            'light': LIGHT_TEAL,
            'quote': '«Toma una respiración consciente. Nota cómo entra el aire y cómo sale.»',
            'bullets': [
                'Respiración profunda y lenta; atención al movimiento del abdomen.',
                'Opcional: técnica 4-4-4 (inhala · retén · exhala, 4 seg cada fase).',
                bold('Objetivo:') + ' activar el sistema nervioso parasimpático y reducir cortisol/adrenalina.',
            ]
        },
        {
            'letter': 'O',
            'en': 'OBSERVE',
            'es': 'Observa',
            'color': colors.HexColor('#6A1B9A'),
            'light': colors.HexColor('#F3E5F5'),
            'quote': '«¿Qué está pasando dentro de ti ahora mismo? Sin juzgarlo, sin cambiarlo.»',
            'bullets': [],
            'table': [
                [bold('Canal'), bold('Preguntas guía')],
                ['Cuerpo',       '¿Dónde noto tensión? ¿Qué sensaciones físicas hay?'],
                ['Emociones',    '¿Qué emoción está presente? ¿Intensidad (0-10)?'],
                ['Pensamientos', '¿Qué dice mi mente? ¿Son hechos o interpretaciones?'],
            ],
            'note': (
                'Postura de testigo imparcial: observar sin identificarse. '
                'Nombrar la emoción («noto que hay ansiedad»). '
                + bold('Objetivo:') + ' distancia metacognitiva y defusión cognitiva.'
            )
        },
        {
            'letter': 'P',
            'en': 'PROCEED',
            'es': 'Continúa con conciencia',
            'color': colors.HexColor('#E65100'),
            'light': colors.HexColor('#FFF3E0'),
            'quote': '«¿Qué quieres hacer ahora? No la reacción automática — lo que tú eliges.»',
            'bullets': [
                'Retomar la actividad con mayor conciencia o elegir una acción deliberada.',
                it('«¿Qué haría la persona que quiero ser en este momento?»') + ' (enlace ACT con valores).',
                bold('Objetivo:') + ' acción consciente frente a reacción automática.',
            ]
        },
    ]

    result = []
    for step in steps:
        col = step['color']
        light = step['light']
        s_body = S('sb', fontSize=8, leading=11.5, textColor=GRAY_D, leftIndent=4)
        s_quote = S('sq', fontName='Helvetica-Oblique', fontSize=8.5, textColor=col,
                    leading=12, leftIndent=4)

        # Header row: letter badge + title
        letter_cell = Paragraph(
            f'<font name="Helvetica-Bold" size="24">{step["letter"]}</font>',
            S('lc', alignment=TA_CENTER, textColor=WHITE, leading=28)
        )
        title_cell = [
            Paragraph(f'<font name="Helvetica-Bold" size="11" color="#FFFFFF">{step["en"]}</font>',
                      S('tc', textColor=WHITE, leading=14)),
            Paragraph(f'<font size="8.5" color="#CCDDFF">{step["es"]}</font>',
                      S('tcs', textColor=WHITE, leading=11)),
        ]
        header = Table([[letter_cell, title_cell]], colWidths=[14*mm, inner-14*mm])
        header.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), col),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING',  (0,0), (0,0), 2), ('RIGHTPADDING',  (0,0), (0,0), 2),
            ('LEFTPADDING',  (1,0), (1,0), 4),
            ('TOPPADDING',   (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))

        body_rows = [header]
        inner_content = [Paragraph(step['quote'], s_quote)]

        for b in step.get('bullets', []):
            inner_content.append(Paragraph(f'• {b}', s_body))

        if 'table' in step:
            t_data = []
            for i, row in enumerate(step['table']):
                t_data.append([Paragraph(str(c), S(f'tc{i}', fontSize=7.5,
                    fontName='Helvetica-Bold' if i==0 else 'Helvetica',
                    textColor=WHITE if i==0 else GRAY_D, leading=10)) for c in row])
            obs = Table(t_data, colWidths=[28*mm, inner-28*mm-16*mm], hAlign='LEFT')
            obs.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), col),
                ('BACKGROUND', (0,1), (-1,1), light),
                ('BACKGROUND', (0,2), (-1,2), WHITE),
                ('BACKGROUND', (0,3), (-1,3), light),
                ('BOX',       (0,0), (-1,-1), 0.5, GRAY_M),
                ('INNERGRID', (0,0), (-1,-1), 0.3, GRAY_M),
                ('LEFTPADDING',  (0,0), (-1,-1), 4),
                ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ('TOPPADDING',   (0,0), (-1,-1), 2),
                ('BOTTOMPADDING',(0,0), (-1,-1), 2),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            inner_content.append(sp(1))
            inner_content.append(obs)
            if 'note' in step:
                inner_content.append(sp(1))
                inner_content.append(Paragraph(step['note'],
                    S('note', fontSize=7.5, textColor=GRAY_D, leading=10.5, leftIndent=4)))

        body_cell = Table([[c] for c in inner_content], colWidths=[inner-8*mm])
        body_cell.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), light),
            ('LEFTPADDING',  (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING',   (0,0), (-1,-1), 2), ('BOTTOMPADDING',(0,0), (-1,-1), 2),
        ]))

        outer = Table([[body_cell]], colWidths=[inner])
        outer.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), light),
            ('LEFTPADDING',  (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING',   (0,0), (-1,-1), 0), ('BOTTOMPADDING',(0,0), (-1,-1), 4),
            ('LINEBELOW', (0,0), (-1,-1), 1, col),
        ]))

        result.append(KeepTogether([header, outer, sp(2)]))

    return result


def build_problems(inner):
    problems = [
        {
            'n': '1',
            'title': 'No puede parar — activación demasiado alta',
            'why': 'Con activación intensa el córtex prefrontal está inhibido y el paciente no puede «decidir parar».',
            'actions': [
                'Añadir ancla física previa: «Pon los dos pies en el suelo, nota el peso. Ahora sí — para.»',
                'Usar una señal física externa como disparador (ej. mano en el pecho).',
                'Entrenar la técnica en momentos de baja activación, no en crisis.',
            ]
        },
        {
            'n': '2',
            'title': 'La respiración genera más ansiedad',
            'why': 'Frecuente en pánico o hipocondría: dirigir atención a la respiración puede disparar más activación.',
            'actions': [
                'Redirigir la atención: «Solo observa que estás respirando, sin cambiar nada.»',
                'Sustituir por pausa sensorial externa: notar la temperatura de la mesa durante 3 segundos.',
                'Abreviar el paso T a una simple pausa de 2 segundos.',
            ]
        },
        {
            'n': '3',
            'title': 'Se pierde en los pensamientos en lugar de observarlos',
            'why': 'La instrucción de «observar la mente» puede convertirse en déclencheur de más rumiación (especialmente en depresión o TAG).',
            'actions': [
                'Defusión cognitiva ACT: «Nótalo desde fuera. ¿Qué dice? No si es verdad — solo qué dice.»',
                'Limitar a 5 segundos: «Una palabra o frase es suficiente.»',
                'Anclar al cuerpo si la mente se dispersa: «¿Dónde sientes la emoción físicamente?»',
                'Fórmula de nombrado: «En lugar de \'estoy ansioso\', prueba \'noto que hay ansiedad\'.»',
            ]
        },
        {
            'n': '4',
            'title': 'El paso P siempre termina en la misma respuesta automática',
            'why': 'El hábito conductual es tan fuerte que vuelve a la respuesta automática aunque haya completado los cuatro pasos.',
            'actions': [
                'Trabajar el paso P explícitamente en sesión, en frío: listar opciones antes de que ocurra la situación.',
                'Conectar con valores: «¿Qué haría la versión de ti que actúa desde lo que más te importa?»',
                'Introducir micro-demora conductual: «Solo espera 2 minutos antes de actuar.»',
            ]
        },
        {
            'n': '5',
            'title': 'Lo hace en sesión pero no lo recuerda en el momento real',
            'why': 'Bajo alta activación el acceso al recuerdo procedimental se bloquea; la técnica aún no está automatizada.',
            'actions': [
                'Crear una tarjeta física (o fondo de pantalla) con las cuatro letras y una frase por paso.',
                'Establecer disparador corporal personalizado: la primera señal de activación = inicio del STOP.',
                'Practicar a diario en situaciones de baja intensidad (atasco, cola, aburrimiento).',
            ]
        },
        {
            'n': '6',
            'title': 'Le parece demasiado simple o no se cree que funcione',
            'why': 'Pacientes con alta capacidad intelectual o experiencias previas negativas pueden desestimar la técnica.',
            'actions': [
                'Explicar el mecanismo: la activación inhibe el córtex prefrontal; parar y observar lo reactiva.',
                'Ofrecerla como experimento: «No te pido que creas que funciona. Pruébala 5 veces y cuéntame qué observas.»',
                'Normalizar efecto acumulativo: «La primera vez cambia poco. La décima vez, sí.»',
            ]
        },
    ]

    s_why    = S('why', fontSize=7.5, textColor=GRAY_D, leading=10.5,
                 fontName='Helvetica-Oblique', leftIndent=4)
    s_bullet = S('bul', fontSize=7.5, textColor=GRAY_D, leading=10.5, leftIndent=8)

    result = []
    for i, p in enumerate(problems):
        # header
        hdr = Table([[
            Paragraph(f'<font name="Helvetica-Bold" size="10" color="white">P{p["n"]}</font>',
                      S('ph', alignment=TA_CENTER, leading=12)),
            Paragraph(f'<font name="Helvetica-Bold" size="8.5" color="white">{p["title"]}</font>',
                      S('pt', textColor=WHITE, leading=11)),
        ]], colWidths=[9*mm, inner-9*mm])
        hdr.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), DARK_RED),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING',  (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING',   (0,0), (-1,-1), 3),
            ('BOTTOMPADDING',(0,0), (-1,-1), 3),
        ]))

        body_items = [Paragraph(f'<b>Por qué ocurre:</b> {p["why"]}', s_why)]
        body_items.append(Paragraph('<b>Qué hacer:</b>', S('qh', fontSize=7.5, textColor=DARK_RED,
                                                           fontName='Helvetica-Bold', leading=10, leftIndent=4)))
        for b in p['actions']:
            body_items.append(Paragraph(f'• {b}', s_bullet))

        body_rows = [[item] for item in body_items]
        body = Table(body_rows, colWidths=[inner])
        body.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_RED),
            ('LEFTPADDING',  (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING',   (0,0), (-1,-1), 1), ('BOTTOMPADDING',(0,0), (-1,-1), 1),
        ]))

        result.append(KeepTogether([hdr, body, sp(2)]))

    return result


def build_summary(inner):
    s_h = S('sh', fontName='Helvetica-Bold', fontSize=8, textColor=WHITE, leading=11)
    s_b = S('sb2', fontSize=7.5, textColor=GRAY_D, leading=10.5)
    s_b_bold = S('sbb', fontName='Helvetica-Bold', fontSize=7.5, textColor=DARK_BLUE, leading=10.5)

    rows = [
        [Paragraph('Dificultad', s_h), Paragraph('Adaptación clave', s_h)],
        ['No puede parar', 'Ancla física previa + entrenar en calma'],
        ['Respiración genera ansiedad', 'Observar sin cambiar + sustituir por pausa táctil'],
        ['Se pierde en pensamientos', 'Defusión ACT + anclar al cuerpo + límite de tiempo'],
        ['Siempre termina igual en P', 'Opciones en frío + conectar con valores'],
        ['No lo recuerda en el momento', 'Tarjeta física + disparador corporal personalizado'],
        ['No se cree que funcione', 'Explicación neurofisiológica + enfoque experimental'],
    ]

    data = []
    for i, row in enumerate(rows):
        if i == 0:
            data.append(row)
        else:
            data.append([Paragraph(row[0], s_b_bold), Paragraph(row[1], s_b)])

    tbl = Table(data, colWidths=[58*mm, inner-58*mm])
    style = [
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX',       (0,0), (-1,-1), 0.8, DARK_BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.3, GRAY_M),
        ('LEFTPADDING',  (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING',   (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0), (-1,-1), 3),
    ]
    for i in range(1, len(rows), 2):
        style.append(('BACKGROUND', (0,i), (-1,i), LIGHT_BLUE))
    tbl.setStyle(TableStyle(style))

    title = Table([[
        Paragraph('<font name="Helvetica-Bold" size="9" color="white">RESUMEN RÁPIDO DE ADAPTACIONES</font>',
                  S('rt', alignment=TA_CENTER, textColor=WHITE, leading=12))
    ]], colWidths=[inner])
    title.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('LEFTPADDING',  (0,0), (-1,-1), 4),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
    ]))

    return [title, tbl]


# ── Main ─────────────────────────────────────────────────────────────────────
def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=MARGIN + 32*mm, bottomMargin=MARGIN + 8*mm,
    )

    frame1 = Frame(
        doc.leftMargin, doc.bottomMargin,
        INNER, H - doc.topMargin - doc.bottomMargin,
        id='p1',
    )
    frame2 = Frame(
        MARGIN, MARGIN + 6*mm,
        INNER, H - MARGIN - 20*mm - MARGIN - 6*mm,
        id='p2',
    )

    doc.addPageTemplates([
        PageTemplate(id='page1', frames=[frame1], onPage=page1_canvas),
        PageTemplate(id='page2', frames=[frame2], onPage=page2_canvas),
    ])

    from reportlab.platypus import NextPageTemplate, PageBreak

    s_section = S('sec', fontName='Helvetica-Bold', fontSize=9, textColor=DARK_BLUE,
                  leading=12, spaceBefore=2, spaceAfter=2)

    story = []

    # Page 1
    story += build_intro(INNER)
    story.append(sp(3))
    story.append(Paragraph('PROTOCOLO PASO A PASO', s_section))
    story.append(hr(DARK_BLUE, 0.8))
    story.append(sp(1))
    story += build_steps(INNER)

    # Page 2
    story.append(NextPageTemplate('page2'))
    story.append(PageBreak())
    story += build_problems(INNER)
    story.append(sp(3))
    story += build_summary(INNER)

    doc.build(story)
    print(f'PDF generado: {OUTPUT}')


if __name__ == '__main__':
    build()
