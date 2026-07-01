from providers.gdelt_provider import GDELTProvider

provider = GDELTProvider()

articles = provider.search(

    query='Bosch AND "Predictive Maintenance"',

    max_results=10

)

print()

print(f"Found {len(articles)} articles\n")

for article in articles:

    print("=" * 80)

    print(article.title)

    print()

    print(article.source)

    print()

    print(article.url)

    print()

    print(article.published)

    print()