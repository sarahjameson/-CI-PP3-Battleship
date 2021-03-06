import copy
import time
import random
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Setting up gspread use
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("winners").sheet1
COL = SHEET.col_values(1)


class GameBoard(object):

    def __init__(self, battleships, board_width, board_height):
        self.battleships = battleships
        self.shots = []
        self.board_width = board_width
        self.board_height = board_height

    def take_shot(self, shot_location):
        """
        Update battleship with hits and save whether a shot was a hit or miss.
        If hit, returns the battleship
        Otherwise, returns None
        """
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

    def is_game_over(self):
        """
        Keeps track of when game is over
        """
        return all([b.is_destroyed() for b in self.battleships])


class Shot(object):

    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit


class Battleship(object):

    @staticmethod
    def build(head, length, direction):
        """
        Builds battlship and returns it
        """
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

    def is_destroyed(self):
        """
        Checks if ship has been hit everywhere
        """
        return all(self.hits)


class Player(object):

    def __init__(self, name, shot_f):
        self.name = name
        self.shot_f = shot_f


def render(game_board):
    """
    Creates gameboard and adds any shots to the board
    """
    header = "+" + "-" * game_board.board_width + "+"
    print(header)

    # Construct empty board
    board = []
    for _ in range(game_board.board_width):
        board.append([None for _ in range(game_board.board_height)])

    # Add the shots to the board
    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            ch = "X"
        else:
            ch = "."
        board[x][y] = ch

    for y in range(game_board.board_height):
        row = []
        for x in range(game_board.board_width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(header)


def announce_en(event_type, metadata={}):
    """
    Makes announcements during game
    """
    if event_type == "game_over":
        print("%s WINS THE GAME! ????" % metadata["player"])
        winning_player = metadata["player"]
        add_winning_player(winning_player)
        go_back = input("Press any key and enter to go back:\n").lower()
        if go_back:
            os.system("clear")
            return welcome()
    elif event_type == "new_turn":
        print("%s YOUR TURN! ????" % metadata["player"])
    elif event_type == "miss":
        print("%s MISSED! ????" % metadata["player"])
    elif event_type == "battleship_destroyed":
        print("%s DESTROYED a battleship! ????" % metadata["player"])
    elif event_type == "battleship_hit":
        print("%s HIT a battleship! ????" % metadata["player"])
    else:
        print("UNKNOWN EVENT TYPE: %s" % event_type)


def add_winning_player(winning_player):
    """
    Adds winning player to gsheet so they
    can be remembered
    """
    insert_row = [winning_player]
    SHEET.insert_row(insert_row, 1)


def get_random_ai_shot(game_board):
    """
    Picks coordinates for computer's go
    """
    x = random.randint(0, game_board.board_width - 1)
    y = random.randint(0, game_board.board_height - 1)
    return (x, y)


def random_sleepy_ai(sleep_time):
    """
    Puts timer on computer's go
    """
    return sleepy_ai(get_random_ai_shot, sleep_time)


def sleepy_ai(ai_f, sleep_time):
    def f(game_board):
        time.sleep(sleep_time)
        return ai_f(game_board)
    return f


def get_human_shot(game_board):
    """
    Ask for human's coordinates
    """
    inp = input("""Where do you want to shoot?\n
Enter coordinates like 2,3 for example\n""")
    try:
        xstr, ystr = inp.split(",")
        x = int(xstr)
        y = int(ystr)
        if x > 9 or y > 9:
            return get_human_shot(game_board)
        return (x, y)
    except:
        print("Opps. Try again.")
        return get_human_shot(game_board)


def run(announce_f, render_f):
    name = input("Enter your name:\n")

    battleships = [
        Battleship.build((1, 1), 2, "N"),
        # Battleship.build((5, 8), 5, "N"),
        # Battleship.build((2, 3), 4, "E"),
        # Battleship.build((6, 6), 3, "S"),
        # Battleship.build((9, 9), 5, "W"),
    ]

    game_boards = [
        GameBoard(battleships, 10, 10),
        GameBoard(copy.deepcopy(battleships), 10, 10)
    ]

    players = [
        Player(name, get_human_shot),
        Player("Mr Robot", random_sleepy_ai(1.5)),
    ]

    offensive_idx = 0
    while True:
        # defensive player is the non-offensive one
        defensive_idx = (offensive_idx + 1) % 2

        defensive_board = game_boards[defensive_idx]
        offensive_player = players[offensive_idx]

        announce_f("new_turn", {"player": offensive_player.name})
        shot_location = offensive_player.shot_f(defensive_board)

        hit_battleship = defensive_board.take_shot(shot_location)
        if hit_battleship is None:
            announce_f("miss", {"player": offensive_player.name})
        else:
            if hit_battleship.is_destroyed():
                announce_f(
                    "battleship_destroyed",
                    {"player": offensive_player.name})
            else:
                announce_f("battleship_hit", {"player": offensive_player.name})

        render_f(defensive_board)

        if defensive_board.is_game_over():
            announce_f("game_over", {"player": offensive_player.name})
            break

        # offensive player becomes the previous defensive player
        offensive_idx = defensive_idx


def display_rules():
    """
    Prints rules of game to screen
    """
    os.system("clear")
    print("""
R U L E S

Guess where the opponents ships are.\n
Give x, y cordinates for the 10X10 board.\n
Game ends when you have guessed where all the ships are.
    """)
    go_back = input("Press any key and enter to go back:\n").lower()
    if go_back:
        os.system("clear")
        return welcome()


def display_winners():
    print("5  R E C E N T  W I N N E R S")
    print()
    winners_list = []
    for winners in COL:
        winners_list.append(winners)
    if len(winners_list) > 5:
        del winners_list[5:]
    for each_winner in winners_list:
        print("????" + each_winner)
    go_back = input("Press any key and enter to go back:\n").lower()
    if go_back:
        os.system("clear")
        return welcome()


def welcome():
    """
    Prints welcome message
    """
    print(r"""
______       _   _   _          _     _
| ___ \     | | | | | |        | |   (_)
| |_/ / __ _| |_| |_| | ___ ___| |__  _ _ __ 
| ___ \/ _` | __| __| |/ _ / __| '_ \| | '_ \
| |_/ | (_| | |_| |_| |  __\__ | | | | | |_) |
\____/ \__,_|\__|\__|_|\___|___|_| |_|_| .__/
                                       | |
                                       |_|
    """)
    print("M A I N  M E N U")
    choice = input("""
Welcome to the game Battleship!\n
Would you like to:\n
1.Play game\n
2.Read rules\n
3.View winners\n
4.Quit\n
Enter 1, 2, 3 or 4:\n""")
    os.system("clear")
    if choice == "1":
        run(announce_en, render)
    elif choice == "2":
        display_rules()
    elif choice == "3":
        display_winners()
    elif choice == "4":
        print("G O O D B Y E ????")
        exit()
    else:
        print("???Incorrect choice. Try again.???")
        print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
        welcome()


if __name__ == "__main__":
    welcome()
