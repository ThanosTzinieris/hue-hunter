from random import randint


class Color():

    def __init__(self, R, G, B):
        self.red = R
        self.green = G
        self.blue = B

    def print(self):
        print("R =", self.red, "G =", self.green, "B =", self.blue)

# Randomly produce one color
color1 = Color(randint(0, 255), randint(0, 255), randint(0, 255))
color1.print()


def calculate(sr, sg, sb, tr, tg, tb):
    difr = abs(sr - tr) / 255
    difg = abs(sg - tg) / 255
    difb = abs(sb - tb) / 255

    diff_ratio = (difr + difg + difb) / 3  # Average the differences
    diffin = int(100 * (1 - diff_ratio))  # Convert to percentage

    return max(0, diffin)