import socket
import asyncio
from api import api

def construct_response(status:int, content_type:str = "text/html", data=b'') -> bytes:
    res = ''
    res += 'HTTP/2 ' + str(status) + '\r\n'
    res += 'content-type: ' + content_type + '\r\n'
    res += 'content-length: ' + str(len(data)) + '\r\n\r\n'
    res = bytes(res, "utf-8") + bytes(data)
    return res

def serve_request(sock, request):
    method, path = None, None
    line = request.split(b'\n\r')[0].split(b' ')
    if len(line) > 3:
       method, path = line[0], line[1]
    if not (method and path):
        return 1
    if ( method != b'GET' ):
        return 2

    if (path == b'/index.html' or path == b"/"):
        data = b''
        with open('../res/templates/index.html', 'rb') as file:
            data += file.read()
        print(data)
        response = construct_response(200, "text/html", data)
        sock.send(response)
    elif (path == b'/datatable.html'):
        data = b''
        with open('../res/templates/datatable.html', 'rb') as file:
            data += file.read()
        response = construct_response(200, "text/html", data)
        sock.send(response)
    elif (path == b"/reciklazna_dvorista.json" ):
        data = b''
        with open('../reciklažna_dvorišta.json', 'rb') as file:
            data += file.read()
        response = construct_response(200, "application/json", data)
        sock.send(response)
    elif (path == b'/reciklazna_dvorista.csv'):
        data = b''
        with open('../reciklažna_dvorišta.csv', 'rb') as file:
            data += file.read()
        response = construct_response(200, "plain", data)
        sock.send(response)
    elif (path == b'/main.js'):
        data = b''
        with open('../res/scripts/main.js', 'rb') as file:
            data += file.read()
        response = construct_response(200, "application/javascript", data)
        sock.send(response)
    elif ( path.startswith(b'/api/') ):
        data = api(path)
        if data:
            response = construct_response(200, "application/json", data)
            sock.send(response)
        else:
            response = construct_response(404)
            sock.send(response)
    else:
        response = construct_response(404)
        sock.send(response)

async def serve_connection(sock):
    data = sock.recv(1024)
    requests = data.split(b'\r\n\r\n')
    for request in requests:
        serve_request(sock, request)
    sock.close()

def run_server(acc_addr, port):
    sock_tcp = socket.create_server((acc_addr, port), family=socket.AF_INET)

    while True:
        conn_socket, addr = sock_tcp.accept()
        print(f"Recieved request from {addr[0]}:{addr[1]}")
        asyncio.run(serve_connection(conn_socket))

    sock_tcp.close(sock_tcp)
