from dataclasses import dataclass


@dataclass
class Article:

    company_id: str = ""
    company_name: str = ""

    product_name: str = ""

    semantic: str = ""

    query: str = ""

    title: str = ""
    summary: str = ""

    source: str = ""
    published: str = ""

    google_url: str = ""
    resolved_url: str = ""

    content: str = ""

    extractor: str = ""

    word_count: int = 0
    character_count: int = 0