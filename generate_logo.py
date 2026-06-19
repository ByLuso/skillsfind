"""
Genera el logo de Luis Martínez en SVG y PNG,
más un bloque de firma listo para insertar en los PDFs.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT_BOLD   = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_REG    = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FONT_ITALIC = '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'

OUT_DIR = '/home/user/skillsfind'

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY   = (0,   45,  95)      # #002D5F
BLUE   = (21, 101, 192)      # #1565C0
TEAL   = (0,  105,  92)      # #00695C
WHITE  = (255, 255, 255)
GRAY   = (144, 164, 174)


# ── SVG (scalable, primary asset) ───────────────────────────────────────────
SVG = """\
<svg width="460" height="110" viewBox="0 0 460 110"
     xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Luis Martínez — Enfermero">

  <!-- Monogram badge -->
  <circle cx="55" cy="55" r="50" fill="#002D5F"/>
  <!-- inner ring accent -->
  <circle cx="55" cy="55" r="44" fill="none" stroke="#1565C0" stroke-width="2"/>
  <!-- LM initials -->
  <text x="55" y="67"
        font-family="Liberation Sans, Arial, sans-serif"
        font-size="30" font-weight="bold"
        fill="white" text-anchor="middle"
        letter-spacing="1">LM</text>

  <!-- Vertical divider -->
  <line x1="122" y1="18" x2="122" y2="92"
        stroke="#90A4AE" stroke-width="1.5"/>

  <!-- Name -->
  <text x="140" y="52"
        font-family="Liberation Sans, Arial, sans-serif"
        font-size="30" font-weight="bold"
        fill="#002D5F" letter-spacing="0.5">Luis Martínez</text>

  <!-- Profession -->
  <text x="142" y="76"
        font-family="Liberation Sans, Arial, sans-serif"
        font-size="16" fill="#00695C" letter-spacing="2">ENFERMERO</text>

  <!-- Accent underline -->
  <line x1="140" y1="86" x2="452" y2="86"
        stroke="#1565C0" stroke-width="2.5"/>
  <!-- small teal dot at end -->
  <circle cx="452" cy="86" r="3.5" fill="#00695C"/>
</svg>
"""

svg_path = os.path.join(OUT_DIR, 'logo_luis_martinez.svg')
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(SVG)
print(f'SVG guardado: {svg_path}')


# ── PNG (300 dpi equivalent, 2× for sharpness) ──────────────────────────────
SCALE  = 3          # 3× → ~150 dpi on screen, crisp for PDF embed
W, H   = 460, 110
pw, ph = W * SCALE, H * SCALE

img  = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

cx, cy, r = 55*SCALE, 55*SCALE, 50*SCALE

# Badge circle
draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=NAVY + (255,))
# Inner ring
draw.ellipse([cx-44*SCALE, cy-44*SCALE, cx+44*SCALE, cy+44*SCALE],
             outline=BLUE + (255,), width=SCALE*2)

# Initials
font_init = ImageFont.truetype(FONT_BOLD, 30*SCALE)
draw.text((cx, cy+4*SCALE), 'LM', font=font_init, fill=WHITE+(255,), anchor='mm')

# Divider
lx = 122*SCALE
draw.line([(lx, 18*SCALE), (lx, 92*SCALE)], fill=GRAY+(255,), width=SCALE)

# Name
font_name = ImageFont.truetype(FONT_BOLD, 30*SCALE)
draw.text((140*SCALE, 48*SCALE), 'Luis Martínez',
          font=font_name, fill=NAVY+(255,), anchor='lm')

# Profession
font_prof = ImageFont.truetype(FONT_REG, 14*SCALE)
draw.text((142*SCALE, 74*SCALE), 'ENFERMERO',
          font=font_prof, fill=TEAL+(255,), anchor='lm')

# Accent line
line_y = 86*SCALE
draw.line([(140*SCALE, line_y), (452*SCALE, line_y)],
          fill=BLUE+(255,), width=SCALE*2)
# Dot
dot_r = 3*SCALE
draw.ellipse([(452*SCALE - dot_r, line_y - dot_r),
              (452*SCALE + dot_r, line_y + dot_r)],
             fill=TEAL+(255,))

# Downscale with LANCZOS for anti-aliasing
final = img.resize((W, H), Image.LANCZOS)
png_path = os.path.join(OUT_DIR, 'logo_luis_martinez.png')
final.save(png_path, 'PNG')
print(f'PNG guardado: {png_path}')


# ── B&W version (para impresión en escala de grises) ────────────────────────
bw = final.convert('LA').convert('RGBA')
bw_path = os.path.join(OUT_DIR, 'logo_luis_martinez_bw.png')
bw.save(bw_path, 'PNG')
print(f'PNG B&W guardado: {bw_path}')

print('\nArchivos generados:')
for p in [svg_path, png_path, bw_path]:
    size = os.path.getsize(p)
    print(f'  {os.path.basename(p):40s} {size/1024:.1f} KB')
