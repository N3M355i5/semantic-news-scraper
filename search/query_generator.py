import json
from pathlib import Path


class QueryGenerator:

    def __init__(self, json_path: Path):

        with open(
            json_path,
            encoding="utf-8"
        ) as f:

            self.ibm = json.load(f)

    def build_semantic_index(self):

        semantic_index = {}

        for product in self.ibm["products"]:

            industry = product["industry"]

            product_name = product["product_name"]

            for semantic in product["semantics"]:

                if semantic not in semantic_index:

                    semantic_index[semantic] = {

                        "products": [],

                        "industries": []

                    }

                if product_name not in semantic_index[semantic]["products"]:

                    semantic_index[semantic]["products"].append(
                        product_name
                    )

                if industry not in semantic_index[semantic]["industries"]:

                    semantic_index[semantic]["industries"].append(
                        industry
                    )

        return semantic_index