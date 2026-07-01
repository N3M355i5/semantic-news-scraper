from bs4 import BeautifulSoup
from models.article import Article

class RSSParser:
    def parse(self, feed):
        articles = []
        for entry in feed.entries:
            title = entry.get(
                "title",
                ""
            )
            summary_html = entry.get(
                "summary",
                ""
            )
            summary = BeautifulSoup(
                summary_html,
                "html.parser"
            ).get_text(
                separator=" ",
                strip=True
            )
            source = ""
            if (
                "source" in entry
                and isinstance(
                    entry.source,
                    dict
                )
            ):
                source = entry.source.get(
                    "title",
                    ""
                )
            article = Article(
                title=title,
                summary=summary,
                source=source,
                published=entry.get(
                    "published",
                    ""
                ),
                google_url=entry.get(
                    "link",
                    ""
                )
            )
            articles.append(
                article
            )
        return articles