# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
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


if __name__ == "__main__":
    shots = []
    while True:
        inp = input("Where do you want to shoot?\n")
        x, y = inp.split(",")
        x = int(x)
        y = int(y)
        shots.append((x, y))
        render(10, 10, shots)
