import socket
from _thread import *
import pickle
from game import Game
from player import Player


#############################SERVER INITIALIZATION####################
server = "192.168.1.86"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")
#####################################################################


#################GAME INITIALIZATION######################
game = Game()
##########################################################


def threaded_client(conn, id):

    #######################PLAYER INITIALIZATION########################

    # encodes and sends the player number to the client
    conn.send(str.encode(str(id)))

    # receives the player name from the client
    name = conn.recv(4096).decode()

    # creates a new player object
    player = Player(name, id)

    # adds new player object into the games list
    game.add_player(player)

    if game.player_count() == 3:
        game.gameOn = True
        game.shuffle()
        game.fill_circles()
        # game.populate_walls()
        game.first_player_move(0)

    ###################################################################

    ############CLIENT-SERVER COMMUNICATION LOOP##################
    while True:
        try:
            data = conn.recv(4096).decode()

            if data == "DISCONNECT":
                conn.send(str.encode(
                    "You disconnected from the server..."))
                break

            elif data == "get":
                conn.sendall(pickle.dumps(game))

            elif data == "confirm":
                if game.active_player_id() == id and game.circle_pointer != None and game.tile_pointer != None:
                    game.players[id].take_tiles(game)
                    game.next_player_move()

            elif data.startswith("select_circle"):
                circle = int(data[-1])
                game.select_circle(circle)

            elif data == "toggle_tile":
                game.toggle_tile()

            elif data.startswith("toggle_block"):
                b = int(data[-1])
                game.players[id].toggle_block_pointer(b)

            elif data == "ready":
                game.players[id].play_again = True
                count = 0
                for player in game.players:
                    if player.play_again == True:
                        count += 1
                if count == 3:
                    game.play_again()

            else:
                pass

        except:
            break

    #################################################################

    print("Lost connection")
    conn.close()

    ##################################################################


####################MAIN SERVER LOOP##################################
while True:

    conn, addr = s.accept()
    print("Connected to:", addr)

    gameId = game.player_count()

    start_new_thread(threaded_client, (conn, gameId))
######################################################################
