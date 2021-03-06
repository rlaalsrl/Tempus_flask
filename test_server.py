import socket
import argparse
import threading
import time

host = "127.0.0.1"
port = 4000
user_list = {}
notice_flag = 0

def msg_func(msg):
    print(msg)
    for con in user_list.valus():
        try:
            con.send(msg.encode('utf-8'))
        except:
            print("연결이 비정사적으로 종료된 소켓 발견")

def handle_receive(client_socket,addr,user):
    msg = "---- %s 님이 들어오셨습니다. ----"%user
    msg_func(msg)
    while 1:
        data = client_socket.recv(1024)
        string = data.decode('utf-8')

        if "/종료" in string:
            msg = " ---- %s님이 나가셨습니다. ----"%user
            del user_list[user]
            msg_func(msg)
            break
        string = "%s : %s" %(user, string)
        msg_func(string)
        client_socket.close()

def handle_notice(client_socket, addr, user):
    pass

def accept_func():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_socket.bind((host,port))

    server_socket.listen(5)

    while 1:
        try:
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            for user, con in user_list:
                con.close()
            server_socket.close()
            print("Keyboard interrupt")
            break
        user = client_socket.recv(1024).decode('utf-8')
        user_list[user] = client_socket

        notice_thread = threading.Thread(target=handle_notice, args=(client_socket, addr, user))
        notice_thread.daemon = True
        notice_thread.start()

        receive_thread = threading.Thread(target=handle_receive, args=(client_socket, addr,user))
        receive_thread.daemon = True
        receive_thread.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="\nJoo's server\n-p port\n")
    parser.add_argument('-p', help="port")

    args = parser.parse_args()
    try:
        port = int(args.p)
    except:
        pass
    accept_func()

