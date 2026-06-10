---
name: google-dorks
description: Builds and explains Google dork queries (advanced search operators) for OSINT, asset discovery, and authorized security reconnaissance. Use when the user asks for "google dorks", "dorking", footprinting a domain/company via search engines, or finding exposed files, login panels, open directories, leaked configs, or other public-data exposure through search operators.
---

# Google Dorks

Helps build precise Google search queries ("dorks") using advanced search
operators to map a target's public footprint: exposed files, admin/login
panels, open directories, leaked configs, subdomains, cloud buckets, and
more.

## Scope and Ethics (read first)

Google dorking is a passive reconnaissance technique — it only surfaces what
search engines have already indexed. It is widely used for:

- Bug bounty / penetration testing recon (within authorized scope)
- OSINT investigations
- Auditing your own organization's exposure ("attack surface review")
- CTF challenges and security education

**Before generating target-specific dorks**, confirm the user is querying a
domain/asset they own or are explicitly authorized to test (e.g. it's in
their bug bounty scope, pentest engagement, or CTF). If authorization is
unclear, say so and either keep examples generic/educational or ask for
confirmation. Never suggest accessing, downloading, or exploiting data found
this way — the goal is to identify and report exposure, not to exfiltrate it.

## Step 1: Gather Context

If not already provided, ask the user for:

- **Target**: domain, company name, or asset (e.g. `example.com`)
- **Authorization**: their own asset, bug bounty scope, pentest engagement, or CTF
- **Objective**: what they want to find — general recon, exposed files,
  login portals, subdomains, leaked credentials, specific file types, PII, etc.

## Step 2: Operator Reference

| Operator | Purpose | Example |
|---|---|---|
| `site:` | Restrict to a domain/subdomain | `site:example.com` |
| `inurl:` | Term must appear in the URL | `inurl:admin` |
| `allinurl:` | All terms must appear in the URL | `allinurl:wp-content uploads` |
| `intitle:` | Term must appear in the page title | `intitle:"index of"` |
| `allintitle:` | All terms must appear in the title | `allintitle:admin login` |
| `intext:` / `allintext:` | Term(s) in the page body | `intext:"sql syntax"` |
| `filetype:` / `ext:` | Restrict to a file extension | `filetype:pdf` |
| `cache:` | Show Google's cached version of a page | `cache:example.com` |
| `related:` | Sites related to a domain | `related:example.com` |
| `"exact phrase"` | Match an exact phrase | `"internal use only"` |
| `-term` | Exclude a term | `-inurl:www` |
| `*` | Wildcard placeholder | `intitle:"index of" "*.env"` |
| `OR` / `\|` | Either term matches | `filetype:sql OR filetype:bak` |
| `..` | Numeric range | `budget 2020..2024` |
| `before:` / `after:` | Date-bounded results | `after:2023-01-01` |

Combine operators with parentheses and `OR`/`-` to narrow or broaden results,
e.g. `site:example.com (filetype:sql OR filetype:bak OR filetype:db)`.

## Step 3: Dork Templates by Category

Replace `{domain}` with the target domain and `{org}` with the company name
(used for cloud-bucket and document searches where a literal domain doesn't
appear).

### Open directories / index listings
```
site:{domain} intitle:"index of"
intitle:"index of" "{domain}"
intitle:"index of" intext:"backup"
```

### Login & admin panels
```
site:{domain} inurl:login
site:{domain} (inurl:admin OR inurl:administrator OR inurl:wp-admin OR inurl:cpanel)
site:{domain} intitle:"login" (inurl:admin OR inurl:portal OR inurl:dashboard)
```

### Exposed files & backups
```
site:{domain} (filetype:sql OR filetype:bak OR filetype:db OR filetype:dump)
site:{domain} (filetype:log OR filetype:env OR filetype:ini OR filetype:conf OR filetype:cfg)
site:{domain} ext:zip OR ext:tar OR ext:tar.gz OR ext:rar
```

### Credentials & secrets
```
site:{domain} (filetype:env OR filetype:yml OR filetype:json) (intext:"PASSWORD" OR intext:"API_KEY" OR intext:"SECRET")
site:{domain} filetype:xml (inurl:wp-config OR intext:"DB_PASSWORD")
site:{domain} intext:"BEGIN PRIVATE KEY" OR intext:"BEGIN RSA PRIVATE KEY"
```

### Error messages & tech fingerprinting
```
site:{domain} intext:"SQL syntax near" OR intext:"Warning: mysql_" OR intext:"valid MySQL result"
site:{domain} intext:"Fatal error" OR intext:"stack trace" OR intext:"Exception in thread"
site:{domain} intitle:"phpinfo()" "PHP Version"
```

### Subdomains & related assets
```
site:*.{domain} -site:www.{domain}
site:{domain} -inurl:www
```

### Cloud storage buckets
```
site:s3.amazonaws.com "{org}"
site:storage.googleapis.com "{org}"
site:blob.core.windows.net "{org}"
intitle:"index of" "{org}" (site:s3.amazonaws.com OR site:storage.googleapis.com)
```

### Office documents & PII
```
site:{domain} (filetype:xls OR filetype:xlsx OR filetype:csv) (intext:"email" OR intext:"password" OR intext:"@{domain}")
site:{domain} (filetype:doc OR filetype:docx OR filetype:pdf) (intext:"confidential" OR intext:"internal use only")
```

### Exposed cameras / IoT (generic, not domain-bound)
```
intitle:"webcamXP" inurl:8080
intitle:"Network Camera" inurl:"view/index"
```

## Step 4: Assemble and Present

1. Pick the categories that match the user's objective.
2. Substitute `{domain}` / `{org}` with the confirmed target.
3. Present each dork as a ready-to-paste query, with a one-line note on what
   it's looking for.
4. Suggest tightening with `-` exclusions or `before:`/`after:` if results
   are too noisy, and broadening with `OR` if too narrow.
5. Remind the user to verify findings manually and report exposed sensitive
   data through proper disclosure channels rather than downloading it.

## Resources

- Google Hacking Database (GHDB): https://www.exploit-db.com/google-hacking-database
- Google's advanced search operators documentation
