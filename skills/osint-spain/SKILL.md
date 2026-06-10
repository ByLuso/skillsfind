---
name: osint-spain
description: OSINT (Open Source Intelligence) toolkit and methodology focused on Spain — public registries, company/business records, property/cadastre, judicial and official gazettes, people search, phone/domain lookups, and image/social-media verification using Spanish-specific sources (BOE, BORME, Catastro, INE, Colegios Profesionales, etc.). Use when the user asks for OSINT, investigación, due diligence, verificación de personas/empresas, antecedentes, or research using Spanish public records.
---

# OSINT España

A methodology and source reference for open-source investigations focused on
Spain: people, companies, properties, official records, domains, phone
numbers, and images.

## Scope and Ethics (read first)

OSINT relies entirely on **publicly available** information, but "public" is
not the same as "fair game." In Spain, processing personal data is governed
by the **RGPD/GDPR** and the **LOPDGDD** (Ley Orgánica 3/2018). Legitimate
uses include journalism, due diligence/KYC, fraud and scam prevention,
security research, academic/genealogical research, and verifying claims made
by businesses or individuals.

- Confirm the **purpose** before digging into a private individual: due
  diligence on a counterparty, verifying a public figure/company, your own
  digital footprint, etc.
- **Decline or push back** if the goal looks like stalking, harassment,
  doxxing, or building a profile on someone without a legitimate reason.
- Prefer **official/primary sources** (registries, gazettes) over scraped
  aggregators when accuracy matters.
- Respect data minimization: collect only what's needed for the stated
  purpose, and don't republish sensitive personal data.
- For Google search-operator recon (site-specific dorks, exposed files,
  subdomains), pair this skill with the **google-dorks** skill.

## Step 1: Define the Target and Objective

Ask (if not already clear):

- **Target type**: person, company/organization, domain/infrastructure,
  property, phone number, vehicle, or a specific document/legal record.
- **Identifiers available**: full name, NIF/NIE/CIF, domain, phone, address,
  username/handle, etc.
- **Purpose**: what decision or question this research supports.

## Step 2: Source Reference by Category

### Personas (People)

- **Redes sociales**: LinkedIn, X/Twitter, Instagram, Facebook, TikTok —
  use each platform's advanced search and `site:` dorks for cached/indexed
  profiles.
- **Username/handle correlation**: tools like Sherlock, Maigret, or
  WhatsMyName check a username across many platforms at once.
- **Directorios**: paginasamarillas.es / paginasblancas.es, 11888.es —
  landline listings by name and address.
- **Colegios profesionales** (verify professional credentials):
  - Abogacía: Consejo General de la Abogacía Española (abogacia.es) — lawyer
    registration lookup ("censo de letrados").
  - Medicina: Consejo General de Colegios Oficiales de Médicos (cgcom.es).
  - Notarios: Consejo General del Notariado (notariado.org).
  - Economistas/Auditores: Consejo General de Economistas (economistas.es).
- **BOE** (boe.es): full-text search for official appointments,
  oposiciones/concursos, subvenciones, condecoraciones, naturalizaciones, and
  **edictos judiciales** (court notices) by name.
- **Sede Judicial Electrónica** (sedejudicial.justicia.es): public judicial
  notices and edicts.

### Empresas (Companies / Business)

- **BORME** — Boletín Oficial del Registro Mercantil
  (borme.registradores.org): incorporations, dissolutions, director/admin
  appointments, capital changes, mergers — searchable free of charge.
- **Registro Mercantil Central** (rmc.es): company name search, links to
  provincial registries for "notas simples" (paid).
- **Free company reports**: e-informa.com, axesor.es, einforma.com —
  administrators, financial summaries, CNAE activity codes, related
  companies.
- **datos.gob.es**: open government data — public contracts, subsidies,
  grants awarded to a company.
- **Plataforma de Contratación del Sector Público**
  (contrataciondelestado.es): public tenders and awards.
- **CIF validation**: Spanish tax ID (CIF) has a check-digit algorithm — use
  it to validate a CIF format before trusting a document/listing.
- **Boletines Oficiales autonómicos** (BOCM, DOGC, BOJA, BOPV, etc.): regional
  subsidies, sanctions, and appointments not in the BOE.

### Inmuebles y Catastro (Property)

- **Sede Electrónica del Catastro** (sede.catastro.gob.es): free lookup of a
  property's cadastral reference, surface area, use, and cartography by
  address or reference number.
- **Idealista / Fotocasa**: current and historical listings (price history
  via Wayback Machine snapshots).
- **Registro de la Propiedad** (registradores.org): "nota simple" (paid,
  identifies registered owner and charges).

### Dominios e Infraestructura (Domains/Infra)

- **.es domains**: dominios.es / sede.nic.es for registration status (WHOIS
  data is largely redacted under GDPR; registrant contact may not be public).
- **General recon**: WHOIS, DNS records, crt.sh (certificate transparency),
  Shodan/Censys for exposed services, Wayback Machine / archive.today for
  historical site snapshots.
- For Google-indexed exposure (open directories, leaked files, subdomains),
  use the **google-dorks** skill with `site:` scoped to the target domain.

### Teléfonos (Phone Numbers)

- **Reverse lookup / spam check**: listaspam.com, responderono.es,
  elnumero.es — community-reported caller info.
- **Operator identification**: CNMC's national numbering plan maps prefixes
  to assigned operators (useful for spotting spoofed/VoIP numbers).

### Vehículos (Vehicles)

- DGT vehicle/owner records are **not public** — accessing them requires a
  legitimate interest recognized by law (insurer, law enforcement, the owner
  themselves via "informe del vehículo" on sede.dgt.gob.es). Do not suggest
  workarounds to access restricted vehicle-owner data.

### Documentos Oficiales / Transparencia

- **BOE** (boe.es): full-text search across all state gazette publications
  since 1960.
- **Boletines autonómicos**: BOCM (Madrid), DOGC (Cataluña), BOJA (Andalucía),
  BOPV (País Vasco), etc. — each has its own searchable portal.
- **Portal de Transparencia** (transparencia.gob.es): government contracts,
  subsidies, senior official declarations of assets/interests.
- **Congreso/Senado**: registro de intereses and biographies of elected
  officials.

### Imágenes y Geolocalización

- **Reverse image search**: Google Lens, Yandex, TinEye — find where an image
  has appeared before.
- **Geolocation**: Google Street View / Mapillary to match landmarks; EXIF
  metadata (when present) for camera/GPS info; SunCalc for shadow-based time
  estimation.

## Step 3: Workflow

1. Clarify target type, available identifiers, and legitimate purpose.
2. Start from **official/primary sources** (BOE, BORME, Catastro, Colegios
   profesionales) before aggregators.
3. Cross-reference at least two independent sources before treating a fact as
   confirmed.
4. Use the **google-dorks** skill for search-engine-based discovery
   (`site:`, `filetype:`, `intitle:"index of"`, etc.) on domains/companies.
5. Keep a source log (URL + date accessed) for traceability — official
   registries are periodically updated and snapshots can change.
6. Summarize findings with sources; flag anything that required a paid/
   restricted-access report rather than open data.

## Resources

- BOE: https://www.boe.es
- BORME: https://www.borme.registradores.org
- Sede Electrónica del Catastro: https://www1.sedecatastro.gob.es
- Sede Judicial Electrónica: https://sedejudicial.justicia.es
- Portal de Transparencia: https://transparencia.gob.es
- datos.gob.es: https://datos.gob.es
