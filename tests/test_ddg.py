from duckduckgo_search import DDGS

title = (
    "Bosch acquires Uptake to expand predictive maintenance "
    "for commercial fleets"
)

query = f'"{title}" site:dcvelocity.com'

print(f"\nSearching:\n{query}\n")

with DDGS() as ddgs:

    results = list(
        ddgs.text(
            query,
            max_results=5
        )
    )

print(f"Found {len(results)} results\n")

for i, result in enumerate(results, start=1):

    print("=" * 80)

    print(f"Result {i}")

    print("\nTitle:")
    print(result.get("title"))

    print("\nURL:")
    print(result.get("href"))

    print("\nSnippet:")
    print(result.get("body"))