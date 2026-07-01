from models.article import Article
from extractors.trafilatura_extractor import TrafilaturaExtractor

article = Article()

article.resolved_url = (
    "https://www.automotive-fleet.com/news/"
    "bosch-to-acquire-ai-predictive-maintenance-startup-uptake-technologies"
)

extractor = TrafilaturaExtractor()

article = extractor.extract(article)

if article:

    print("SUCCESS\n")

    print(article.word_count)

    print(article.character_count)

    print(article.extractor)

    print()

    print(article.content[:1000])

else:

    print("FAILED")