"""chat client."""
import socket
import select
import sys
import getpass
import json
import re


def message_form(types, content):
    return json.dumps({"type": types, "content": content}).encode('utf-8')


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


def login():
    sys.stdout.write('Hello world, please login!\n')
    id = input("ID: ")
    pw = getpass.getpass("PASSWORD: ")
    sys.stdout.flush()
    return {"id": id, "password": pw}

# main function
if __name__ == "__main__":

    if(len(sys.argv) < 3):
        print ('Usage : python telnet.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect.')
        sys.exit()

    s.send(message_form("login", login()))

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(
            socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
                try:
                    data = json.loads(sock.recv(4096).decode('utf-8'))
                    if not data:
                        print ('\nDisconnected from chat server')
                        sys.exit()
                    elif data['type'] == 'login':
                        if(data['content'] == "True"):
                            print("login succeed")
                            print (
                                'Connected to remote host. Start chat app'
                            )
                            prompt()
                        else:
                            print("login failed.")
                            s.send(message_form("login", login()))

                    elif data['type'] == 'invitation':
                        answer = input(data['content']['message'])
                        s.send(message_form("invitation", {"state": "response", "answer": answer}))
                        prompt()
                    else:
                        # print data
                        sys.stdout.write(data["content"])
                        prompt()
                except Exception as e:
                    print(e)
                    break

            # user entered a message
            else:
                msg = sys.stdin.readline()
                m = re.search(r'^!invite[\s]*([a-zA-Z])', msg,)
                if (m):
                    # 초대 보내기
                    target = m.group(1)
                    s.send(message_form(
                        "invitation", {"state": "request", "target": target}))
                    prompt()
                else:
                    # 그냥 메세지 보내기
                    s.send(message_form("message", msg))
                    prompt()
    s.close()
