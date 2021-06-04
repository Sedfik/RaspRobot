import socket
import time


HOST = ''
PORT = 10223
BUFF_SIZE = 1024

#SERVER_HOST = '10.42.0.137'
SERVER_HOST= '192.168.1.1'
SERVER_PORT = 9000

MESSAGE_FREQUENCY = 1/10


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((SERVER_HOST, SERVER_PORT))

client.send(b"register vteam")

robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robot.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
robot.connect((HOST, PORT))


mouvement = False
turning = False

# Create socket to robot server
client.settimeout(0.1)
while True:
    try:
        data = client.recv(BUFF_SIZE).decode()
        print('Received: ' + data)
    except:
        data = None
        if mouvement:
            robot.send(b"DS")
        if turning:
            robot.send(b"TS")
        mouvement = False
        turning = False
        print("Nothing received")
        continue      
    if "forward" in data:
        mouvement = True
        robot.send(b"forward")
    elif "backward" in data:
        mouvement = True
        robot.send(b"backward")
    elif "left" in data:
        turning = True
        robot.send(b"left")
    elif "right" in data:
        turning = True
        robot.send(b"right")
    else:
        print("unknown command")
        # robot.send(b"DS")
    time.sleep(MESSAGE_FREQUENCY)


# forward = b"forward"
# backwardStop = b"backward"
# #client.send(forward)
# time.sleep(2)
# #client.send(backwardStop)
# time.sleep(2)
# client.send(b"DS")

# client.close()
