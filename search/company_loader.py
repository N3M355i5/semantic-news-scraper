import json


class CompanyLoader:

    def __init__(self, json_path):

        with open(

            json_path,

            "r",

            encoding="utf-8"

        ) as f:

            self.data = json.load(f)

    ###############################################################

    def get_semantic_index(self):

        return self.data