from search.company_loader import CompanyLoader
from rss.rss_client import RSSClient
from news.url_decoder import URLDecoder
from extractors.trafilatura_extractor import TrafilaturaExtractor
from database.postgres import PostgresDB
from config.settings import DB_CONFIG
from search.company_loader import CompanyLoader

import random
import time


INDUSTRY_MAPPING = {

    "Healthcare": "Healthcare & Life Sciences",

    "Manufacturing": "Manufacturing & Industry 4.0",

    "Financial Services": "Financial Services",

    "Transportation": "Transportation",

    "Retail": "Retail & Consumer Goods",

    "Energy": "Energy & Utilities",

    "Government": "Government & Public Sector",

    "Telecommunications": "Telecommunications"

}


class CompanyPipeline:

    # TARGET_ARTICLES = 2
    TARGET_COMPANY_ARTICLES = 10

    def __init__(self):

        self.rss = RSSClient()

        self.decoder = URLDecoder()

        self.extractor = TrafilaturaExtractor()

        self.db = PostgresDB(DB_CONFIG)

    ##############################################################

    def run(self, semantic_json):

        loader = CompanyLoader(semantic_json)

        semantic_index = loader.get_semantic_index()

        companies = self.db.get_companies()

        print(f"\nLoaded {len(companies)} companies")

        print(f"Loaded {len(semantic_index)} industry groups")

        ##########################################################
        # Google request counter
        ##########################################################

        request_count = 0

        ##########################################################

        for company in companies:

            company_id = company["company_id"]

            company_name = company["company_name"]

            industry = company["industry_group"]

            last_semantic = company["last_semantic"]

            if industry is None:

                continue

            industry = INDUSTRY_MAPPING.get(

                industry,

                industry

            )

            if industry not in semantic_index:

                continue

            print("\n====================================================")

            print(company_name)

            print(industry)

            print("====================================================")

            industry_semantics = semantic_index[industry]
            last_semantic_in_index = next(reversed(industry_semantics))

            if last_semantic == last_semantic_in_index:
                print(f"Skipping {company_name} (already completed)")
                continue

            ######################################################
            # Resume support
            ######################################################

            resume = (
                last_semantic is None
                or last_semantic not in industry_semantics
            )

            ######################################################
            # Company article counter
            ######################################################

            company_saved = 0

            # resume = last_semantic is None

            # if last_semantic not in industry_semantics:

            #     resume = True
            # else:

            #     resume = False

            for semantic, products in industry_semantics.items():

                if not resume:

                    if semantic == last_semantic:

                        resume = True

                        continue

                    continue

                ##################################################

                query = f'"{company_name}" "{semantic}"'


                # rss_articles = self.rss.search(query)

                # print(f"RSS Returned : {len(rss_articles)}")

                try:

                    rss_articles = self.rss.search(query)

                    request_count += 1

                    print(f"\nQuery {request_count}: {query}")

                    if request_count % 50 == 0:

                        pause = random.randint(30, 60)

                        print(
                            f"\nCooling down after "
                            f"{request_count} requests "
                            f"for {pause} seconds..."
                        )

                        time.sleep(pause)

                except RuntimeError as e:

                    if str(e) == "GOOGLE_RATE_LIMIT":

                        print("\n======================================")
                        print("GOOGLE RATE LIMIT EXCEEDED")
                        print("Stopping pipeline...")
                        print("======================================")

                        self.db.close()

                        return

                    raise

                delay = random.uniform(0.35, 0.55)

                print(f"Sleeping for {delay:.2f}s")

                time.sleep(delay)

                print(f"RSS Returned : {len(rss_articles)}")

                # saved = 0

                pointer = 0
                semantic_saved = 0
                # while (

                #     pointer < len(rss_articles)

                #     and saved < self.TARGET_ARTICLES

                # ):

                while (

                    pointer < len(rss_articles)

                    and semantic_saved < 5

                    and company_saved < self.TARGET_COMPANY_ARTICLES

                ):

                    article = rss_articles[pointer]

                    pointer += 1

                    article.company_id = company_id

                    article.company_name = company_name

                    article.product_name = ", ".join(products)

                    article.semantic = semantic

                    article.query = query

                    try:

                        ##################################################

                        article.resolved_url = self.decoder.decode(

                            article.google_url

                        )

                        if not article.resolved_url:

                            continue

                        ##################################################

                        article = self.extractor.extract(article)

                        if article is None:

                            continue

                        ##################################################

                        inserted = self.db.save_article(article)

                        if inserted:

                            semantic_saved += 1
                            company_saved += 1

                            print(

                                f"Saved {semantic_saved}/5 "
                                f"({company_saved}/{self.TARGET_COMPANY_ARTICLES} company): "
                                f"{article.title}"

                            )

                        else:

                            print(

                                f"Duplicate: {article.title}"

                            )

                        # saved += 1

                        # print(

                        #     f"Saved {saved}: "

                        #     f"{article.title}"

                        # )

                        # print(

                        #     f"Saved {company_saved}/{self.TARGET_COMPANY_ARTICLES}: "

                        #     f"{article.title}"

                        # )

                    except Exception as e:

                        print(e)

                        continue

                ######################################################
                # Resume checkpoint
                ######################################################

                self.db.update_last_semantic(

                    company_id,

                    semantic

                )

                if company_saved >= self.TARGET_COMPANY_ARTICLES:

                    break

            ######################################################
            # Company completed successfully
            ######################################################

            # self.db.clear_last_semantic(

            #     company_id

            # )

            print(

                f"\nCompleted {company_name}"

            )

            ##########################################################

        self.db.close()

        print(

            "\n======================================"

        )

        print(

             "Pipeline Finished"

        )

        print(

            "======================================"

        )
