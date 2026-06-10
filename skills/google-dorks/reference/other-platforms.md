# Beyond Google: Other Dorking Surfaces

Web search engines only index what's crawlable over HTTP(S) and allowed by `robots.txt`.
For full attack-surface visibility, combine dorking with these specialized search engines.

## Shodan

Shodan (https://www.shodan.io) indexes banners and metadata from internet-facing devices and
services (routers, IoT, industrial control systems, databases, web servers) gathered via its
own internet-wide scanning — not web crawling.

Useful filters (require a free/paid account for full results):

- `org:"<organization name>"` — assets registered to an org
- `hostname:<domain>` — assets resolving to a domain
- `net:<CIDR>` — assets within an IP range
- `port:<port>` — assets exposing a specific port
- `product:"<software name>"` — assets running specific software (e.g. `product:"MongoDB"`)
- `country:ES` / `city:Madrid` — geographic filters (useful for Spain-focused recon)
- `ssl:"<domain>"` — find hosts presenting a certificate for a domain, even on non-standard
  IPs/ports

Combine: `org:"<organization name>" port:3389` to find exposed RDP, or
`org:"<organization name>" product:nginx` to fingerprint web infrastructure.

## Censys

Censys (https://search.censys.io) is similar to Shodan — internet-wide scan data with a
powerful query language. Useful for certificate-based pivoting:
`services.tls.certificates.leaf_data.subject.organization:"<organization name>"` to find all
hosts presenting certificates issued to an org, regardless of hostname.

## FOFA / ZoomEye

Chinese-origin equivalents (https://fofa.info, https://www.zoomeye.org) with their own query
syntax (`app=`, `title=`, `host=`, `org=`). Useful for coverage of assets that may not be
well-indexed by Shodan/Censys, particularly in APAC.

## GitHub / GitLab Code Search ("GitHub Dorking")

Source code repositories frequently leak credentials, internal hostnames, and configuration.
GitHub's code search (https://github.com/search) supports qualifiers:

- `org:<org-name> password`
- `org:<org-name> filename:.env`
- `"<company domain>" extension:yml password`
- `"<internal hostname or API key prefix>"`

Note: GitHub code search syntax and coverage change over time, and secret-scanning by GitHub
itself now flags many common credential patterns automatically — if you're auditing your own
org, also enable GitHub's secret scanning and push protection rather than relying solely on
manual dorking.

## Wayback Machine / Common Crawl

- **Wayback Machine** (https://web.archive.org) — historical snapshots can reveal previously
  exposed pages, old contact info, or removed admin links that are no longer live but were
  once indexed.
- **Common Crawl** (https://commoncrawl.org) — large-scale open web crawl datasets; useful
  for bulk analysis of a domain's historical content if you need to search at scale
  programmatically.

## Choosing the Right Tool

| Goal | Best tool |
| --- | --- |
| Find indexed documents/pages on a domain | Google / Bing dorking |
| Find internet-facing services, banners, open ports | Shodan / Censys |
| Find leaked secrets in source code | GitHub/GitLab code search + secret scanning |
| Find historical/removed content | Wayback Machine |
| Bulk/offline analysis across many sites | Common Crawl |
