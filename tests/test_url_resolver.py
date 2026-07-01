import requests

url = (
    "https://news.google.com/rss/articles/CBMirAFBVV95cUxOaDQ0UjZkbEN2MURlNE1aaGRfNHU1RmJYYzc3ampvSmJ4eHdETjRNd3EycGJDdEVjSTdTMkJ2R0RCNkdTMDJZeUJDMjNqdG1BNVdfdUhuMlBFTkZTNDY2MWhwSTRYQXFXclhkdWN4RTMtZXFLSVpkbGJyRWRNYjhKaVhKSWU3OWRvRzdsX3Y0RzNKUG81SGt1V3R2NGFYYlRyc0pCZ3ZHSkI1bWdQ?oc=5"
)

response = requests.get(
    url,
    allow_redirects=True,
    timeout=30,
    headers={
        "User-Agent":
        "Mozilla/5.0"
    }
)

print("\nFINAL URL\n")
print(response.url)

print("\nSTATUS\n")
print(response.status_code)