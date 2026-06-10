# Digital Footprint: Domains, Search Dorking & Social Media (Spain)

## `.es` Domain & Infrastructure Reconnaissance

- **WHOIS** — query via https://www.dominios.es (official NIC.es registry) or any standard
  WHOIS/RDAP client. Personal registrant data is usually redacted under GDPR; organizational
  registrants often remain visible (registrant name, NIF, contact email).
- **DNS records** — standard `dig`/`nslookup`/RDAP queries reveal mail providers (MX),
  hosting (A/AAAA → reverse IP/ASN lookup via RIPE), and SPF/DMARC records that can hint at
  the email infrastructure a Spanish org uses.
- **Certificate Transparency** — search https://crt.sh for a domain to enumerate subdomains
  and historical certificates issued for `*.es` or corporate domains.
- **ASN / IP ownership** — for IPs in Spanish ranges, query the RIPE database
  (https://apps.db.ripe.net) by organization name to find associated netblocks and abuse
  contacts.
- **Wayback Machine** — https://web.archive.org — historical snapshots of a Spanish company's
  website (old staff pages, contact info, pricing, leaked documents previously linked).

## Search Engine Dorking Patterns

Replace `<term>` with the name, company, email, or phone number being investigated. Use
quotes for exact phrases. These work with Google, Bing, or DuckDuckGo:

- `"<full name>" site:linkedin.com/in` — professional profile
- `"<full name>" (Twitter OR X.com OR Instagram OR Facebook)`
- `site:*.es "<company name>" filetype:pdf` — official documents, tenders, annual reports
  hosted on Spanish domains
- `"<company name>" site:boe.es` — official gazette mentions (incorporation, insolvency,
  subsidies)
- `"<NIF/CIF>"` — direct search for the tax ID often surfaces invoices, contracts, or
  procurement records that reference it
- `"<email>"` — find data breach mentions, forum posts, or business listings using that
  address
- `intitle:"curriculum" "<full name>"` — publicly posted CVs (common on Spanish university
  and association sites)

## Social Media & Community Platforms Common in Spain

- **LinkedIn** — primary professional network; search by name + region (e.g., "Madrid,
  Comunidad de Madrid, España") to disambiguate common Spanish surnames.
- **X (Twitter) / Instagram / Facebook / TikTok** — standard personal/brand presence.
  Spanish users frequently include their city or autonomous community in bios.
- **Forocoches** — large general-interest forum; historically a source for leaked or
  self-disclosed personal information in older threads — search via `site:forocoches.com`.
- **InfoJobs** — https://www.infojobs.net — Spain's largest job board; public company
  profiles list employee counts, reviews, and sometimes HR contact details.
- **Glassdoor / Indeed España** — employee reviews and salary data for Spanish companies.

## Reverse Image Search

Use Google Images, Yandex Images, and TinEye to check whether a profile photo is reused
across multiple accounts/sites — a common technique for verifying or debunking an identity.

## Geolocation & Property Visualization

- **Catastro map viewer** — https://www1.sedecatastro.gob.es includes a cartographic viewer
  to visually confirm a parcel matches an address or satellite imagery.
- **Google Maps / Street View** — corroborate a registered business address (signage,
  building type) against registry data.

## Putting It Together

A typical workflow for a Spanish company:

1. Confirm the CIF format (`reference/identifiers.md`) and look it up on AEAT's census tool.
2. Search BORME for the company name to find incorporation date, registered address, and
   directors/administrators.
3. Search BOE for any insolvency ("concurso de acreedores") or sanction notices.
4. Check `contrataciondelestado.es` and `infosubvenciones.es` for public money received.
5. Look up the company's domain (WHOIS, DNS, Wayback Machine) and LinkedIn page for digital
   footprint and key personnel.
6. Cross-check named individuals against professional colegio directories if relevant
   (lawyers, architects, doctors, etc.).
7. Compile findings with source links and retrieval dates.
