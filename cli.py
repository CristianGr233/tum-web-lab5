import sys
from urllib.parse import urlparse, quote_plus

from http_client import https_get
from html_utils import strip_html, get_body


def help():
    print("""
go2web CLI

Usage:
  python go2web.py -u <URL>
  python go2web.py -s <query>
  python go2web.py -h
""")


def fetch_url(url):
    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)

    host = parsed.netloc
    path = parsed.path or "/"

    if parsed.query:
        path += "?" + parsed.query

    if parsed.scheme == "https":
        response = https_get(host, path)
    else:
        response = https_get(host, path)

    body = get_body(response)
    print(strip_html(body))


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

    for i, (t, l) in enumerate(output, 1):
        print(f"{i}. {t}")
        print(f"   {l}\n")


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