from gdeltdoc import GdeltDoc
from gdeltdoc import Filters

from models.article import Article

from providers.base_provider import BaseProvider


class GDELTProvider(BaseProvider):

    def __init__(self):

        self.client = GdeltDoc()

    def search(
        self,
        query: str,
        max_results: int = 50
    ):

        filters = Filters(

            keyword=query,

            timespan="3months",

            num_records=max_results

        )

        df = self.client.article_search(
            filters
        )

        articles = []

        if df.empty:
            return articles

        for _, row in df.iterrows():

            article = Article(

                title=row["title"],

                summary="",

                url=row["url"],

                source=row["domain"],

                published=str(
                    row["seendate"]
                )

            )

            articles.append(
                article
            )

        return articles