import requests
import trafilatura

from utils.text_cleaner import TextCleaner


class TrafilaturaExtractor:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                )
            }
        )

    ##############################################################

    def extract(self, article):

        try:

            response = self.session.get(

                article.resolved_url,

                timeout=30

            )

            response.raise_for_status()

            html = response.text

            text = trafilatura.extract(

                html,

                include_comments=False,

                include_tables=True,

                favor_precision=True

            )

            if text is None:

                return None

            text = TextCleaner.clean(text)

            if len(text.strip()) < 200:

                return None

            article.content = text

            article.word_count = len(text.split())

            article.character_count = len(text)

            article.extractor = "Trafilatura"

            return article

        except Exception:

            return None