import psycopg2


class PostgresDB:

    def __init__(self, config):

        self.conn = psycopg2.connect(**config)

        self.cur = self.conn.cursor()

    ###############################################################
    # READ COMPANIES
    ###############################################################

    def get_companies(self):

        self.cur.execute(
            """
            SELECT
                company_id,
                company_name,
                industry_group,
                last_semantic
            FROM companies
            ORDER BY company_name
            """
        )

        rows = self.cur.fetchall()

        companies = []

        for row in rows:

            companies.append(
                {
                    "company_id": row[0],
                    "company_name": row[1],
                    "industry_group": row[2],
                    "last_semantic": row[3]
                }
            )

        return companies

    ###############################################################
    # UPDATE LAST SEMANTIC
    ###############################################################

    def update_last_semantic(

        self,

        company_id,

        semantic

    ):

        self.cur.execute(

            """
            UPDATE companies
            SET last_semantic = %s
            WHERE company_id = %s
            """,

            (

                semantic,

                company_id

            )

        )

        self.conn.commit()

    # ###############################################################
    # # CLEAR LAST SEMANTIC
    # ###############################################################

    # def clear_last_semantic(

    #     self,

    #     company_id

    # ):

    #     self.cur.execute(

    #         """
    #         UPDATE companies
    #         SET last_semantic = NULL
    #         WHERE company_id = %s
    #         """,

    #         (

    #             company_id,

    #         )

    #     )

    #     self.conn.commit()

    ###############################################################
    # SAVE ARTICLE
    ###############################################################

    def save_article(self, article):

        try:

            self.cur.execute(

                """
                INSERT INTO articles
                (
                    company_id,
                    product_name,
                    semantic,
                    title,
                    article_text,
                    source,
                    publication_date,
                    google_url,
                    resolved_url,
                    query,
                    extractor,
                    word_count,
                    character_count
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

                ON CONFLICT (resolved_url)
                DO NOTHING
                """,

                (

                    article.company_id,

                    article.product_name,

                    article.semantic,

                    article.title,

                    article.content,

                    article.source,

                    article.published,

                    article.google_url,

                    article.resolved_url,

                    article.query,

                    article.extractor,

                    article.word_count,

                    article.character_count

                )

            )

            self.conn.commit()

            if self.cur.rowcount == 1:

                return True

            return False

        except Exception as e:

            self.conn.rollback()

            print("\n===================================")
            print("DATABASE ERROR")
            print(e)
            print("===================================\n")

            return False

    ###############################################################

    def close(self):

        self.cur.close()

        self.conn.close()