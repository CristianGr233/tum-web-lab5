import sys
from urllib.parse import urlparse, quote_plus

from http_client import http_get, https_get
from http_cache import get as cache_get, set as cache_set
from html_utils import strip_html, get_body


# ----------------------------
# HELP
# ----------------------------
def help():
    print("""
go2web CLI

Usage:
  python go2web.py -u <URL>         Fetch webpage
  python go2web.py -s <query>       Search web (top 10 results)
  python go2web.py -h               Help
""")


# ----------------------------
# FETCH URL WITH CACHE + REDIRECTS
# ----------------------------
def fetch_url(url, max_redirects=5):
    if not url.startswith("http"):
        url = "http://" + url

    for _ in range(max_redirects):

        cached = cache_get(url)

        if cached:
            print("[CACHE HIT]")
            response = cached
        else:
            parsed = urlparse(url)

            host = parsed.netloc
            path = parsed.path or "/"

            if parsed.query:
                path += "?" + parsed.query

            if parsed.scheme == "https":
                response = https_get(host, path)
            else:
                response = http_get(host, path)

            cache_set(url, response)

        # ----------------------------
        # PARSE HEADERS
        # ----------------------------
        header_part = response.split("\r\n\r\n", 1)[0]

        headers = {}
        for line in header_part.split("\r\n")[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.lower()] = v.strip()

        status = header_part.split("\r\n")[0]

        # ----------------------------
        # REDIRECT HANDLING
        # ----------------------------
        if "301" in status or "302" in status:
            if "location" in headers:
                url = headers["location"]
                print(f"[Redirect → {url}]")
                continue

        # ----------------------------
        # OUTPUT BODY
        # ----------------------------
        body = get_body(response)
        clean = strip_html(body)

        print("\n" + "=" * 60)
        print(clean)
        print("=" * 60 + "\n")
        return

    print("Too many redirects")


# ----------------------------
# SEARCH ENGINE (-s)
# ----------------------------
def search(query):
    print(f"\nSearching: {query}\n")

    q = quote_plus(query)

    host = "html.duckduckgo.com"
    path = f"/html/?q={q}"

    response = https_get(host, path)
    body = get_body(response)

    import re

    results = re.findall(
        r'<a[^>]*class="result__a"[^>]*href="(.*?)"[^>]*>(.*?)</a>',
        body,
        re.S
    )

    output = []

    for link, title in results:
        clean_title = strip_html(title)
        output.append((clean_title, link))

        if len(output) == 10:
            break

    if not output:
        print("No results found")
        return

    print("\n" + "=" * 60)

    for i, (t, l) in enumerate(output, 1):
        print(f"{i}. {t}")
        print(f"   {l}\n")

    print("=" * 60 + "\n")


# ----------------------------
# MAIN
# ----------------------------
def main():
    if len(sys.argv) < 2:
        help()
        return

    cmd = sys.argv[1]

    if cmd == "-h":
        help()

    elif cmd == "-u":
        if len(sys.argv) < 3:
            print("Missing URL")
            return
        fetch_url(sys.argv[2])

    elif cmd == "-s":
        if len(sys.argv) < 3:
            print("Missing search query")
            return
        search(" ".join(sys.argv[2:]))

    else:
        print("Unknown command")
        help()