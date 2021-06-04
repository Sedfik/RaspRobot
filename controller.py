import socket
import time
from threading import Lock
from pynput.keyboard import Listener, Key
from pynput import keyboard

HOST = '127.0.0.1'
PORT = 9000
BUFF_SIZE = 1024

MESSAGE_FREQUENCY = 1/10

CURRENT_KEY = ""
mutex = Lock()

local_current_speed = 100

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((HOST, PORT))

client.send(b"connect vteam")

def run_client_cmd():
    # mutex.acquire()
    while CURRENT_KEY != "Key.esc":
        handle_client_cmd(CURRENT_KEY)
        # mutex.release()
        time.sleep(MESSAGE_FREQUENCY)
    return 1

def on_press(key):
    CURRENT_KEY = key
    print(f"New key: {CURRENT_KEY}")
    handle_client_cmd(CURRENT_KEY)
    time.sleep(MESSAGE_FREQUENCY)

def on_release(key):
    mutex.acquire()
    CURRENT_KEY = ""
    print(f"Release key {CURRENT_KEY}")
    handle_client_cmd(CURRENT_KEY)
    mutex.release()
    time.sleep(MESSAGE_FREQUENCY)

def handle_client_cmd(key):
    print(f"key: {CURRENT_KEY}")
    if str(key) == "'q'":
        print('Left')
        client.send(b'left')
        # return False
    elif str(key) == "'z'":
        print('Forward')
        client.send(b'forward')
        # return False
    elif str(key) == "'d'":
        print('Right')
        client.send(b'right')
        # return False
    elif str(key) == "'s'":
        print('Back')
        client.send(b'backward')
        # return False
    elif str(key) == "Key.space": 
        print('Stop')
        client.send(b'DS')
        return False
    elif str(key) == "Key.esc":
        print("Return")
        return False
    elif str(key) == "'a'":
        print('Accelerate')
        new_local_current_speed = min(local_current_speed + 10, 100)
        local_current_speed_str = "local_current_speed " + str(new_local_current_speed)
        client.send(local_current_speed_str.encode())
    elif str(key) == "'e'":
        print('Slow down')
        new_local_current_speed = max(local_current_speed - 10, 50)
        local_current_speed_str = "local_current_speed " + str(new_local_current_speed)
        client.send(local_current_speed_str.encode())    
    else:
        print('Unknown command')
        # return False

listener = keyboard.Listener(on_press = on_press, on_release = on_release)
listener.start()
run_client_cmd()

# forward = b"forward"
# backwardStop = b"backward"
# #client.send(forward)
# time.sleep(2)
# #client.send(backwardStop)
# time.sleep(2)
# client.send(b"DS")

# client.close()