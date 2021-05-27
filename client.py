import pygame
from player import Player
from network import Network
import pickle
from static import *
pygame.font.init()

##############################STATIC SETTINGS#################
width = 1200
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Azul client")
border = 30
win.fill(background)
win.blit(logo, (300, 100))
pygame.display.update()

################################################################


def redrawWindow(win, game, n):

    win.fill(background)
    draw_static(win, game, n)
    draw_circle_content(win, game)
    turn_check(win, game, n)
    drawPlayerContent(win, game, n)
    drawSelectionCircle(win, game)
    drawSelectionTile(win, game)
    drawBlockPointer(win, game, n)
    pygame.display.update()


def turn_check(win, game, n):

    if game.gameOn:
        font = pygame.font.SysFont("comicsans", 60)
        text = "Your turn"

        if not game.players[n.id].turn:
            for player in game.players:
                if player.turn == True:
                    text = player.name + " turn..."

        text = font.render(text, True, black, background)
        win.blit(text, (500, 50))


def controls(game, n):
    global run

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            n.client.send(str.encode("DISCONNECT"))
            message = n.client.recv(4096).decode()
            print(message)
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game.gameOn == False and game.end_game == True:
                    n.send_data("ready")

        if game.players[n.id].turn:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    n.send_data("confirm")

                elif event.key == pygame.K_KP1:
                    n.send_data("select_circle:0")

                elif event.key == pygame.K_KP2:
                    n.send_data("select_circle:1")

                elif event.key == pygame.K_KP3:
                    n.send_data("select_circle:2")

                elif event.key == pygame.K_KP4:
                    n.send_data("select_circle:3")

                elif event.key == pygame.K_KP5:
                    n.send_data("select_circle:4")

                elif event.key == pygame.K_KP6:
                    n.send_data("select_circle:5")

                elif event.key == pygame.K_KP7:
                    n.send_data("select_circle:6")

                elif event.key == pygame.K_KP8:
                    n.send_data("select_circle:7")

                elif event.key == pygame.K_SPACE:
                    n.send_data("toggle_tile")

                elif event.key == pygame.K_DOWN:
                    n.send_data("toggle_block_1")

                elif event.key == pygame.K_UP:
                    n.send_data("toggle_block_0")


def main():
    global game

    n = Network()

    run = True
    clock = pygame.time.Clock()

    print(f"Welcome {n.name}, you are player {n.id}")

    while run:

        try:
            game = n.send("get")

        except:
            run = False
            print("Couldn't get game")
            break

        redrawWindow(win, game, n)
        controls(game, n)


main()
