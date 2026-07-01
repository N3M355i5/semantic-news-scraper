from rss.rss_client import RSSClient
from news.url_decoder import URLDecoder
from extractors.trafilatura_extractor import TrafilaturaExtractor

rss = RSSClient()
decoder = URLDecoder()
extractor = TrafilaturaExtractor()

query = 'Bosch "Predictive Maintenance"'

print("Searching...")

articles = rss.search(query)

print(f"RSS Articles : {len(articles)}")

if len(articles) == 0:
    print("RSS FAILED")
    exit()

article = articles[0]

print(article.title)
print(article.google_url)

article.resolved_url = decoder.decode(
    article.google_url
)

print("\nDecoded URL")

print(article.resolved_url)

if not article.resolved_url:

    print("URL Decode Failed")

    exit()

article = extractor.extract(article)

print("\nExtraction Result")

print(article)

if article is None:

    print("Extraction Failed")

    exit()

print("\nSUCCESS")

print(article.title)

print(article.word_count)

print(article.character_count)  