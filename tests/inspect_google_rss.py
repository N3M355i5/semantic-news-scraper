import requests

url = "https://news.google.com/rss/articles/CBMirAFBVV95cUxOaDQ0UjZkbEN2MURlNE1aaGRfNHU1RmJYYzc3ampvSmJ4eHdETjRNd3EycGJDdEVjSTdTMkJ2R0RCNkdTMDJZeUJDMjNqdG1BNVdfdUhuMlBFTkZTNDY2MWhwSTRYQXFXclhkdWN4RTMtZXFLSVpkbGJyRWRNYjhKaVhKSWU3OWRvRzdsX3Y0RzNKUG81SGt1V3R2NGFYYlRyc0pCZ3ZHSkI1bWdQ?oc=5"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers,
    timeout=30
)

print(response.status_code)
print(response.text[:3000])