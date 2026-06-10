# Dork Recipes by Category

Generic, reusable query patterns grouped by what they're useful for. Replace
`<domain>`/`<keyword>` with your authorized target. These mirror the categories used by the
Google Hacking Database (GHDB, part of Exploit-DB) — consult it directly for an exhaustive,
continuously-updated list: https://www.exploit-db.com/google-hacking-database

## 1. Exposed Documents

Find spreadsheets, presentations, and PDFs that may contain sensitive internal data:

- `site:<domain> filetype:xlsx OR filetype:csv OR filetype:pdf`
- `site:<domain> intext:"confidential" filetype:pdf`
- `site:<domain> (intitle:"employee directory" OR intitle:"phone list")`
- `site:<domain> filetype:doc OR filetype:docx intext:"password"`

## 2. Directory Listings

Misconfigured web servers sometimes expose raw directory listings instead of an index page:

- `intitle:"index of" site:<domain>`
- `intitle:"index of" "parent directory" site:<domain>`
- `intitle:"index of" (backup OR bak OR old OR archive) site:<domain>`

## 3. Login & Admin Portals (Attack Surface Mapping)

Identify exposed administrative interfaces — useful for inventorying attack surface during an
authorized assessment, not for credential attacks:

- `site:<domain> (inurl:login OR inurl:signin OR inurl:admin OR inurl:portal)`
- `site:<domain> intitle:"login" OR intitle:"sign in"`
- `site:<domain> inurl:wp-admin` (WordPress)
- `site:<domain> inurl:phpmyadmin` (database admin panels)

## 4. Configuration & Credential Files

Common filenames/extensions that should never be web-accessible. Their presence in a search
index is itself a finding (the file is exposed) — do not open files containing live secrets
that belong to a third party:

- `site:<domain> ext:env OR ext:ini OR ext:conf OR ext:cfg`
- `site:<domain> filetype:sql intext:"INSERT INTO"`
- `site:<domain> filetype:log intext:"password"`
- `site:<domain> inurl:wp-config.php`
- `site:<domain> ext:bak OR ext:swp OR ext:old OR ext:orig`

## 5. Cloud Storage & Object Storage Buckets

Misconfigured cloud storage is one of the most common real-world exposure classes:

- `site:s3.amazonaws.com "<company name>"`
- `site:storage.googleapis.com "<company name>"`
- `site:blob.core.windows.net "<company name>"`
- `intitle:"index of" inurl:s3 "<company name>"`

For a thorough sweep, dedicated bucket-enumeration tools (which brute-force common naming
patterns rather than relying on search indexing) are more effective than dorking alone.

## 6. Error Messages & Technology Disclosure

Verbose error pages can reveal frameworks, versions, file paths, and database details:

- `site:<domain> intext:"Warning: mysql_connect()"`
- `site:<domain> intext:"Fatal error" intext:"on line"`
- `site:<domain> intext:"Index of /" "Apache/2"`
- `site:<domain> "stack trace" filetype:log`

## 7. Subdomain & Asset Discovery

Search-engine indexes can reveal subdomains that certificate-transparency or DNS brute-force
might miss:

- `site:*.<domain> -site:www.<domain>`
- `site:<domain> -inurl:www`

Combine with certificate transparency (`crt.sh`) and DNS tooling for full coverage.

## 8. CCTV / IoT / Remote Access (Awareness Only)

GHDB documents queries that surface unauthenticated camera and device interfaces (e.g.
`intitle:"webcamXP 5"`, `inurl:"/view/index.shtml"`). These are listed here only so you
recognize them when auditing **your own** network for accidentally-exposed devices — never
access third-party devices found this way, as doing so is unauthorized access in most
jurisdictions.

## 9. People & Organization OSINT

- `"<full name>" site:linkedin.com/in`
- `"<full name>" filetype:pdf (cv OR resume OR curriculum)`
- `"<company name>" site:<domain> intitle:"org chart"`
- `"<email address>"` — find breach mentions, forum posts, registrations

## Self-Audit Checklist

For your own domain(s), periodically run:

1. `site:<domain> filetype:pdf OR filetype:doc OR filetype:xls OR filetype:csv`
2. `site:<domain> ext:env OR ext:sql OR ext:bak OR ext:log OR ext:config`
3. `intitle:"index of" site:<domain>`
4. `site:<domain> intext:"confidential" OR intext:"internal use only"`
5. `site:s3.amazonaws.com OR site:storage.googleapis.com OR site:blob.core.windows.net "<your org name>"`

For any hit that shouldn't be public: remove or restrict access to the file, add it to
`robots.txt` / a `noindex` meta tag if it must remain reachable, and request removal of the
already-indexed URL via Google Search Console's URL Removal tool.
