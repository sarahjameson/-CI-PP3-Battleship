# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

class GameBoard(object):

    def __init__(self, battleships, board_width, board_height):
        self.battleships = battleships
        self.shots = []
        self.board_width = board_width
        self.board_height = board_height

    # update battleship with hits
    # save if hit or miss
    def take_shot(self, shot_location):
        hit_battleship = None
        is_hit = False
        for b in self.battleships:
            idx = b.body_index(shot_location)
            if idx is not None:
                is_hit = True
                b.hits[idx] = True
                hit_battleship = b
                break

        self.shots.append((Shot(shot_location, is_hit)))
        return hit_battleship

    # game over function


class Shot(object):

    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit


class Battleship(object):

    @staticmethod
    def build(head, length, direction):
        body = []
        for i in range(length):
            if direction == "N":
                el = (head[0], head[1] - i)
            elif direction == "S":
                el = (head[0], head[1] + i)
            elif direction == "W":
                el = (head[0] - i, head[1])
            elif direction == "E":
                el = (head[0] + i, head[1])

            body.append(el)

        return Battleship(body, direction)


    def __init__(self, body, direction):
        self.body = body
        self.direction = direction
        self.hits = [False] * len(body)


    def body_index(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None


    # destroyed function


# player class


def render(game_board, show_battleships=False):
    header = "+" + "-" * game_board.board_width + "+"
    print(header)

    # Construct empty board
    board = []
    for _ in range(game_board.board_width):
        board.append([None for _ in range(game_board.board_height)])

    if show_battleships:
        # Add the battleships to the board
        for b in game_board.battleships:
            for i, (x, y) in enumerate(b.body):
                if b.direction == "N":
                    chs = ("v", "|", "^")
                elif b.direction == "S":
                    chs = ("^", "|", "v")
                elif b.direction == "W":
                    chs = (">", "=", "<")
                elif b.direction == "E":
                    chs = ("<", "=", ">")
                else:
                    raise "Unknown direction"

                if i == 0:
                    ch = chs[0]
                elif i == len(b.body) - 1:
                    ch = chs[2]
                else:
                    ch = chs[1]
                board[x][y] = ch

    # Add the shots to the board
    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            ch = "X"
        else:
            ch = "@"
        board[x][y] = ch

    for y in range(game_board.board_height):
        row = []
        for x in range(game_board.board_width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(header)




if __name__ == "__main__":
    battleships = [
        Battleship.build((1, 1), 2, "N"),
        Battleship.build((5, 8), 5, "N"),
        Battleship.build((2, 3), 4, "E")
    ]

    game_board = GameBoard(battleships, 10, 10)
    shots = [(1, 1), (0, 0), (5, 7)]
    for sh in shots:
        game_board.take_shot(sh)

    render(game_board)

    for sh in game_board.shots:
        print(sh.location)
        print(sh.is_hit)
        print("==========")
    for b in game_board.battleships:
        print(b.body)
        print(b.hits)
        print("==========")
   
    render(10, 10, game_board.shots)

    exit(0)

    shots = []

    while True:
        inp = input("Where do you want to shoot?\n")
        x, y = inp.split(",")
        x = int(x)
        y = int(y)
        shots.append((x, y))
        render(10, 10, shots)
