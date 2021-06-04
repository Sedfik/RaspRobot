import socket
from sys import exec_prefix
from threading import Thread, Lock
import _thread

UNKNOWN_EXCEPTION = b"unknown"
ALREADY_USED_EXCEPTION = b"already_used"
OK = b"ok"

ALLOWED_CMD = ["forward", "backward", "left", "right", "speed"]

ROBOTS = {
    "vteam2": {
        "robot": (("192.168.12.1",10223),"socket"),
        "controller": (("192.168.12.2",9000),"passocket")
    }
}

def find_robot(controller_socket, dictio):
    return [team for team, values in dictio.items() if values.get("controller")[1] == controller_socket][0]# if values.get("controller") == controller_socket}

# Server listing host and port
ADDRESS = '' # Localhost default
PORT = 9000

BUFF_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ADDRESS, PORT))
server.listen(1)

mutex = Lock()

print("Listening on: ", ADDRESS, ":", PORT)

def handle_client(client_socket, addr):
    while True:
        data = client_socket.recv(BUFF_SIZE).decode()
        if not data: break
        print('Received: ' + data)
        data_list = data.split(" ")
        print(data_list[0])
        if data_list[0] == "register":
            print("Register recieved")
            mutex.acquire()
            try:
                print(repr(data_list[1]))
                if data_list[1] in ROBOTS.keys():
                    print(ALREADY_USED_EXCEPTION)
                    exception = ALREADY_USED_EXCEPTION
                    raise Exception(ALREADY_USED_EXCEPTION)
                else:
                    ROBOTS[data_list[1]] = {"robot" : (addr, client_socket)}
                    print("New robot added added")
                    client_socket.send(OK)
                    print(ROBOTS)
            except Exception as e:
                print("Exception : {} raised".format(e))
                client_socket.send(exception)
                break
            finally:
                mutex.release()
            break
        elif data_list[0] == "connect":
            print("connect received")
            mutex.acquire()
            try:
                print(repr(data_list[1]))
                if data_list[1] in ROBOTS.keys():
                    if "controller" in ROBOTS.get(data_list[1]).keys():
                        print(ALREADY_USED_EXCEPTION)
                        exception = ALREADY_USED_EXCEPTION
                        raise Exception(ALREADY_USED_EXCEPTION)
                    else:
                        ROBOTS.get(data_list[1])["controller"] = (addr, client_socket)
                        print("New controller added")
                        client_socket.send(OK)
                        print(ROBOTS)
                else:
                    print(UNKNOWN_EXCEPTION)
                    exception = UNKNOWN_EXCEPTION
                    raise Exception(UNKNOWN_EXCEPTION)
            except Exception as e:
                print("Exception : {} raised".format(e))
                client_socket.send(exception)
                break
            finally:
                mutex.release()
        elif data_list[0] in ALLOWED_CMD:
            mutex.acquire()
            try:
                if data_list[0] == "speed":
                    quantity = data_list[1]
                    print(quantity)
                    break
                else: # Just forward
                    team = find_robot(client_socket, ROBOTS)
                    print(team)
                    # Handle if robot is ""
                    socket = ROBOTS.get(team).get("robot")[1] 
                    print(socket)
                    socket.send(data_list[0].encode())
            finally:
                mutex.release()
        else: 
            print("unknown command")
        
        # send_to = ROBOTS.get("vteam").get("robot")

        # print("Forwarding to : vteam")
        # print("message: ",data)
        # robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # robot.connect(send_to)
        # robot.send(data.encode())
    # client_socket.close()

while True:
    client_socket, addr = server.accept()
    print('Connection from ', addr)
    Thread(target = handle_client , args = (client_socket, addr)).start()
    # print('Closing client connection')
    # client.close()
    # print('Closing server.')
    # server.close()

# data = client.recv(BUFF_SIZE).decode()
# if data:
#     print('Received: ' + data)
#     send_to = ROBOTS.get("vteam")
    
#     print("Forwarding to : vteam")
#     print("message: ",data)

#     # robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # robot.connect(send_to)
#     # robot.send(data.encode())
# else:
#     print("No message recieved")
