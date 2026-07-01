CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    company_id UUID,
    company_name TEXT,
    product_name TEXT,
    search_query TEXT,
    title TEXT,
    summary TEXT,
    url TEXT UNIQUE,
    source TEXT,
    published_date TIMESTAMP,
    article_text TEXT,
    extraction_method TEXT,
    extraction_status TEXT,
    relevance_score INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);