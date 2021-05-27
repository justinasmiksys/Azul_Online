class Player:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.score = 0
        self.turn = False
        self.first_player_tile = False
        self.blocks = [[], [], [], [], []]
        self.wall = [[None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None]]
        self.penalty = []
        self.block_pointer = 0
        self.play_again = False

    def toggle_block_pointer(self, b):

        if b == 1 and self.block_pointer < 4:
            self.block_pointer += 1
        elif b == 0 and self.block_pointer > 0:
            self.block_pointer -= 1
        else:
            pass

    def take_tiles(self, game):

        circle_num = game.circle_pointer

        if circle_num != 7:
            tiles = game.circles[circle_num].content
        else:
            tiles = game.middle

        tile_num = game.tile_pointer
        selected_block = self.blocks[self.block_pointer]
        color = tiles[tile_num].color
        match = []
        unmatch = []

        for _ in range(len(tiles)):
            if tiles[-1].color == color:
                match.append(tiles.pop())
            else:
                unmatch.append(tiles.pop())

        if game.first_player_tile in unmatch:
            self.penalty.append(unmatch.pop())
            self.first_player_tile = True

        wall_colors = []
        for i in range(5):
            if self.wall[self.block_pointer][i] != None:
                wall_colors.append(self.wall[self.block_pointer][i].color)

        if (len(selected_block) == 0 or match[0].color == selected_block[0].color) and color not in wall_colors:
            available_spots = self.block_pointer - len(selected_block) + 1
            for _ in range(available_spots):
                if len(match) != 0:
                    selected_block.append(match.pop())

        for _ in range(len(match)):
            self.penalty.append(match.pop())

        for _ in range(len(unmatch)):
            game.middle.append(unmatch.pop())

        game.round_end_check()
        game.game_end_check()

        if game.end_game == True:
            game.game_end()

    def add_points(self, row, col):

        hor, ver, final = 0, 0, 0

        # scan row left/right
        for i in range(col, 5):
            if self.wall[row][i] != None:
                hor += 1
            else:
                break

        for i in range(col-1, -1, -1):
            if self.wall[row][i] != None:
                hor += 1
            else:
                break

        # scan column up/down
        for i in range(row, 5):
            if self.wall[i][col] != None:
                ver += 1
            else:
                break

        for i in range(row-1, -1, -1):
            if self.wall[i][col] != None:
                ver += 1
            else:
                break

        if hor == 1 or ver == 1:
            final = hor + ver - 1
        else:
            final = hor + ver

        self.score += final

    def subtract_penalty(self):

        total = len(self.penalty)
        if total == 1:
            self.score -= 1
        elif total == 2:
            self.score -= 2
        elif total == 3:
            self.score -= 4
        elif total == 4:
            self.score -= 6
        elif total == 5:
            self.score -= 8
        elif total == 6:
            self.score -= 11
        elif total == 7:
            self.score -= 14

        self.penalty = []

    def reset(self):
        self.score = 0
        self.turn = False
        self.first_player_tile = False
        self.blocks = [[], [], [], [], []]
        self.wall = [[None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None],
                     [None, None, None, None, None]]
        self.penalty = []
        self.block_pointer = 0
        self.play_again = False
