<div align="center">

# 📡 Semantic News Scraper

**A resumable, semantics-driven news intelligence pipeline.**
Turns a company × product × industry taxonomy into targeted search queries, harvests fresh coverage from Google News RSS, resolves and extracts full article text, and lands clean, deduplicated records in PostgreSQL - ready for downstream lead-generation and market-signal analysis.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-lead--intelligence-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/status-active--development-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## Why this exists

Turning "which companies are talking about X in the news" into a queryable dataset sounds simple until you actually try it: Google News RSS returns redirect-wrapped URLs, not the real article; every publisher's HTML is different; the same story gets syndicated across a dozen outlets; and any script that fires hundreds of queries in a loop gets rate-limited in minutes.

This project is my answer to that problem, built around a simple idea: **let a semantic taxonomy drive the search, not a flat keyword list.** Instead of searching "Bosch news," it searches `"Bosch" "Predictive Maintenance"`, `"Bosch" "Fraud Detection"`, etc. - one query per relevant concept, generated automatically from a company's product/industry mapping - so the articles that come back are actually relevant to a specific business signal, not just noise.

---

## How it flows

```mermaid
flowchart TD
    A["Company & Product Config<br/>(data/companies/*.json)"] --> B["Semantic Index Builder<br/>tools/build_semantic_index.py"]
    B --> C["Semantic Index<br/>Industry → Concept → Products"]
    C --> D["Query Generator<br/>search/query_generator.py"]
    D --> E["RSS Client<br/>Google News RSS"]
    E -->|"rate-limit aware, cooldown + jitter"| F["RSS Parser<br/>feed → Article objects"]
    F --> G["Google URL Decoder<br/>redirect → publisher URL"]
    G --> H["Content Extractor<br/>Trafilatura (+ pluggable engines)"]
    H --> I["Filters<br/>dedupe · relevance scoring"]
    I --> J[("PostgreSQL<br/>articles table")]
    J --> K["Resume checkpoint<br/>per company / per concept"]
    K -.->|"next run picks up where it left off"| D

    style A fill:#1e293b,color:#fff
    style J fill:#0f172a,color:#fff
    style K fill:#334155,color:#fff
```

Every company run walks its industry's concept list one at a time, checkpoints its progress in Postgres after each concept, and can be killed and restarted without redoing work or re-saving duplicates.

---

## Architecture at a glance

The codebase is split into small, swappable layers rather than one monolithic script - the goal was to make it trivial to add a new news source or a new extraction engine without touching the pipeline logic.

```mermaid
flowchart LR
    subgraph Sources["Pluggable Sources"]
        direction TB
        P1["BaseProvider<br/>(interface)"]
        P2["Google News RSS"]
        P3["GDELT Doc API"]
        P1 --- P2
        P1 --- P3
    end

    subgraph Extraction["Pluggable Extractors"]
        direction TB
        E1["Trafilatura ✅"]
        E2["Newspaper4k"]
        E3["Crawl4AI"]
        E4["Firecrawl"]
    end

    subgraph Core["Pipeline Core"]
        direction TB
        CP["CompanyPipeline"]
        DC["URL Decoder"]
        DB[("PostgreSQL")]
    end

    Sources --> CP --> DC --> Extraction --> DB
```

| Layer         | Purpose                                                                                                                                | Status                                                         |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `providers/`  | Abstract source interface (`BaseProvider`) - Google News RSS is the primary path, GDELT is a secondary source for broader time windows | ✅ RSS · ✅ GDELT                                              |
| `extractors/` | Pulls clean article text out of arbitrary publisher HTML                                                                               | ✅ Trafilatura wired in · others scaffolded for future engines |
| `filters/`    | Deduplication and relevance scoring before a write hits the DB                                                                         | 🚧 in progress                                                 |
| `pipeline/`   | Orchestrates the full run per company, with resume/checkpoint logic and Google rate-limit backoff                                      | ✅                                                             |
| `database/`   | PostgreSQL persistence layer + schema                                                                                                  | ✅                                                             |
| `search/`     | Builds the industry → concept → product semantic index from a company's taxonomy and generates targeted queries from it                | ✅                                                             |

---

## What's under the hood

<table>
<tr><td valign="top" width="50%">

**Ingestion & parsing**

- `feedparser` - Google News RSS/Atom parsing
- `requests` - HTTP layer with custom UA + timeout handling
- `googlenewsdecoder` - resolves Google's redirect URLs to the real publisher link
- `gdeltdoc` - GDELT Doc API as a secondary source

**Extraction & cleaning**

- `trafilatura` - main-content extraction from raw HTML
- `newspaper4k` - alternate extraction engine (scaffolded)
- `beautifulsoup4` / `lxml` - HTML parsing utilities

</td><td valign="top" width="50%">

**Persistence**

- `psycopg2-binary` - PostgreSQL driver
- Resume-safe schema with a `UNIQUE` constraint on URL for free deduplication at the DB layer

**Ops & DX**

- `python-dotenv` - environment-based config, no secrets in code
- `loguru` - structured logging
- `tqdm` / `colorama` - progress + readable console output
- Randomized jitter + cooldown windows to stay under Google's rate limits

</td></tr>
</table>

---

## Project structure

```
semantic-news-scraper/
├── main.py                      # entry point - kick off a company run
├── config/
│   └── settings.py              # env-driven config (DB, timeouts, limits)
├── search/
│   ├── company_loader.py        # loads a company's semantic index
│   └── query_generator.py       # builds "Company" "Concept" search queries
├── tools/
│   └── build_semantic_index.py  # Industry → Concept → Products index builder
├── rss/
│   ├── rss_client.py            # Google News RSS client + rate-limit handling
│   └── rss_parser.py            # feed entries → Article objects
├── providers/
│   ├── base_provider.py         # abstract source interface
│   └── gdelt_provider.py        # GDELT Doc API source
├── news/
│   └── url_decoder.py           # Google redirect URL → real publisher URL
├── extractors/
│   └── trafilatura_extractor.py # HTML → clean article text
├── filters/                     # dedup + relevance scoring (in progress)
├── models/
│   └── article.py                # Article dataclass shared across the pipeline
├── database/
│   ├── postgres.py               # persistence layer
│   └── schema.sql                # articles table definition
├── pipeline/
│   └── company_pipeline.py       # orchestration, resume logic, backoff
├── data/
│   └── companies/                # per-company product/industry taxonomies
└── tests/                        # exploratory scripts against live sources
```

---

## Local setup

**1. Clone and create a virtual environment**

```bash
git clone https://github.com/<your-username>/semantic-news-scraper.git
cd semantic-news-scraper
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Set up PostgreSQL**

```bash
createdb lead_intelligence
psql -d lead_intelligence -f database/schema.sql
```

**4. Configure environment variables**

```bash
cp .env.example .env
# then edit .env with your local DB credentials
```

**5. Build the semantic index** (from a company taxonomy in `data/companies/`)

```bash
python tools/build_semantic_index.py
```

**6. Run the pipeline**

```bash
python main.py
```

---

## Example: how a query gets built

Given a taxonomy entry like:

```json
{
  "product_name": "Product X",
  "industry": "Financial Services",
  "semantics": ["Fraud Detection", "Payment Security", "AML"]
}
```

the pipeline generates one targeted RSS query per concept - `"<Company>" "Fraud Detection"`, `"<Company>" "Payment Security"`, `"<Company>" "AML"` - rather than one generic company-name search, so what comes back is filtered toward a specific business signal before a single line of article text is even fetched.

---

## Roadmap

- [ ] Finish relevance & duplicate filters (currently scaffolded, not wired into the pipeline)
- [ ] Add Newspaper4k / Crawl4AI / Firecrawl as selectable extraction backends
- [ ] Turn ad-hoc scripts in `tests/` into real automated tests
- [ ] Batch pipeline for running multiple companies concurrently
- [ ] Lightweight dashboard for reviewing captured signals

---

## License

MIT - see [LICENSE](LICENSE) for details.
