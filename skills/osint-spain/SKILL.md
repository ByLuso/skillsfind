---
name: osint-spain
description: Provides methodology, public registries, and identifier-validation techniques for open-source intelligence (OSINT) research focused on Spain. Use when investigating Spanish individuals, companies, properties, court cases, domains, or social media footprints for due diligence, fraud/background checks, journalism, or authorized security research.
---

# OSINT Spain

Methodology and a curated map of Spanish open data sources for conducting open-source
intelligence (OSINT) research on people, companies, properties, legal proceedings, and
digital assets located in Spain.

## When to Use This Skill

Use this skill when a user needs to:

- Research a Spanish company: ownership, directors, financial filings, registered address
- Verify or look up a Spanish identifier (DNI, NIE, CIF/NIF, IBAN, vehicle plate)
- Find property/ownership information via the Spanish Land Registry (Catastro)
- Search Spanish court rulings, insolvency notices, or official gazette publications
- Investigate a `.es` domain or Spanish-hosted infrastructure
- Build a profile of a Spanish person or organization from public social media and media
  archives
- Conduct due diligence, background checks, fraud investigation, journalism research, or
  authorized security/penetration-testing reconnaissance involving Spanish targets

## Legal & Ethical Boundaries — Read First

- **Only public, lawfully-accessible sources.** Spain enforces the GDPR plus the national
  LOPDGDD (Ley Orgánica 3/2018). The municipal *padrón* (residents' register), DNI photos,
  health, and tax records are **not** public — do not suggest scraping or social-engineering
  these.
- **Use official channels** for anything requiring identity verification (e.g., AEAT's NIF
  checker, Catastro's "datos no protegidos" mode) rather than third-party scrapers.
- **State the purpose.** Confirm the user has a legitimate basis (due diligence, journalism,
  authorized pentest/recon, personal background check on a counterparty, academic research).
  Refuse or push back if the request looks like stalking, harassment, doxxing, or unauthorized
  surveillance of a private individual.
- **Cite sources.** Every fact pulled from a registry should be attributed to that registry and
  dated, since company/property data changes over time.

## Workflow

1. **Scope the target.** Identify what you have (full name, company name, NIF/CIF, domain,
   address, phone) and what you're trying to learn (ownership, solvency, identity, location,
   digital footprint).
2. **Validate identifiers first.** If a DNI/NIE/CIF/IBAN/plate is provided, check its format
   and checksum (see `reference/identifiers.md`) before searching — a malformed ID means the
   source data is wrong or fabricated.
3. **Query official registries** relevant to the target type (see table below and
   `reference/registries.md` for the full catalogue).
4. **Cross-reference** with news archives, professional colegio directories, and procurement/
   subsidy databases to corroborate or expand findings.
5. **Build the digital footprint** using domain/WHOIS lookups and social media search
   techniques (`reference/social-and-web.md`).
6. **Synthesize**: present findings with source + retrieval date for each claim, flag
   contradictions, and note what could *not* be verified through public sources.

## Quick Reference: Core Spanish OSINT Sources

| Need | Source | URL |
| --- | --- | --- |
| Laws, official notices, insolvency/bankruptcy notices | BOE (Boletín Oficial del Estado) | https://www.boe.es |
| Company registrations, appointments, dissolutions | BORME (Boletín Oficial del Registro Mercantil) | https://www.boe.es/borme/ |
| Company name search & certificates | Registro Mercantil Central (RMC) | https://www.rmc.es |
| Property/cadastral data by address or reference | Sede Electrónica del Catastro | https://www1.sedecatastro.gob.es |
| Court rulings & case law search | CENDOJ / Poder Judicial | https://www.poderjudicial.es |
| NIF/CIF validation, tax census | Agencia Tributaria (AEAT) | https://sede.agenciatributaria.gob.es |
| `.es` domain WHOIS | Red.es / NIC.es | https://www.dominios.es |
| Government contracts | Plataforma de Contratación del Sector Público | https://contrataciondelestado.es |
| Public subsidies/grants | Base de Datos Nacional de Subvenciones (BDNS) | https://www.infosubvenciones.es |
| Public sector transparency, salaries, agendas | Portal de Transparencia | https://transparencia.gob.es |
| Professional licensing (lawyers, doctors, architects, etc.) | Colegios profesionales (per-province) | varies — see reference |

For the full catalogue (regional registries, vehicle/traffic data, intellectual property,
press archives, etc.), see `reference/registries.md`.

## Detailed References

- **`reference/registries.md`** — exhaustive, categorized list of Spanish public registries,
  databases, and portals (corporate, judicial, property, regional, IP, press archives,
  procurement, sanctions).
- **`reference/identifiers.md`** — format specs and checksum/validation algorithms for DNI,
  NIE, CIF/NIF, Spanish IBAN, Social Security number (NUSS), and vehicle plates.
- **`reference/social-and-web.md`** — techniques for `.es` domain/IP reconnaissance, search
  engine dorking patterns, and finding Spanish social media, professional, and news profiles.
