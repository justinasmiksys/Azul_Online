Rules of the game: https://youtu.be/dXuucWGrFMQ

This is a board game, which can be played by 3 people on the local network.

CONTENTS:

- static.py: functions which are used my client.py in order to draw elements of the game

- network.py: network object that is used by client.py in order to establsh the connection between the client and the server.
server and port attributes might have to be adjusted

- player.py: player object which contains all the current state of the player and is used by the client.py

- client.py: the main script that runs on the client side, sending/receiving the data to/from the server, updating the client view and allowing to make moves

- game.py: game object, which contains all the data about players and the game and is used by the server.py

- server.py: the main script that runs the server side


REQUIRED LIBRARIES:
- socket
- thread
- pickle
- pygame
- random
- tkinter
