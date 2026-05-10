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
  python go2web.py -u <URL>         Fetch webpage (HTTP/HTTPS)
  python go2web.py -s <query>       Search web (top 10 results)
  python go2web.py -h               Help
""")


# ----------------------------
# FETCH URL (-u)
# ----------------------------
def fetch_url(url):
    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)

    host = parsed.netloc
    path = parsed.path or "/"

    if parsed.query:
        path += "?" + parsed.query

    # ----------------------------
    # CACHE
    # ----------------------------
    cached = cache_get(url)

    if cached:
        print("\n[CACHE HIT]\n")
        response = cached
    else:
        if parsed.scheme == "https":
            response = https_get(host, path)
        else:
            response = http_get(host, path)

        cache_set(url, response)

    # ----------------------------
    # OUTPUT CLEANING
    # ----------------------------
    body = get_body(response)
    clean = strip_html(body)

    print("\n" + "=" * 60)
    print(clean)
    print("=" * 60 + "\n")


# ----------------------------
# SEARCH (-s)
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
        clean_link = link

        output.append((clean_title, clean_link))

        if len(output) == 10:
            break

    if not output:
        print("No results found")
        return

    print("\n" + "=" * 60)

    for i, (title, link) in enumerate(output, 1):
        print(f"{i}. {title}")
        print(f"   {link}\n")

    print("=" * 60 + "\n")


# ----------------------------
# MAIN CLI ROUTER
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
        print(f"Unknown command: {cmd}")
        help()


# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    main()