import requests

url = "https://www.automotive-fleet.com/news/bosch-to-acquire-ai-predictive-maintenance-startup-uptake-technologies"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("STATUS:", response.status_code)
    print("CONTENT LENGTH:", len(response.text))
    print("\nFIRST 500 CHARACTERS:\n")
    print(response.text[:500])

except Exception as e:
    print(e)