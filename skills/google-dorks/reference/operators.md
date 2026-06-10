# Search Operator Reference

## Google

| Operator | Meaning | Example |
| --- | --- | --- |
| `site:` | Limit to a domain or subdomain | `site:example.com`, `site:*.example.com` |
| `inurl:` | Word/phrase appears in the URL | `inurl:wp-content` |
| `allinurl:` | All terms appear in the URL | `allinurl: admin login` |
| `intitle:` | Word/phrase appears in the `<title>` | `intitle:"index of"` |
| `allintitle:` | All terms appear in the title | `allintitle: confidential report` |
| `intext:` / `inbody:` | Word/phrase appears in page body | `intext:"internal use only"` |
| `filetype:` / `ext:` | Restrict by file extension | `filetype:xlsx`, `ext:sql` |
| `"phrase"` | Exact phrase match | `"do not distribute"` |
| `-term` | Exclude term | `site:example.com -inurl:blog` |
| `OR` (or `\|`) | Logical OR | `filetype:pdf OR filetype:docx` |
| `AND` | Logical AND (often implicit) | `term1 AND term2` |
| `*` | Wildcard for one or more words | `"* api_key *"` |
| `num1..num2` | Numeric range | `"price" 100..500` |
| `before:YYYY-MM-DD` / `after:YYYY-MM-DD` | Date filter | `after:2024-01-01` |
| `cache:` | View Google's cached copy of a page | `cache:example.com` |
| `related:` | Sites related to a domain | `related:example.com` |
| `link:` | Pages linking to a URL (largely deprecated) | `link:example.com` |
| `define:` | Dictionary definition | `define:phishing` |

### Combining Operators

Operators can be chained in a single query. Examples:

- `site:example.com filetype:pdf intext:"confidential"`
- `site:example.com (inurl:login OR inurl:admin OR inurl:portal)`
- `site:example.com ext:env OR ext:bak OR ext:old`
- `intitle:"index of" "parent directory" site:example.com`

## Bing

Bing supports many of the same operators with slightly different syntax/availability:

| Operator | Notes |
| --- | --- |
| `site:` | Same as Google |
| `inbody:` | Equivalent to Google's `intext:` |
| `intitle:` | Same as Google |
| `filetype:` | Same as Google |
| `ip:` | Find sites hosted on a given IP address — useful for finding co-hosted sites |
| `feed:` | Find RSS/Atom feeds |
| `contains:` | Find pages linking to a file of a given type |

Bing's `ip:` operator is particularly useful for OSINT: given an IP address, it can reveal
other domains hosted on the same server (shared hosting).

## DuckDuckGo

DuckDuckGo supports a useful subset: `site:`, `filetype:`, `intitle:`, `inurl:`, `"phrase"`,
`-term`, and `OR`. It does not track users, which can be preferable for OSINT work where you
don't want a personalized/filtered result set.

## General Tips

- **Use multiple engines.** Google, Bing, and DuckDuckGo index different subsets of the web
  and apply different ranking/filtering — cross-checking surfaces more results.
- **Mind regional indexes.** For country-specific investigations (e.g. Spain), pair `site:*.es`
  with local search engines or set the search region/language to surface locally-indexed
  content that global defaults might deprioritize.
- **Strip tracking and re-run periodically.** Indexed content changes; a query that returns
  nothing today may return new results after a re-crawl, especially after a misconfiguration
  is introduced.
