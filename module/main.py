import socket
import functools


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

    def request_parser(self, request):
        request_list = request.decode('utf-8').split('\r\n')
        method, url, _ = request_list[0].split(' ')

        response, status_code = self.routing(url)
        headers = self.get_headers(status_code)
        return (headers + response).encode()

    def get_headers(self, status_code):
        if status_code == 200:
            text = 'Ok'
        elif status_code == 404:
            text = 'Not Found'
        else:
            text = 'Unknown'
        result = f'HTTP/1.0 {status_code} {text}\n\n'
        return result

    def routing(self, url):
        if url in self.urls:
            return self.urls[url][0](), 200

        url_parts = url.split('/')
        params_len = len(url_parts) - 2
        params = url_parts[2:]
        p = ''
        if params_len > 0:
            p = '/p' * params_len

        key = ''.join(['/', url_parts[1], p])
        if key in self.urls:
            func, param = self.urls[key]
            response = func(*params)
            status_code = 200
        else:
            response, status_code = '<h1>Page not found :(</h1>', 404

        return response, status_code

    @classmethod
    def route_register(cls, urls):
        for url, view in urls.items():
            if url == '/':
                cls.urls[url] = (view, ())
                continue
            url_parts = url.split('/')

            params = []
            for i in url_parts:
                if '<' in i:
                    params.append(i[1:-1])
            params_len = len(url_parts) - 2

            key = ''.join(['/', url_parts[1], '/p' * params_len])
            value = (view, tuple(params))
            cls.urls[key] = value
