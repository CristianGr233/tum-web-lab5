import sys


def help():
    print("""
go2web CLI

Usage:
  python go2web.py -u <URL>         Fetch webpage
  python go2web.py -s <query>       Search web
  python go2web.py -h               Help
""")


def main():
    if len(sys.argv) < 2:
        help()
        return

    cmd = sys.argv[1]

    if cmd == "-h":
        help()

    elif cmd == "-u":
        print("Fetch feature not implemented yet")

    elif cmd == "-s":
        print("Search feature not implemented yet")

    else:
        print("Unknown command")
        help()