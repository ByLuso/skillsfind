# Spanish Identifier Formats & Validation

Use these checks to confirm an identifier is *well-formed* before spending time searching for
it. A failed checksum means the number is mistyped, fabricated, or fake — flag this to the user
rather than searching further.

## DNI (Documento Nacional de Identidad)

Format: 8 digits + 1 check letter, e.g. `12345678Z`.

Algorithm:

1. Take the 8-digit number.
2. Compute `index = number mod 23`.
3. Look up `index` in the letter table below (0-indexed).

```
Index:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22
Letter: T  R  W  A  G  M  Y  F  P  D  X  B  N  J  Z  S  Q  V  H  L  C  K  E
```

Example: `12345678 mod 23 = 14` → `Z`, so `12345678Z` is a structurally valid DNI.

## NIE (Número de Identidad de Extranjero)

Format: leading letter `X`, `Y`, or `Z` + 7 digits + 1 check letter, e.g. `X1234567L`.

Algorithm:

1. Replace the leading letter with a digit: `X → 0`, `Y → 1`, `Z → 2`.
2. Concatenate with the 7 digits to form an 8-digit number.
3. Apply the same `mod 23` table as the DNI.

Example: `X1234567` → `01234567 mod 23 = 14` → `Z`, so `X1234567Z`... (recompute for the
specific number you're validating; the table above is the source of truth).

## CIF / NIF for Legal Entities (Código de Identificación Fiscal)

Format: 1 organization-type letter + 7 digits + 1 control character (digit **or** letter
depending on the organization type), e.g. `B12345674`.

Common leading letters: `A` Sociedad Anónima, `B` Sociedad Limitada, `C` Sociedad Colectiva,
`D` Sociedad Comanditaria, `F` Cooperativa, `G` Asociación, `J` Sociedad Civil, `N` Entidad
extranjera, `P` Organismo público, `Q` Organismo autónomo/entidad de derecho público, `R`
Congregación religiosa, `S` Órgano de la Administración del Estado/CCAA, `U` UTE, `V` Otros
tipos, `W` Establecimiento permanente de entidad no residente.

Control character algorithm:

1. Take the 7 digits following the leading letter, `d1 d2 d3 d4 d5 d6 d7`.
2. **Sum A** = `d2 + d4 + d6` (digits at even positions, summed directly).
3. **Sum B** = for each digit at an odd position (`d1, d3, d5, d7`): multiply by 2; if the
   result is ≥ 10, sum its two digits (equivalent to subtracting 9). Sum all four results.
4. `total = A + B`.
5. `control_digit = (10 - (total mod 10)) mod 10`.
6. Determine the final character:
   - If the leading letter is one of `K, P, Q, S` (and a few other public-entity types), the
     control character is a **letter**: index `control_digit` into `"JABCDEFGHI"` (0 → `J`,
     1 → `A`, ..., 9 → `I`).
   - If the leading letter is one of `A, B, E, H`, the control character is the
     **digit** `control_digit` itself.
   - For other leading letters, either form may appear; accept both.

## Spanish IBAN / CCC

A Spanish IBAN is `ES` + 2 IBAN check digits + 20-digit CCC (Código Cuenta Cliente):
`EEEE OOOO DD NNNNNNNNNN` (4-digit entity code, 4-digit branch/office code, 2 CCC control
digits, 10-digit account number).

- The 2 leading **IBAN check digits** follow the standard ISO 7064 MOD 97-10 algorithm shared
  by all IBAN countries.
- The 2 **CCC control digits** (positions 9-10 of the CCC) are computed separately using the
  weights `1, 2, 4, 8, 5, 10, 9, 7, 3, 6` (mod 11) applied to the entity+branch digits for the
  first control digit, and to the account number digits for the second. If the result is `10`,
  the control digit becomes `1`; if `11`, it becomes `0`.

When validating, prefer a standard IBAN-validation library/algorithm rather than re-deriving
this from scratch.

## NUSS (Número de la Seguridad Social)

Format: 12 digits — 2-digit province/office code + 8-digit sequential number + 2 check digits.

Check digits = the 10-digit number formed by the province code + sequential number, taken
`mod 97`, expressed as 2 digits (pad with a leading zero if needed).

## Vehicle Registration Plates

Current format (since September 2000): `NNNN LLL` — 4 digits followed by 3 consonants, e.g.
`1234 BCD`. The letters exclude vowels (`A, E, I, O, U`) and `Ñ`, `Q` to avoid ambiguity, and
combinations that could spell offensive words are skipped. Plates are sequential and do not
encode region or date (unlike the pre-2000 format, which had a 1-2 letter province code).
