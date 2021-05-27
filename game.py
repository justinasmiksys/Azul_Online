import random

circle_coords = ((440, 145),
                 (620, 145),
                 (750, 315),
                 (690, 485),
                 (535, 575),
                 (380, 485),
                 (300, 315))


class Game:

    def __init__(self):
        self.players = []
        self.gameOn = False
        self.all_tiles = []
        self.circles = []
        self.circle_pointer = None
        self.tile_pointer = 0
        self.middle = []
        self.end_game = False
        self.first_player_tile = None

        for color in colors:
            for number in range(1, 51):
                self.all_tiles.append(Tile(color, number, 0, 0))

        for i in range(7):
            self.circles.append(
                Circle(circle_coords[i][0], circle_coords[i][1]))

    def populate_walls(self):
        for player in self.players:
            for line in player.wall:
                for i in range(5):
                    line[i] = self.deal_one()

    def add_player(self, player):
        self.players.append(player)

    def player_count(self):
        return len(self.players)

    def first_player_move(self, player_id):
        self.players[player_id].turn = True

    def active_player_id(self):
        for i in range(self.player_count()):
            if self.players[i].turn == True:
                return i

    def next_player_move(self):
        current_player_id = self.active_player_id()
        self.players[current_player_id].turn = False

        if current_player_id == 2:
            self.players[0].turn = True
        else:
            self.players[current_player_id+1].turn = True

        self.circle_pointer = None
        self.tile_pointer = None

    def deal_one(self):
        return self.all_tiles.pop()

    def shuffle(self):
        random.shuffle(self.all_tiles)

    def fill_circles(self):

        self.first_player_tile = Tile(arrow, 0, 0, 0)

        self.middle.append(self.first_player_tile)

        for circle in self.circles:
            color_count = 0
            while True:
                for _ in range(4):
                    circle.add_tile(self.deal_one())
                    if circle.content[-1].color == circle.content[0].color:
                        color_count += 1
                if color_count == 4:
                    circle.content = []
                    color_count = 0
                else:
                    break

    def select_circle(self, circle):

        if circle != 7:
            if len(self.circles[circle].content) != 0:
                self.circle_pointer = circle
                self.tile_pointer = 0
        else:
            if len(self.middle) != 0:
                self.circle_pointer = 7
                self.tile_pointer = 0

    def toggle_tile(self):
        if self.circle_pointer != None:
            if self.circle_pointer != 7:
                current_circle_tiles = self.circles[self.circle_pointer].content
            else:
                current_circle_tiles = self.middle

            if self.tile_pointer == len(current_circle_tiles) - 1:
                self.tile_pointer = 0
            else:
                self.tile_pointer += 1

    def round_end_check(self):
        for circle in self.circles:
            if len(circle.content) != 0:
                return
        if len(self.middle) != 0:
            return
        self.end_round()
        self.new_round()

    def end_round(self):

        for player in self.players:
            # emptying full blocks/filling the wall
            for b, block in enumerate(player.blocks):
                if len(block) == b + 1:

                    block_color = block[0].color
                    wall_index = None

                    for i, color in enumerate(wall_pattern[b]):
                        if color == block_color:
                            wall_index = i
                            break

                    player.wall[b][i] = block.pop()
                    player.blocks[b] = []
                    player.add_points(b, i)
            player.subtract_penalty()

    def new_round(self):

        self.all_tiles = []

        for color in colors:
            for number in range(1, 51):
                self.all_tiles.append(Tile(color, number, 0, 0))

        self.shuffle()
        self.fill_circles()

        for player in self.players:
            if player.first_player_tile == True:
                player.turn = True
                player.first_player_tile = False
            else:
                player.turn = False

        self.next_player_move()
        self.next_player_move()

    def game_end_check(self):

        count = 0

        for player in self.players:
            for wall_line in player.wall:
                for element in wall_line:
                    if element != None:
                        count += 1
                if count == 5:
                    self.end_game = True
                    return
                else:
                    count = 0

    def game_end(self):

        for player in self.players:

            lines = [0, 0, 0, 0, 0]
            columns = [0, 0, 0, 0, 0]
            colors = {(0, 0, 0): 0, (255, 255, 255): 0,
                      (255, 0, 0): 0, (0, 0, 255): 0, (255, 255, 0): 0}

            for row in range(len(player.wall)):
                for col in range(len(player.wall[row])):
                    if player.wall[row][col] != None:
                        lines[row] += 1
                        columns[col] += 1
                        color = player.wall[row][col].color
                        colors[color] += 1

            color_list = ((0, 0, 0), (255, 255, 255),
                          (255, 0, 0), (0, 0, 255), (255, 255, 0))

            lines_total = 0
            columns_total = 0
            colors_total = 0

            for i in range(5):
                if lines[i] == 5:
                    lines_total += 1
                if columns[i] == 5:
                    columns_total += 1
                if colors[color_list[i]] == 5:
                    colors_total += 1

            extra_points = 2*lines_total + 7*columns_total + 10*colors_total

            player.score += extra_points

        self.gameOn = False

    def play_again(self):

        for player in self.players:
            player.reset()

        self.gameOn = True
        self.all_tiles = []
        self.circles = []
        self.circle_pointer = None
        self.tile_pointer = 0
        self.middle = []
        self.end_game = False
        self.first_player_tile = None

        for color in colors:
            for number in range(1, 51):
                self.all_tiles.append(Tile(color, number, 0, 0))

        self.shuffle()
        self.fill_circles()
        # self.populate_walls()
        self.first_player_move(0)


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
arrow = (199, 54, 141)


colors = [white, red, blue, yellow, black]

wall_pattern = (
    (blue, yellow, red, black, white),
    (white, blue, yellow, red, black),
    (black, white, blue, yellow, red),
    (red, black, white, blue, yellow),
    (yellow, red, black, white, blue)
)


class Tile:

    def __init__(self, color, number, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.number = number


class Circle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.content = []

    def add_tile(self, tile):
        # spacing between the tiles inside the circle
        border = 30
        spacing = 5
        self.content.append(tile)
        count = len(self.content)
        # sets the tile coordinates depending on the circle coordinates and the position inside the circle
        if (count == 1 or count == 2):
            self.content[-1].y = self.y
            if count == 1:
                self.content[-1].x = self.x
            elif count == 2:
                self.content[-1].x = self.x+spacing+border
        else:
            self.content[-1].y = self.y + border
            if count == 3:
                self.content[-1].x = self.x
            elif count == 4:
                self.content[-1].x = self.x+spacing+border
