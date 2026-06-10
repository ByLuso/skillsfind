---
name: google-dorks
description: Provides methodology and a reference for advanced search-engine operators ("Google dorking") used in OSINT, reconnaissance, and security research — finding exposed files, misconfigured services, subdomains, and information disclosure. Use for authorized penetration tests, bug bounty recon, attack-surface/exposure audits of your own organization, and OSINT investigations.
---

# Google Dorks (Advanced Search Operators)

Methodology and reference for using advanced search-engine operators — commonly called
"Google dorks" — to find publicly indexed information that is useful for security research,
reconnaissance, and OSINT.

## When to Use This Skill

Use this skill when a user needs to:

- Enumerate subdomains, login portals, or technology stack of a target during **authorized**
  penetration testing or bug bounty recon
- Audit their **own organization's** external exposure (leaked documents, exposed admin
  panels, open directory listings, misconfigured cloud storage)
- Find publicly indexed documents/pages about a person, company, or domain as part of a
  broader OSINT investigation (pairs well with the `osint-spain` skill for `.es` targets)
- Build a Google Hacking Database (GHDB)-style query for a specific exposure class

## Legal & Ethical Boundaries — Read First

- **Searching is (generally) legal; accessing what you find may not be.** A search engine
  surfacing a URL does not authorize you to access, download, or use the data behind it.
  Accessing systems or data without authorization can violate computer-misuse laws (e.g.
  Spain's Código Penal arts. 197/197 bis, the EU NIS framework, the US CFAA) even if the URL
  was "just sitting there indexed."
- **Stay in scope.** For pentests/bug bounties, only query for and interact with assets
  explicitly covered by the engagement's scope and rules of engagement.
- **Self-audits are the safest use case.** Running these queries against `site:yourdomain.com`
  to find what *you've* accidentally exposed — and then fixing it — is the lowest-risk,
  highest-value application.
- **Don't harvest or redistribute personal data** found this way (PII, credentials, leaked
  documents). If you discover a real exposure of sensitive data belonging to a third party,
  the appropriate action is responsible disclosure to the asset owner, not collection.

## Workflow

1. **Define the target and goal**: a domain, organization name, or person — and what kind of
   exposure you're looking for (documents, login pages, subdomains, cloud storage, etc.).
2. **Start broad** with `site:` to scope every query to the target domain (or `site:*.es` /
   `site:*.<tld>` for a wider sweep).
3. **Layer operators** (see `reference/operators.md`) to narrow by file type, URL pattern,
   page title, or content.
4. **Use recipe categories** (`reference/dork-recipes.md`) for known exposure classes:
   exposed documents, directory listings, login/admin panels, config/credential files, cloud
   storage buckets, error pages revealing stack info.
5. **Pivot to specialized search engines** (`reference/other-platforms.md`) for what Google
   doesn't index well: Shodan/Censys for internet-facing services and banners, GitHub code
   search for leaked secrets in repositories.
6. **Document and remediate**: for each finding, record the query used, the URL, why it's
   sensitive, and — if it's your own asset — the remediation (remove/restrict the file,
   `robots.txt`/`noindex`, request de-indexing via Google Search Console's Removals tool).

## Quick Reference: Core Operators

| Operator | Purpose | Example |
| --- | --- | --- |
| `site:` | Restrict to a domain/subdomain | `site:example.com` |
| `inurl:` | Term must appear in the URL | `inurl:admin` |
| `intitle:` | Term must appear in the page title | `intitle:"index of"` |
| `intext:` | Term must appear in the page body | `intext:"sql syntax error"` |
| `filetype:` / `ext:` | Restrict to a file extension | `filetype:pdf` |
| `"exact phrase"` | Exact match | `"confidential — internal use only"` |
| `-term` | Exclude results containing term | `site:example.com -www` |
| `OR` / `\|` | Either term | `inurl:login OR inurl:signin` |
| `*` | Wildcard placeholder | `"* password" filetype:env` |
| `..` | Numeric range | `"invoice" 2020..2024` |
| `before:` / `after:` | Date-restrict (Google) | `after:2023-01-01` |

See `reference/operators.md` for the full list, syntax differences across Google/Bing/DuckDuckGo,
and combination tips.

## Detailed References

- **`reference/operators.md`** — full operator syntax reference across Google, Bing, and
  DuckDuckGo, plus combination patterns.
- **`reference/dork-recipes.md`** — categorized GHDB-style query recipes: exposed documents,
  directory listings, login portals, configuration/credential files, cloud storage buckets,
  error messages and version disclosure.
- **`reference/other-platforms.md`** — beyond web search: Shodan, Censys, and GitHub/GitLab
  code-search "dorking" for internet-facing services and leaked secrets in source code.
