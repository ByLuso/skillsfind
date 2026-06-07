---
name: pdf-card-generator
description: Generates personalized PDF cards (business cards, greeting cards, certificates, invitations) from user-provided data. Triggers when the user asks to create, generate, or design any kind of card or certificate as a PDF file.
---

# PDF Card Generator

This skill creates personalized PDF cards using Node.js. It supports multiple card types and handles the full workflow: gathering data, generating the PDF, and saving the file.

## Supported Card Types

- **Business cards** — name, title, contact info, company
- **Greeting cards** — custom message, sender/recipient names
- **Certificates** — recipient name, achievement, date, issuer
- **Invitations** — event name, date/time, location, RSVP details
- **ID badges** — name, role, organization, optional photo placeholder

## Step 1: Gather Requirements

Ask the user for:

1. **Card type** — which of the supported types above
2. **Content fields** — all text that should appear on the card
3. **Style preferences** — colors (or "default"), font style (modern/classic/minimal), layout (portrait/landscape)
4. **Output path** — where to save the PDF (default: `./cards/output.pdf`)
5. **Quantity** — single card or batch from a list (CSV/JSON)

For batch generation, ask for the data source file path.

## Step 2: Check for PDFKit

Check if `pdfkit` is available in the project:

```bash
node -e "require('pdfkit')" 2>/dev/null && echo "available" || echo "missing"
```

If missing, install it:

```bash
npm install pdfkit
# or: pnpm add pdfkit / yarn add pdfkit
```

Also ensure the output directory exists:

```bash
mkdir -p ./cards
```

## Step 3: Generate the PDF

Create a script `generate-card.js` (or `.ts` if the project uses TypeScript) based on the card type chosen.

### Business Card Template

```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

function generateBusinessCard(data, outputPath) {
  // Standard business card: 85.6mm × 54mm → ~243pt × 153pt at 72dpi
  const W = 243;
  const H = 153;

  const doc = new PDFDocument({ size: [W, H], margin: 0 });
  doc.pipe(fs.createWriteStream(outputPath));

  const primary   = data.primaryColor   || '#1a1a2e';
  const accent    = data.accentColor    || '#e94560';
  const textLight = '#ffffff';
  const textDark  = '#333333';

  // Background
  doc.rect(0, 0, W, H).fill(primary);

  // Accent bar (left edge)
  doc.rect(0, 0, 6, H).fill(accent);

  // Name
  doc
    .fillColor(textLight)
    .font('Helvetica-Bold')
    .fontSize(13)
    .text(data.name || 'Your Name', 18, 28, { width: W - 24 });

  // Title
  doc
    .fillColor(accent)
    .font('Helvetica')
    .fontSize(8)
    .text((data.title || '').toUpperCase(), 18, 46, { width: W - 24, characterSpacing: 1 });

  // Divider
  doc.moveTo(18, 60).lineTo(W - 12, 60).stroke(accent);

  // Contact details
  const contacts = [
    data.email    && `✉  ${data.email}`,
    data.phone    && `✆  ${data.phone}`,
    data.website  && `⬡  ${data.website}`,
    data.address  && `⌖  ${data.address}`,
  ].filter(Boolean);

  doc.fillColor(textLight).font('Helvetica').fontSize(7.5);
  contacts.forEach((line, i) => {
    doc.text(line, 18, 68 + i * 13, { width: W - 24 });
  });

  // Company (bottom-right)
  if (data.company) {
    doc
      .fillColor(textLight)
      .font('Helvetica-Bold')
      .fontSize(9)
      .text(data.company, 0, H - 22, { width: W - 12, align: 'right' });
  }

  doc.end();
  console.log(`Business card saved → ${outputPath}`);
}

// --- Example usage ---
const cardData = {
  name:         'Ana García',
  title:        'Senior Software Engineer',
  company:      'TechCorp',
  email:        'ana@techcorp.com',
  phone:        '+34 600 123 456',
  website:      'techcorp.com',
  primaryColor: '#1a1a2e',
  accentColor:  '#e94560',
};

generateBusinessCard(cardData, './cards/business-card.pdf');
```

### Greeting Card Template

```javascript
function generateGreetingCard(data, outputPath) {
  // A6 landscape: 148mm × 105mm → ~420pt × 298pt
  const W = 420;
  const H = 298;

  const doc = new PDFDocument({ size: [W, H], margin: 0 });
  doc.pipe(fs.createWriteStream(outputPath));

  const bg      = data.backgroundColor || '#fdf6e3';
  const primary = data.primaryColor    || '#5c3317';
  const accent  = data.accentColor     || '#c0392b';

  // Background
  doc.rect(0, 0, W, H).fill(bg);

  // Decorative border
  doc.rect(10, 10, W - 20, H - 20).stroke(accent).lineWidth(2);
  doc.rect(14, 14, W - 28, H - 28).stroke(accent).lineWidth(0.5);

  // Greeting header
  doc
    .fillColor(accent)
    .font('Helvetica-Bold')
    .fontSize(22)
    .text(data.greeting || '¡Felicidades!', 0, 40, { align: 'center', width: W });

  // Main message
  doc
    .fillColor(primary)
    .font('Helvetica')
    .fontSize(12)
    .text(data.message || 'Wishing you all the best on your special day.', 40, 100, {
      align: 'center',
      width: W - 80,
    });

  // Decorative divider
  const midY = H / 2 + 20;
  doc.moveTo(60, midY).lineTo(W - 60, midY).stroke(accent).lineWidth(1);

  // From / To
  if (data.recipient) {
    doc
      .fillColor(primary)
      .font('Helvetica-Bold')
      .fontSize(10)
      .text(`Para: ${data.recipient}`, 40, midY + 14);
  }
  if (data.sender) {
    doc
      .fillColor(primary)
      .font('Helvetica')
      .fontSize(10)
      .text(`De parte de: ${data.sender}`, 0, midY + 14, { align: 'right', width: W - 40 });
  }

  // Date (bottom center)
  if (data.date) {
    doc
      .fillColor('#999')
      .font('Helvetica')
      .fontSize(9)
      .text(data.date, 0, H - 30, { align: 'center', width: W });
  }

  doc.end();
  console.log(`Greeting card saved → ${outputPath}`);
}
```

### Certificate Template

```javascript
function generateCertificate(data, outputPath) {
  // A4 landscape: 297mm × 210mm → ~842pt × 595pt
  const W = 842;
  const H = 595;

  const doc = new PDFDocument({ size: 'A4', layout: 'landscape', margin: 0 });
  doc.pipe(fs.createWriteStream(outputPath));

  const gold   = data.accentColor  || '#c9a84c';
  const dark   = data.primaryColor || '#1a1a2e';
  const bg     = data.bgColor      || '#fdfaf0';

  // Background fill
  doc.rect(0, 0, W, H).fill(bg);

  // Outer gold border
  doc.rect(20, 20, W - 40, H - 40).stroke(gold).lineWidth(3);
  doc.rect(28, 28, W - 56, H - 56).stroke(gold).lineWidth(1);

  // Header: issuer / organization
  doc
    .fillColor(dark)
    .font('Helvetica-Bold')
    .fontSize(13)
    .text((data.organization || 'Your Organization').toUpperCase(), 0, 60, {
      align: 'center',
      width: W,
      characterSpacing: 2,
    });

  // Certificate title
  doc
    .fillColor(gold)
    .font('Helvetica-Bold')
    .fontSize(36)
    .text('CERTIFICADO', 0, 100, { align: 'center', width: W });

  doc
    .fillColor(dark)
    .font('Helvetica')
    .fontSize(13)
    .text('de ' + (data.certificateType || 'Participación'), 0, 144, {
      align: 'center',
      width: W,
    });

  // Divider
  doc.moveTo(100, 170).lineTo(W - 100, 170).stroke(gold).lineWidth(1.5);

  // Body text
  doc
    .fillColor(dark)
    .font('Helvetica')
    .fontSize(12)
    .text(data.bodyText || 'Se certifica que', 0, 190, { align: 'center', width: W });

  // Recipient name (large)
  doc
    .fillColor(dark)
    .font('Helvetica-Bold')
    .fontSize(30)
    .text(data.recipient || 'Nombre del Destinatario', 0, 215, { align: 'center', width: W });

  // Achievement description
  if (data.achievement) {
    doc
      .fillColor(dark)
      .font('Helvetica')
      .fontSize(12)
      .text(data.achievement, 80, 265, { align: 'center', width: W - 160 });
  }

  // Divider bottom
  doc.moveTo(100, 310).lineTo(W - 100, 310).stroke(gold).lineWidth(1);

  // Signature lines
  const sigY = 360;
  const leftX  = 120;
  const rightX = W - 300;

  doc.moveTo(leftX, sigY + 30).lineTo(leftX + 180, sigY + 30).stroke(dark).lineWidth(0.5);
  doc.moveTo(rightX, sigY + 30).lineTo(rightX + 180, sigY + 30).stroke(dark).lineWidth(0.5);

  doc
    .fillColor(dark)
    .font('Helvetica')
    .fontSize(10)
    .text(data.signerLeft  || 'Firma Autorizada', leftX, sigY + 36, { width: 180, align: 'center' })
    .text(data.signerRight || data.date || new Date().toLocaleDateString('es-ES'), rightX, sigY + 36, {
      width: 180,
      align: 'center',
    });

  doc.end();
  console.log(`Certificate saved → ${outputPath}`);
}
```

## Step 4: Batch Generation (Optional)

If the user wants to generate cards for multiple people from a CSV or JSON file:

```javascript
const fs = require('fs');

// For CSV input
function loadFromCSV(filePath) {
  const lines = fs.readFileSync(filePath, 'utf8').trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  return lines.slice(1).map(line => {
    const values = line.split(',').map(v => v.trim());
    return Object.fromEntries(headers.map((h, i) => [h, values[i]]));
  });
}

// For JSON input
function loadFromJSON(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

// Batch generate
async function batchGenerate(dataList, cardType, outputDir) {
  fs.mkdirSync(outputDir, { recursive: true });
  dataList.forEach((data, index) => {
    const safeName = (data.name || `card-${index}`).replace(/[^a-z0-9]/gi, '_');
    const outPath  = path.join(outputDir, `${safeName}.pdf`);
    if (cardType === 'business')     generateBusinessCard(data, outPath);
    else if (cardType === 'greeting') generateGreetingCard(data, outPath);
    else if (cardType === 'certificate') generateCertificate(data, outPath);
  });
  console.log(`Generated ${dataList.length} cards in ${outputDir}`);
}
```

## Step 5: Run and Verify

After writing the script, run it:

```bash
node generate-card.js
```

Confirm the PDF was created at the expected path and report its size:

```bash
ls -lh ./cards/
```

Open or share the file path with the user.

## Common Customizations

| Need | What to change |
|---|---|
| Different page size | `PDFDocument({ size: 'A4' })` or `[width, height]` in points (1pt = 1/72 inch) |
| Custom font | `doc.registerFont('MyFont', './fonts/MyFont.ttf')` then `.font('MyFont')` |
| Background image | `doc.image('./bg.jpg', 0, 0, { width: W, height: H })` |
| QR code | Add `qrcode` npm package and render as image |
| Logo | `doc.image('./logo.png', x, y, { width: 60 })` |
| Two-sided card | Generate two pages: `doc.addPage()` |

## Error Handling

- **Module not found (pdfkit)**: Run `npm install pdfkit` in the project root.
- **ENOENT on output path**: Create the directory first with `mkdir -p ./cards`.
- **Garbled text / missing glyphs**: Switch to a TTF font that supports your characters.
- **File too large**: Compress with `ghostscript`: `gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -sOutputFile=out.pdf in.pdf`

## Tips

- 1 point (PDF unit) = 1/72 inch. A business card at 85.6mm = ~243pt.
- Use `doc.save()` and `doc.restore()` to scope graphic state changes.
- Call `doc.end()` only once — it finalizes and closes the stream.
- For pixel-perfect layout, work in points and use `doc.page.width` / `doc.page.height`.
