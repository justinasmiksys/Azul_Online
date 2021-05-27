import pygame
pygame.font.init()


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (178, 219, 127)
blue = (0, 0, 255)
yellow = (255, 255, 0)
grey = (209, 199, 183)
arrow = (199, 54, 141)
background = (54, 173, 209)

logo = pygame.image.load(r'azul_new.jpg')

border = 30

colors = [white, red, blue, yellow, black]

seq = {
    0: [0, 1, 2],
    1: [1, 2, 0],
    2: [2, 0, 1]
}

player_coordinates = ((10, 550), (10, 50), (850, 50))


def drawPenaltyNumbers(surface, text_input, position):
    font_1 = pygame.font.SysFont('comicsans', 18)
    text = font_1.render(text_input, True, black, background)
    textRect = text.get_rect()
    textRect.center = position
    surface.blit(text, textRect)


def drawPlayerBoard(surface, position):
    global border
    x0 = position[0]
    y0 = position[1]

    # draws the blocks borders
    for i in range(5, 0, -1):
        for j in range(4, 4-i, -1):
            pygame.draw.rect(surface, black, (x0+(i-1)*border,
                                              y0+border*j, border, border), 2)

    # draws the wall borders
    for i in range(5):
        for j in range(5):
            pygame.draw.rect(surface, black, (x0+5*border +
                                              20+i*border, y0+j*border, border, border), 2)

    color_pattern = (
        (blue, yellow, red, black, white),
        (white, blue, yellow, red, black),
        (black, white, blue, yellow, red),
        (red, black, white, blue, yellow),
        (yellow, red, black, white, blue)
    )

    # draws the wall color markers
    for i in range(5):
        for j in range(5):
            pygame.draw.circle(
                surface, color_pattern[i][j], (x0+20+border*(5.5+j), y0+border*(0.5+i)), 5)

    # draws penalty section
    for i in range(7):
        pygame.draw.rect(surface, black, (x0+i*border,
                                          y0+5*border+border, border, border), 2)

    yy = y0+7.5*border
    drawPenaltyNumbers(surface, '-1', (x0+0.5*border, yy))
    drawPenaltyNumbers(surface, '-1', (x0+1.5*border, yy))
    drawPenaltyNumbers(surface, '-2', (x0+2.5*border, yy))
    drawPenaltyNumbers(surface, '-2', (x0+3.5*border, yy))
    drawPenaltyNumbers(surface, '-2', (x0+4.5*border, yy))
    drawPenaltyNumbers(surface, '-3', (x0+5.5*border, yy))
    drawPenaltyNumbers(surface, '-3', (x0+6.5*border, yy))


def drawCircleNumbers(surface, text_input, position):
    font_1 = pygame.font.Font('freesansbold.ttf', 18)
    text = font_1.render(text_input, True, black, grey)
    textRect = text.get_rect()
    textRect.center = position
    surface.blit(text, textRect)


def drawPointsText(surface, position, text_input, font_size):
    font_1 = pygame.font.SysFont("comicsans", font_size)
    text = font_1.render(text_input, True, black, background)
    textRect = text.get_rect()
    textRect.center = position
    surface.blit(text, textRect)


def drawBoard(surface, game, n):
    global height, width
    circle_radius = 60
    pygame.draw.circle(surface, grey, (470, 170), circle_radius)
    pygame.draw.circle(surface, grey, (650, 170), circle_radius)
    pygame.draw.circle(surface, grey, (780, 340), circle_radius)
    pygame.draw.circle(surface, grey, (720, 510), circle_radius)
    pygame.draw.circle(surface, grey, (565, 600), circle_radius)
    pygame.draw.circle(surface, grey, (410, 510), circle_radius)
    pygame.draw.circle(surface, grey, (330, 340), circle_radius)

    drawCircleNumbers(surface, '1', (470, 130))
    drawCircleNumbers(surface, '2', (650, 130))
    drawCircleNumbers(surface, '3', (780, 300))
    drawCircleNumbers(surface, '4', (720, 470))
    drawCircleNumbers(surface, '5', (565, 560))
    drawCircleNumbers(surface, '6', (410, 470))
    drawCircleNumbers(surface, '7', (330, 300))

    drawPointsText(surface, (900, 650),
                   'Game ends when one of the players fill the line', 30)
    drawPointsText(surface, (900, 690), '+2 for a full line', 30)
    drawPointsText(surface, (900, 730), '+7 for a full column', 30)
    drawPointsText(surface, (900, 770), '+10 for a full color', 30)

    for i, ID in enumerate(seq[n.id]):

        drawPlayerBoard(surface, player_coordinates[i])

        (x, y) = (player_coordinates[i][0] +
                  150, player_coordinates[i][1] - 20)
        player = game.players[ID]

        drawPointsText(surface, (x, y),
                       f'{player.name}   Score: {player.score}', 40)


def drawWaiting(surface, game):
    font = pygame.font.SysFont("comicsans", 60)
    surface.blit(logo, (300, 100))
    line1 = "Players in lobby:"
    lines = []
    lines.append(line1)
    for player in game.players:
        lines.append(player.name)
    for i, line in enumerate(lines):
        text = font.render(line, True, black, background)
        surface.blit(text, (50, 500+i*60))


def drawFinalScore(surface, game):

    standings = sorted(
        game.players, key=lambda player: player.score, reverse=True)

    font = pygame.font.SysFont("comicsans", 60)
    line1 = "Game over!"
    line2 = "Final standings:"
    lines = []

    lines.append(line1)
    lines.append(line2)

    for i in range(3):
        state = ''
        if standings[i].play_again == True:
            state = '   Ready'
        line = f"{i+1}. {standings[i].name} {standings[i].score} {state}"
        lines.append(line)

    for i, line in enumerate(lines):
        text = font.render(line, True, black, background)
        surface.blit(text, (400, 200+i*60))


def draw_static(surface, game, n):

    if game.gameOn == True:
        drawBoard(surface, game, n)
    else:
        if game.end_game == True:
            drawFinalScore(surface, game)
        else:
            drawWaiting(surface, game)


def drawTile(tile, surface):
    pygame.draw.rect(surface, tile.color, (tile.x, tile.y, border-5, border-5))


def draw_circle_content(surface, game):
    global border

    if game.gameOn:

        for circle in game.circles:
            for i in range(len(circle.content)):
                drawTile(circle.content[i], surface)

        x = 475
        y = 300

        for i, tile in enumerate(game.middle):
            if i > 0 and i % 5 == 0:
                x = 475
                y += border
            pygame.draw.rect(surface, tile.color, (x, y, border-5, border-5))
            x += border


def drawSelectionCircle(surface, game):

    dx, dy = 30, 25
    if game.circle_pointer != None:
        if game.circle_pointer != 7:
            pygame.draw.circle(
                surface, red, (game.circles[game.circle_pointer].x+dx, game.circles[game.circle_pointer].y+dy), 60, width=5)
        else:
            pygame.draw.rect(surface, red, (465, 290, 160, 160), 3)


def drawSelectionTile(surface, game):
    global border

    if game.circle_pointer != None and game.tile_pointer != None:
        if game.circle_pointer != 7:
            circle = game.circles[game.circle_pointer]
            tile = game.tile_pointer
            pygame.draw.rect(surface, red, (circle.content[tile].x -
                                            3, circle.content[tile].y-3, 30, 30), 2)
        else:
            x = 475 + (game.tile_pointer % 5)*border
            y = 300 + (game.tile_pointer // 5)*border
            pygame.draw.rect(surface, red, (x - 3, y-3, 30, 30), 2)


def drawBlockPointer(surface, game, n):
    global seq, player_coordinates, border

    if game.gameOn:
        player_id = game.active_player_id()
        player = game.players[player_id]

        for i, num in enumerate(seq[n.id]):
            if num == player_id:
                x = player_coordinates[i][0]
                y = player_coordinates[i][1]

        x = x+border*5+20
        y = y+10+(player.block_pointer*border)
        pygame.draw.polygon(surface, arrow, ((x, y), (x, y+10), (x-10, y+10),
                                             (x-10, y+15), (x-20, y+5), (x-10, y-5), (x-10, y)))


def drawPlayerContent(surface, game, n):
    global seq, player_coordinates, border

    if game.gameOn:

        for i, ID in enumerate(seq[n.id]):

            (x, y) = (player_coordinates[i][0], player_coordinates[i][1])
            player = game.players[ID]

            # DRAW THE BLOCK PART
            for b, block in enumerate(player.blocks):
                for t, tile in enumerate(block):
                    draw_x = x + 4*border - border*t + 3
                    draw_y = y + b*border + 3
                    pygame.draw.rect(surface, tile.color,
                                     (draw_x, draw_y, border-5, border-5))

            # DRAW THE PENALTY PART
            for t, tile in enumerate(player.penalty):
                draw_x = x + border*t + 3
                draw_y = y + 6*border + 3
                pygame.draw.rect(surface, tile.color,
                                 (draw_x, draw_y, border-5, border-5))
                if t == 6:
                    break

            # DRAW THE WALL PART
            for row in range(5):
                for col in range(5):
                    if player.wall[row][col] != None:
                        tile = player.wall[row][col]
                        draw_x = x + border*5 + 23 + col*border
                        draw_y = y + border*row + 3
                        pygame.draw.rect(surface, tile.color,
                                         (draw_x, draw_y, border-5, border-5))
