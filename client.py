import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5000))
s.send(b'Hello')
response = s.recv(1024)
print(response)

# while True:
#     msg = s.recv(8)
#     print(msg.decode('utf-8'))
