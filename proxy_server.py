import socket
import urllib.request


HOST, PORT = '', 8000

#establishing socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print("Listening to port", PORT)

while True:
    (client_connection, client_address) = listen_socket.accept()
    request = client_connection.recv(1024)

    request_path = request.split()

    # set method POST or GET
    method = request_path[0].decode('utf-8')

    # set url
    path = request_path[1].decode('utf-8')
    url = path[7:]

    #responding to client
    if (method == "GET"):
        headers = {}
        headers['user-agent'] = "curl/7.35.0"
        req = urllib.request.Request(url, headers=headers)
        r = urllib.request.urlopen(req)
        r_read = r.read()
        client_connection.send(r_read)
        client_connection.close()

    elif (method == "POST"):
        values = request_path[-1].decode('utf-8')
        val = values.split('&')
        v_d = {}

        for i in val:
            var = i.split('=')
            v_d[var[0]] = var[1]

        headers = {}
        headers['user-agent'] = "curl/7.35.0"

        data = urllib.parse.urlencode(v_d)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        client_connection.send(respData)
        client_connection.close()
