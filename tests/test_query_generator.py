from search.query_generator import QueryGenerator

generator = QueryGenerator()

queries = generator.generate_queries(
    company_name="Bosch",
    product_name="IBM Maximo"
)

for query in queries:
    print(query)