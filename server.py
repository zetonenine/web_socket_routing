import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)


while True:
    clientsocket, address = s.accept()
    print('Connection successfull:', address)
    clientsocket.send(bytes('Welocme to the server!'))
