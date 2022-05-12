import socket
import functools

from module.views import index


route_register = {
    '/': index,
}


def method_handler(method, url):
    if not method == 'GET':
        return 'HTTP/1.0 405 Method not allowed\n\n', 405

    if url not in route_register:
        return 'HTTP/1.0 404 Not Found\n\n', 404

    return 'HTTP/1.0 200 Ok\n\n', 200


def request_parser(request):
    request_list = request.decode('utf-8').split('\r\n')
    method, url, _ = request_list[0].split(' ')
    headers, status_code = method_handler(method, url)
    if status_code == 200:
        return (headers + route_register[url]()).encode()
    if status_code == 404:
        return (headers + '<h1>Page not found :(</h1>').encode()
    if status_code == 405:
        return (headers + '<h1>Method Not allowed</h1>').encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        response = request_parser(request)
        client_socket.sendall(response)

        # client_socket.sendall(b'HTTP/1.0 200 OK\r\nContent-Length: 11\r\nContent-Type: text/html; charset=UTF-8\r\n\r\nContent: Hello World\r\n')

        client_socket.close()


if __name__ == '__main__':
    run()
