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
        is_hit = False
        for b in self.battleships:
            idx = b.body_index(shot_location)
            if idx is not None:
                is_hit = True
                b.hits[idx] = True
                break

        self.shots.append((Shot(shot_location, is_hit)))

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

        return Battleship(body)

    def __init__(self, body):
        self.body = body
        self.hits = [False] * len(body)

    def body_index(self, location):
        try:
            return b.body.index(location)
        except ValueError:
            return None


def render(board_width, board_height, shots):
    header = "+" + "-" * board_width + "+"
    print(header)

    shots = set(shots)
    for y in range(board_height):
        row = []
        for x in range(board_width):
            if (x, y) in shots:
                ch = "X"
            else:
                ch = " "
            row.append(ch)
        print("|" + "".join(row) + "|")
        print("|" + " " * board_width + "|")

    print(header)


def render_battleships(board_width, board_height, battleships):
    header = "+" + "-" * board_width + "+"
    print(header)

    # make board
    board = []
    for x in range(board_width):
        row = []
        for y in range(board_height):
            row.append(None)
        board.append(row)

    # add battleships
    for b in battleships:
        for x, y in b.body():
            board[x][y] = "O"

    for y in range(board_height):
        row = []
        for x in range(board_width):
            row.append((x, y))
        print("".join(row))
    
    print(header)


if __name__ == "__main__":
    battleships = [
        Battleship.build((1, 1), 2, "N"),
        Battleship.build((5, 8), 5, "N"),
        Battleship.build((2, 3), 4, "E")
    ]

    for b in battleships:
        print(b.body)

    game_board = GameBoard(battleships, 10, 10)
    shots = [(1, 1), (0, 0), (5, 7)]
    for sh in shots:
        game_board.take_shot(sh)

    for sh in game_board.shots:
        print(sh.location)
        print(sh.is_hit)
        print("==========")
    for b in game_board.battleships:
        print(b.body)
        print(b.hits)
        print("==========")
    print(game_board.shots)
    print(game_board.battleships)

    exit(0)

    shots = []

    while True:
        inp = input("Where do you want to shoot?\n")
        x, y = inp.split(",")
        x = int(x)
        y = int(y)
        shots.append((x, y))
        render(10, 10, shots)
