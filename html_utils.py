import re


def get_body(response):
    parts = response.split("\r\n\r\n", 1)
    return parts[1] if len(parts) > 1 else response


def strip_html(text):
    # remove scripts/styles
    text = re.sub(r"<script.*?>.*?</script>", "", text, flags=re.S | re.I)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.S | re.I)

    # remove all HTML tags
    text = re.sub(r"<.*?>", "", text)

    # decode basic HTML entities
    text = (text.replace("&amp;", "&")
                .replace("&quot;", '"')
                .replace("&lt;", "<")
                .replace("&gt;", ">"))

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()