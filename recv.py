import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1',1234))


while 1:
    data, addr = sock.recvfrom(0xffff)
    print("server is received data:", data.decode())
    print("Send Client IP : ", addr[0])
    print("Send Client Port :", addr[1])
