import json
from pathlib import Path


INPUT_FILE = Path("data/companies/ibm.json")

OUTPUT_FILE = Path("data/semantic_index.json")


with open(

    INPUT_FILE,

    "r",

    encoding="utf-8"

) as f:

    data = json.load(f)


semantic_index = {}


##############################################################
# Build:
#
# Industry
#     ↓
# Semantic
#     ↓
# IBM Products
##############################################################

for product in data["products"]:

    industry = product["industry"]

    product_name = product["product_name"]

    semantics = product["semantics"]

    if industry not in semantic_index:

        semantic_index[industry] = {}

    for semantic in semantics:

        semantic = semantic.strip()

        if semantic not in semantic_index[industry]:

            semantic_index[industry][semantic] = []

        if product_name not in semantic_index[industry][semantic]:

            semantic_index[industry][semantic].append(

                product_name

            )


##############################################################
# Sort alphabetically
##############################################################

semantic_index = dict(

    sorted(

        semantic_index.items()

    )

)

for industry in semantic_index:

    semantic_index[industry] = dict(

        sorted(

            semantic_index[industry].items()

        )

    )


##############################################################

with open(

    OUTPUT_FILE,

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        semantic_index,

        f,

        indent=4,

        ensure_ascii=False

    )


print("-----------------------------------------")

print(

    f"Industries : {len(semantic_index)}"

)

total = 0

for industry in semantic_index:

    total += len(

        semantic_index[industry]

    )

print(

    f"Unique Semantics : {total}"

)

print(

    f"Saved to {OUTPUT_FILE}"

)

print("-----------------------------------------")