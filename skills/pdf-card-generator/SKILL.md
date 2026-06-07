---
name: pdf-card-generator
description: Generates PDF cards — business cards, data cards, summary cards, flashcards, and other card-format documents — using libraries like Puppeteer, Playwright, jsPDF, or PDFKit. Use this skill when the user asks to create a PDF in a card or tile format, export data as cards, or produce printable card layouts.
---

# PDF Card Generator

This skill helps you generate PDF documents formatted as cards — business cards, data summary cards, flashcards, info tiles, and other compact card-style layouts.

## When to Use This Skill

Use this skill when the user:

- Asks to generate business cards as a PDF
- Wants to export data (contacts, products, employees) as printable cards
- Needs flashcards, index cards, or study cards as a PDF
- Wants a card-grid layout (e.g., "4 cards per page") exported to PDF
- Asks to create printable name badges or ID cards
- Wants to produce summary cards from a dataset or JSON

## Choosing the Right Tool

| Use case | Recommended library |
|---|---|
| HTML/CSS design → PDF (Node.js) | **Puppeteer** or **Playwright** |
| Pure JavaScript PDF (no browser) | **jsPDF** or **PDFKit** |
| Server-side with templates | **PDFKit** |
| React/Next.js apps | **@react-pdf/renderer** |
| Python | **ReportLab** or **WeasyPrint** |

### When to Use Puppeteer / Playwright

Best choice when the card design is complex or already expressed in HTML/CSS. Renders pixel-perfect output matching browser rendering.

```bash
npm install puppeteer
# or
npm install playwright
```

### When to Use jsPDF

Best choice for lightweight, browser-compatible PDF generation with no server dependency.

```bash
npm install jspdf
```

### When to Use PDFKit

Best choice for server-side Node.js scripts that draw cards programmatically without a browser.

```bash
npm install pdfkit
```

## Implementation Patterns

### Pattern 1 — HTML/CSS Cards via Puppeteer (recommended for styled cards)

Design each card as an HTML element, then use Puppeteer to render and export.

```ts
import puppeteer from 'puppeteer';

interface Card {
  name: string;
  title: string;
  email: string;
  phone: string;
}

async function generateCardsPDF(cards: Card[], outputPath: string) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: white; }
        .page {
          width: 210mm;
          padding: 10mm;
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 8mm;
        }
        .card {
          width: 85mm;
          height: 55mm;
          border: 1px solid #ddd;
          border-radius: 4mm;
          padding: 6mm;
          display: flex;
          flex-direction: column;
          justify-content: center;
          background: linear-gradient(135deg, #f8f9fa, #ffffff);
          page-break-inside: avoid;
        }
        .name { font-size: 14pt; font-weight: bold; color: #1a1a2e; }
        .title { font-size: 9pt; color: #555; margin-top: 2mm; }
        .contact { font-size: 8pt; color: #333; margin-top: 4mm; }
      </style>
    </head>
    <body>
      <div class="page">
        ${cards
          .map(
            (c) => `
          <div class="card">
            <div class="name">${c.name}</div>
            <div class="title">${c.title}</div>
            <div class="contact">${c.email}<br>${c.phone}</div>
          </div>
        `,
          )
          .join('')}
      </div>
    </body>
    </html>
  `;

  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });

  await browser.close();
}
```

### Pattern 2 — Programmatic Cards via PDFKit (no browser required)

Draw each card as a rectangle with text, arranged in a grid.

```ts
import PDFDocument from 'pdfkit';
import fs from 'fs';

interface Card {
  title: string;
  value: string;
  subtitle?: string;
}

function generateCardsPDF(cards: Card[], outputPath: string) {
  const doc = new PDFDocument({ size: 'A4', margin: 0 });
  doc.pipe(fs.createWriteStream(outputPath));

  // Card dimensions in points (1mm ≈ 2.835pt)
  const CARD_W = 243; // ~85mm
  const CARD_H = 156; // ~55mm
  const MARGIN = 28;  // ~10mm
  const GAP = 14;     // ~5mm
  const COLS = 2;

  cards.forEach((card, i) => {
    const col = i % COLS;
    const row = Math.floor(i / COLS);

    // Start a new page every 5 rows
    if (i > 0 && col === 0 && row % 5 === 0) {
      doc.addPage();
    }

    const x = MARGIN + col * (CARD_W + GAP);
    const y = MARGIN + (row % 5) * (CARD_H + GAP);

    // Card background
    doc
      .roundedRect(x, y, CARD_W, CARD_H, 8)
      .fillAndStroke('#f8f9fa', '#cccccc');

    // Title
    doc
      .fillColor('#1a1a2e')
      .fontSize(14)
      .font('Helvetica-Bold')
      .text(card.title, x + 12, y + 18, { width: CARD_W - 24 });

    // Value
    doc
      .fillColor('#333333')
      .fontSize(22)
      .font('Helvetica-Bold')
      .text(card.value, x + 12, y + 50, { width: CARD_W - 24 });

    // Subtitle
    if (card.subtitle) {
      doc
        .fillColor('#666666')
        .fontSize(9)
        .font('Helvetica')
        .text(card.subtitle, x + 12, y + 90, { width: CARD_W - 24 });
    }
  });

  doc.end();
}
```

### Pattern 3 — Flashcards via jsPDF (browser-friendly)

```ts
import jsPDF from 'jspdf';

interface Flashcard {
  front: string;
  back: string;
}

function generateFlashcardsPDF(cards: Flashcard[], filename: string) {
  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });

  cards.forEach((card, i) => {
    if (i > 0) doc.addPage();

    // Front side
    doc.setFillColor(240, 248, 255);
    doc.roundedRect(10, 10, 130, 90, 5, 5, 'F');
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text('FRONT', 15, 20);
    doc.setFontSize(18);
    doc.setTextColor(20);
    doc.text(card.front, 75, 55, { align: 'center', maxWidth: 120 });

    // Back side
    doc.setFillColor(255, 248, 240);
    doc.roundedRect(150, 10, 130, 90, 5, 5, 'F');
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text('BACK', 155, 20);
    doc.setFontSize(14);
    doc.setTextColor(20);
    doc.text(card.back, 215, 55, { align: 'center', maxWidth: 120 });
  });

  doc.save(filename);
}
```

## Card Layout Tips

### Standard card sizes

| Card type | Size |
|---|---|
| Business card | 85 × 55 mm (3.5 × 2 in) |
| Index / flashcard | 127 × 76 mm (5 × 3 in) |
| ID badge | 85.6 × 54 mm (CR80) |
| Postcard | 148 × 105 mm (A6) |

### Grid layouts on A4

| Cards per page | Grid | Card size |
|---|---|---|
| 8 | 2 × 4 | 85 × 55 mm |
| 10 | 2 × 5 | 85 × 50 mm |
| 4 | 2 × 2 | 100 × 70 mm |

### Print-ready settings

- Set bleed area of 3mm on each edge for professional print
- Use 300 DPI equivalent resolution for raster images
- Embed fonts to ensure cross-platform rendering
- Use CMYK colors for offset printing; RGB is fine for digital/inkjet

## Handling Data Sources

When generating cards from data, parse the source first:

```ts
// From JSON
const cards = JSON.parse(fs.readFileSync('data.json', 'utf8'));

// From CSV (with csv-parse)
import { parse } from 'csv-parse/sync';
const cards = parse(fs.readFileSync('data.csv'), { columns: true });

// From an API response
const response = await fetch('https://api.example.com/items');
const cards = await response.json();
```

## Common Pitfalls

- **Text overflow**: Always set `maxWidth` or truncate long strings before rendering
- **Font embedding**: In PDFKit, register custom fonts with `doc.registerFont()` before use
- **Page breaks**: In Puppeteer, use `page-break-inside: avoid` on card elements
- **Memory**: For large card sets (1000+), generate in batches and merge PDFs with `pdf-lib`
- **Async Puppeteer**: Always `await browser.close()` in a `finally` block to avoid zombie processes

## Merging Multiple PDFs

When generating cards in batches, merge with `pdf-lib`:

```bash
npm install pdf-lib
```

```ts
import { PDFDocument } from 'pdf-lib';
import fs from 'fs';

async function mergePDFs(paths: string[], outputPath: string) {
  const merged = await PDFDocument.create();
  for (const path of paths) {
    const pdf = await PDFDocument.load(fs.readFileSync(path));
    const pages = await merged.copyPages(pdf, pdf.getPageIndices());
    pages.forEach((page) => merged.addPage(page));
  }
  fs.writeFileSync(outputPath, await merged.save());
}
```
