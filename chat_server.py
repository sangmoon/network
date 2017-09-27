"""tcp Chat server."""
# To-do 각각의 사람들에 대해 메세지 큐를 만든다.
# 방에 참여한 사람이 로그아웃 한 경우, 큐에 메세지를 넣고 로그인 했을 때
# 다 보여준다.
import socket
import select
import json
# Function to broadcast chat messages to all connected clients


def broadcast_data(sock, message):
    # Do not send the message to master socket and the client who has
    # send us the message
    for _socket in CONNECTION_LIST:
        if (_socket != server_socket and
                _socket != sock and
                LOGIN_MAP.get(sock, None) in CHAT_MEMBER_LIST and
                LOGIN_MAP.get(_socket, None) in CHAT_MEMBER_LIST):
            try:
                # _socket.send(message.encode('utf-8'))
                _socket.send(message_form("message", message))
            except:
                # broken socket connection may be, chat client pressed
                # ctrl+c for example
                _socket.close()
                CONNECTION_LIST.remove(_socket)


def message_form(types, content):
    return (json.dumps({"type": types, "content": content})).encode('utf-8')


def login(idd, password):
    for user in USER_DB:
        if user["ID"] == idd and user["PASSWORD"] == password:
            return True
    return False

if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    CHAT_MEMBER_LIST = ["A", "B"]
    LOGIN_MAP = {}
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 5000
    USER_DB = [
        {"ID": "A", "PASSWORD": "123"}, {"ID": "B", "PASSWORD": "123"},
        {"ID": "C", "PASSWORD": "123"}, {"ID": "D", "PASSWORD": "123"}
    ]

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(4)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    print ("Chat server started on port " + str(PORT))

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(
            CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved
                # through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)

                broadcast_data(sockfd, "[%s] entered room\n" % str(LOGIN_MAP.get(sockfd, addr)))

            # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    # In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = json.loads(sock.recv(RECV_BUFFER))
                    print(LOGIN_MAP)
                    print("1")
                    if data:
                        print("2")
                        if data['type'] == "login":
                            print("3")
                            # login process
                            if login(
                                data['content']['id'],
                                data['content']['password']
                            ):
                                LOGIN_MAP[sock] = data['content']['id']
                                sock.send(message_form("login", "True"))
                            else:
                                sock.send(message_form("login", "False"))
                        elif data['type'] == "invitation":
                            if(data['content']['state'] == "request"):
                                # request 상황 시
                                print(4)
                                for _socket, _id in list(LOGIN_MAP.items()):
                                    if _id == data['content']['target']:
                                        _socket.send(message_form("invitation", {"state":"request","message":"You are invited for chat room, Y or N?"}))
                                        break
                            else:
                                # response 상황 시
                                print(5)
                                if data['content']['answer'] in ['Y', 'y']:
                                    CHAT_MEMBER_LIST.append(LOGIN_MAP[sock])
                                else:
                                    print("no this is error")
                        else:
                            # normal process
                            broadcast_data(sock, "\r" + '<' + str(
                                LOGIN_MAP[sock]) + '> ' + data["content"])

                except Exception as e:
                    print(e)
                    broadcast_data(sock, "Client (%s, %s) is offline\n" % addr)
                    print ("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    for key, value in list(LOGIN_MAP.items()):
                        if(sock == key):
                            del LOGIN_MAP[key]
                    continue

    server_socket.close()
