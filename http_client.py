import socket
import ssl


def raw_request(host, path, use_ssl=False):
    port = 443 if use_ssl else 80

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    if use_ssl:
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=host)

    try:
        sock.connect((host, port))

        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: go2web\r\n"
            f"Connection: close\r\n\r\n"
        )

        sock.send(request.encode())

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data

        return response.decode(errors="ignore")

    finally:
        sock.close()


def http_get(host, path):
    return raw_request(host, path, False)


def https_get(host, path):
    return raw_request(host, path, True)