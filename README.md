# RaspRobot

## Structure 
### Server.py
The server handle socket connexion as described by the protocol.
- connect robotname
- register robotname
- ["forward", "backward", "left", "right", "speed"]

Dict is used to map robot and controller socket wich allows to only keep robot/team name as shared key for robot/controller.

### Controller.py
Controller program used to send keyboard events as cmd to the server

### Robot.py
Just file to map server cmd with correct cmd for the robot. Note that the robot handle messages with a defined frequency in order to handle when no messages is sent.

# How to use
- launch the server.py file.
- Modify controller HOST and PORT variable to match with server
- Do the same for variables SERVER_HOST/PORT in robot.py
- Launch robot.py on the robot
- Launch controller.py on the controller device

**Note:** The controller program use pynput libraries wich doesn't support WSL commands.