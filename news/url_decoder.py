from googlenewsdecoder import gnewsdecoder


class URLDecoder:

    def decode(self, google_url: str) -> str | None:
        """
        Converts a Google News RSS URL into the original publisher URL.

        Returns:
            Original publisher URL or None if decoding fails.
        """

        try:

            result = gnewsdecoder(
                google_url,
                interval=1
            )

            if result.get("status"):

                return result.get("decoded_url")

            return None

        except Exception as e:

            print(f"URL Decode Error: {e}")

            return None