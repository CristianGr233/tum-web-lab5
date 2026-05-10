import os
import hashlib
import time

CACHE_DIR = ".cache"
TTL = 60 * 60  # 1 hour


def _key(url):
    return hashlib.md5(url.encode()).hexdigest()


def get(url):
    path = os.path.join(CACHE_DIR, _key(url))

    if not os.path.exists(path):
        return None

    # TTL check
    if time.time() - os.path.getmtime(path) > TTL:
        return None

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def set(url, data):
    os.makedirs(CACHE_DIR, exist_ok=True)

    path = os.path.join(CACHE_DIR, _key(url))

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)