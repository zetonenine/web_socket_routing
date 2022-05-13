import socket


class Frame:
    _instance = None

    urls = {}

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', 5000))
        self.server_socket.listen()

        self.loop()

    def loop(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            request = client_socket.recv(1024)
            response = self.request_parser(request)
            client_socket.sendall(response)
            client_socket.close()

    def method_handler(self, method, url):
        if not method == 'GET':
            return 'HTTP/1.0 405 Method not allowed\n\n', 405

        if url not in self.urls:
            return 'HTTP/1.0 404 Not Found\n\n', 404

        return 'HTTP/1.0 200 Ok\n\n', 200

    def request_parser(self, request):
        request_list = request.decode('utf-8').split('\r\n')
        method, url, _ = request_list[0].split(' ')
        headers, status_code = self.method_handler(method, url)
        if status_code == 200:
            return (headers + self.urls[url]()).encode()
        if status_code == 404:
            return (headers + '<h1>Page not found :(</h1>').encode()
        if status_code == 405:
            return (headers + '<h1>Method Not allowed</h1>').encode()

    @classmethod
    def route_register(cls, urls):
        for url, view in urls.items():
            cls.urls[url] = view
