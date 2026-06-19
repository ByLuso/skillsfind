from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = "/home/user/skillsfind/tecnica_STOP_paciente.pdf"

W, H = A4
MARGIN = 14 * mm

# Palette — warm clinical, B&W safe
NAVY      = colors.HexColor('#00356B')
BLUE      = colors.HexColor('#1565C0')
LIGHT_BG  = colors.HexColor('#EEF4FB')
TEAL      = colors.HexColor('#00695C')
TEAL_L    = colors.HexColor('#E0F5F1')
PURPLE    = colors.HexColor('#5C3D8F')
PURPLE_L  = colors.HexColor('#F0EBF8')
ORANGE    = colors.HexColor('#D84315')
ORANGE_L  = colors.HexColor('#FFF0EA')
GRAY_D    = colors.HexColor('#37474F')
GRAY_M    = colors.HexColor('#90A4AE')
GRAY_L    = colors.HexColor('#F4F7FA')
WHITE     = colors.white
BLACK     = colors.black

INNER = W - 2 * MARGIN


def draw_page(c, doc):
    # Top header band
    c.setFillColor(NAVY)
    c.rect(0, H - 30*mm, W, 30*mm, fill=1, stroke=0)
    # Thin accent line
    c.setFillColor(BLUE)
    c.rect(0, H - 32*mm, W, 2*mm, fill=1, stroke=0)
    # Title
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 18)
    c.drawCentredString(W/2, H - 14*mm, 'Técnica  S · T · O · P')
    c.setFont('Helvetica', 9)
    c.setFillColor(colors.HexColor('#AECBF0'))
    c.drawCentredString(W/2, H - 22*mm, 'Una pausa consciente que puedes usar en cualquier momento y lugar')
    # Footer
    c.setFillColor(GRAY_M)
    c.setFont('Helvetica', 6.5)
    c.drawCentredString(W/2, 8*mm, 'Técnica S.T.O.P. · Adaptado de MBSR (Kabat-Zinn) · Uso terapéutico')


def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=9, leading=13, textColor=GRAY_D)
    base.update(kw)
    return ParagraphStyle(name, **base)


def build_intro():
    intro = (
        'Tiene cuatro pasos y los hacemos juntos. No necesitas experiencia previa, '
        'no hay forma de hacerlo mal. Es tuya: úsala cuando lo necesites.'
    )
    row = Table([[Paragraph(intro, S('i', fontSize=9, leading=13, textColor=GRAY_D,
                                     alignment=TA_CENTER))]], colWidths=[INNER])
    row.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), LIGHT_BG),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('LINEBELOW',    (0,0), (-1,-1), 1.5, BLUE),
    ]))
    return [row]


STEPS = [
    {
        'letter': 'S',
        'en': 'STOP',
        'es': 'Para',
        'color': NAVY,
        'light': LIGHT_BG,
        'body': (
            'Lo primero es simplemente <b>dejar de hacer lo que estás haciendo</b>. '
            'Si estás hablando, paras. Si estás pensando en algo, paras. '
            'Solo un momento — como si pulsaras el botón de pausa.'
        ),
    },
    {
        'letter': 'T',
        'en': 'TAKE A BREATH',
        'es': 'Respira',
        'color': TEAL,
        'light': TEAL_L,
        'body': (
            'Toma <b>una respiración consciente</b>. No tiene que ser perfecta. '
            'Solo un poco más consciente que las anteriores. '
            'Nota cómo entra el aire y cómo sale. '
            'No tienes que cambiar nada — solo observar que estás respirando.'
        ),
    },
    {
        'letter': 'O',
        'en': 'OBSERVE',
        'es': 'Observa',
        'color': PURPLE,
        'light': PURPLE_L,
        'body': (
            'Mira hacia dentro <b>sin juzgar</b> lo que encuentres. '
            '¿Qué sientes en el cuerpo? ¿Qué emoción está presente? '
            '¿Qué está diciendo tu mente? No tienes que resolver nada. '
            'Solo mirar — como si fueras un testigo de lo que ocurre dentro de ti. '
            'Si aparece un pensamiento, <b>no te metas dentro de él</b>: '
            'nótalo desde fuera, como si lo vieras escrito en una pantalla.'
        ),
    },
    {
        'letter': 'P',
        'en': 'PROCEED',
        'es': 'Continúa',
        'color': ORANGE,
        'light': ORANGE_L,
        'body': (
            'Después de haber parado, respirado y observado, '
            'te preguntas: <b>¿qué quiero hacer ahora?</b> '
            'No lo que harías en automático — '
            'sino lo que <i>tú eliges</i> hacer conscientemente en este momento.'
        ),
    },
]


def build_steps():
    result = []
    for step in STEPS:
        col   = step['color']
        light = step['light']

        # Badge + title header
        badge = Paragraph(
            f'<font name="Helvetica-Bold" size="26" color="white">{step["letter"]}</font>',
            S('badge', alignment=TA_CENTER, leading=30)
        )
        title_block = [
            Paragraph(
                f'<font name="Helvetica-Bold" size="12" color="white">{step["en"]}</font>',
                S('en', textColor=WHITE, leading=14)
            ),
            Paragraph(
                f'<font size="9" color="#DDEEFF">{step["es"]}</font>',
                S('es', textColor=WHITE, leading=11)
            ),
        ]
        hdr = Table([[badge, title_block]], colWidths=[14*mm, INNER - 14*mm])
        hdr.setStyle(TableStyle([
            ('BACKGROUND',   (0,0), (-1,-1), col),
            ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING',  (0,0), (0,0),   3),
            ('LEFTPADDING',  (1,0), (1,0),   6),
            ('TOPPADDING',   (0,0), (-1,-1), 5),
            ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ]))

        # Body
        body = Table(
            [[Paragraph(step['body'], S('b', fontSize=9, leading=13.5, textColor=GRAY_D))]],
            colWidths=[INNER]
        )
        body.setStyle(TableStyle([
            ('BACKGROUND',   (0,0), (-1,-1), light),
            ('LEFTPADDING',  (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING',   (0,0), (-1,-1), 5),
            ('BOTTOMPADDING',(0,0), (-1,-1), 7),
            ('LINEBELOW',    (0,0), (-1,-1), 1.5, col),
        ]))

        result.append(KeepTogether([hdr, body, Spacer(1, 3*mm)]))

    return result


def build_reminder():
    text = (
        '<b>Recuerda:</b> no hay forma de hacerlo mal. '
        'Cuantas más veces lo practiques en momentos tranquilos — '
        'en un atasco, esperando en una cola, en una pausa — '
        'más disponible estará cuando de verdad lo necesites.'
    )
    box = Table([[Paragraph(text, S('r', fontSize=8.5, leading=12.5, textColor=NAVY))]], colWidths=[INNER])
    box.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), LIGHT_BG),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('BOX',          (0,0), (-1,-1), 1, BLUE),
    ]))
    return [box]


def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 34*mm,
        bottomMargin=MARGIN + 8*mm,
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        INNER, H - doc.topMargin - doc.bottomMargin,
        id='main',
    )
    doc.addPageTemplates([PageTemplate(id='p1', frames=[frame], onPage=draw_page)])

    story = []
    story += build_intro()
    story.append(Spacer(1, 4*mm))
    story += build_steps()
    story.append(Spacer(1, 2*mm))
    story += build_reminder()

    doc.build(story)
    print(f'PDF generado: {OUTPUT}')


if __name__ == '__main__':
    build()
