# Remote Control for multiple PCs

<img widht="640" height="360" src="https://raw.githubusercontent.com/TuinboonDev/remote_control/refs/heads/main/banner.png">

A simple yet usefull python project to control multiple PCs from one central PC

The project consists of three parts:
 - The server: responsible for relaying data from the master to the clients
 - The master terminal: responsible for sending commands to the clients/ server
 - The cleint terminal: responsible for receiving and executing commands

# How to use

You can get started by git cloning this repo and following the <a href="https://github.com/TuinboonDev/remote_control/raw/refs/heads/main/preview.mp4">preview video</a> but that doesnt do much.
However you can add commands at `code/master/gui.py:75` to make the server recognize these you can add a new case to `code/server/server.py:58` and to make the client actually do something edit: `code/client/client.py:68`

If you have any questions feel free to DM tuinboon on discord or slack
