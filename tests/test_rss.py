from rss.rss_client import RSSClient

rss = RSSClient()

articles = rss.search(
    'Bosch "Predictive Maintenance"'
)

print()

print(
    f"Found {len(articles)} articles\n"
)

for article in articles[:5]:

    print("=" * 80)

    print(
        "TITLE:"
    )

    print(
        article.title
    )

    print()

    print(
        "SOURCE:"
    )

    print(
        article.source
    )

    print()

    print(
        "DATE:"
    )

    print(
        article.published
    )

    print()

    print(
        "URL:"
    )

    print(
        article.url
    )

    print()

    print(
        "SUMMARY:"
    )

    print(
        article.summary
    )

    print()