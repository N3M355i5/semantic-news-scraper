import re


class TextCleaner:

    @staticmethod
    def clean(text: str):

        if not text:
            return ""

        patterns = [
            r"Read More\s*→",
            r"Keep Reading!",
            r"Advertisement",
            r"Sponsored",
            r"Cookie Settings",
            r"Privacy Policy"
        ]

        for p in patterns:
            text = re.sub(
                p,
                "",
                text,
                flags=re.IGNORECASE
            )

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()