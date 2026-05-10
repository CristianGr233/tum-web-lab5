import sys
from urllib.parse import urlparse

from http_client import http_get, https_get
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
        response = http_get(host, path)

    body = get_body(response)
    clean = strip_html(body)

    print("\n" + "=" * 50)
    print(clean)
    print("=" * 50 + "\n")


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
        print("Search not implemented yet")

    else:
        print("Unknown command")
        help()