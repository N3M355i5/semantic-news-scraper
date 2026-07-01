from database.postgres import PostgresDB
from config.settings import DB_CONFIG

from models.article import Article

db = PostgresDB(DB_CONFIG)

article = Article()

article.company_id = "a94cf55d-40c8-4079-8511-894fc32706e1"

article.product_name = "IBM Maximo"

article.semantic = "Predictive Maintenance"

article.title = "Database Test"

article.content = "Hello World"

article.source = "Test"

article.published = "2026-06-29"

article.google_url = "https://google.com"

article.resolved_url = "https://example.com/database_test"

article.query = "test"

article.extractor = "Trafilatura"

article.word_count = 2

article.character_count = 11

db.save_article(article)

db.close()

print("DONE")