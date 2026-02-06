---
name: faker-patterns
description: Realistic data generation patterns using faker providers with locale awareness
---

# Faker Patterns

## Purpose

Map schema column types and naming conventions to appropriate faker data generators. This skill ensures generated test data is realistic, locale-aware, and respects type constraints.

---

## Column Name to Provider Mapping

Use column name heuristics to select the most realistic faker provider:

| Column Name Pattern | Faker Provider | Example Output |
|---------------------|---------------|----------------|
| `*name`, `first_name` | `faker.name()` / `faker.first_name()` | "Alice Johnson" |
| `*last_name`, `surname` | `faker.last_name()` | "Rodriguez" |
| `*email` | `faker.email()` | "alice@example.com" |
| `*phone*`, `*tel*` | `faker.phone_number()` | "+1-555-0123" |
| `*address*`, `*street*` | `faker.street_address()` | "742 Evergreen Terrace" |
| `*city` | `faker.city()` | "Toronto" |
| `*state*`, `*province*` | `faker.state()` | "Ontario" |
| `*country*` | `faker.country()` | "Canada" |
| `*zip*`, `*postal*` | `faker.postcode()` | "M5V 2H1" |
| `*url*`, `*website*` | `faker.url()` | "https://example.com" |
| `*company*`, `*org*` | `faker.company()` | "Acme Corp" |
| `*title*`, `*subject*` | `faker.sentence(nb_words=5)` | "Updated quarterly report summary" |
| `*description*`, `*bio*`, `*body*` | `faker.paragraph()` | Multi-sentence text |
| `*created*`, `*updated*`, `*_at` | `faker.date_time_between(start_date='-2y')` | "2024-06-15T10:30:00" |
| `*date*`, `*dob*`, `*birth*` | `faker.date_of_birth(minimum_age=18)` | "1990-03-22" |
| `*price*`, `*amount*`, `*cost*` | `faker.pydecimal(min_value=0.01, max_value=9999.99)` | 49.99 |
| `*quantity*`, `*count*` | `faker.random_int(min=1, max=100)` | 7 |
| `*status*` | Random from enum or `["active", "inactive", "pending"]` | "active" |
| `*uuid*`, `*guid*` | `faker.uuid4()` | "550e8400-e29b-41d4-a716-446655440000" |
| `*ip*`, `*ip_address*` | `faker.ipv4()` | "192.168.1.42" |
| `*color*`, `*colour*` | `faker.hex_color()` | "#3498db" |
| `*password*`, `*hash*` | `faker.sha256()` | Hash string (never plaintext) |
| `*image*`, `*avatar*`, `*photo*` | `faker.image_url()` | "https://picsum.photos/200" |
| `*slug*` | `faker.slug()` | "updated-quarterly-report" |
| `*username*`, `*login*` | `faker.user_name()` | "alice_johnson42" |

## Type Fallback Mapping

When column name does not match any pattern, fall back to type-based generation:

| Canonical Type | Generator |
|----------------|-----------|
| `string` | `faker.pystr(max_chars=max_length)` |
| `integer` | `faker.random_int(min=0, max=2147483647)` |
| `float` | `faker.pyfloat(min_value=0, max_value=10000)` |
| `decimal` | `faker.pydecimal(left_digits=precision-scale, right_digits=scale)` |
| `boolean` | `faker.pybool()` |
| `datetime` | `faker.date_time_between(start_date='-2y', end_date='now')` |
| `date` | `faker.date_between(start_date='-2y', end_date='today')` |
| `uuid` | `faker.uuid4()` |
| `json` | `{"key": faker.word(), "value": faker.sentence()}` |

## Locale Support

Supported locales affect names, addresses, phone formats, and postal codes:

| Locale | Names | Addresses | Phone | Currency |
|--------|-------|-----------|-------|----------|
| `en_US` | English names | US addresses | US format | USD |
| `en_CA` | English names | Canadian addresses | CA format | CAD |
| `en_GB` | English names | UK addresses | UK format | GBP |
| `pt_BR` | Portuguese names | Brazilian addresses | BR format | BRL |
| `fr_FR` | French names | French addresses | FR format | EUR |
| `de_DE` | German names | German addresses | DE format | EUR |
| `ja_JP` | Japanese names | Japanese addresses | JP format | JPY |
| `es_ES` | Spanish names | Spanish addresses | ES format | EUR |

Default locale: `en_US`. Override per-profile or per-command with `--locale`.

## Edge Case Values

Include at configurable ratio (default 10%):

| Type | Edge Cases |
|------|------------|
| `string` | Empty string `""`, max-length string, unicode characters, emoji, SQL special chars `'; DROP TABLE --` |
| `integer` | 0, -1, MAX_INT, MIN_INT |
| `float` | 0.0, -0.0, very small (0.0001), very large (999999.99) |
| `date` | Today, yesterday, epoch (1970-01-01), leap day (2024-02-29) |
| `boolean` | null (if nullable) |
| `email` | Plus-addressed `user+tag@example.com`, long domain, subdomain email |
