from googlenewsdecoder import gnewsdecoder

google_url = (
    "https://news.google.com/rss/articles/"
    "CBMirAFBVV95cUxOaDQ0UjZkbEN2MURlNE1aaGRfNHU1RmJYYzc3ampvSmJ4eHdETjRNd3EycGJDdEVjSTdTMkJ2R0RCNkdTMDJZeUJDMjNqdG1BNVdfdUhuMlBFTkZTNDY2MWhwSTRYQXFXclhkdWN4RTMtZXFLSVpkbGJyRWRNYjhKaVhKSWU3OWRvRzdsX3Y0RzNKUG81SGt1V3R2NGFYYlRyc0pCZ3ZHSkI1bWdQ?oc=5"
)

print("\nDecoding Google News URL...\n")

result = gnewsdecoder(
    google_url,
    interval=1
)

print(result)