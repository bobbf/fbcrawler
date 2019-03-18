import socket
import json
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1',1234))


def getJsonFromUrl(urlString):
    #print(urlString)
    response = urllib.request.urlopen(urlString).read().decode()
    responseJson = json.loads(response)
    return responseJson


while 1:
    data, addr = sock.recvfrom(0xffff)
    print("server is received data")
    comments = json.loads(data)
    print(json.dumps(comments, indent=2, sort_keys=True))
    for comment in comments["data"]:
        print("message : " + comment["message"])
        print("writer : " + comment["writer"])

