from canvas import Canvas
from tile import Tileset
import random

WIDTH = 2
HEIGHT = 2

ts = Tileset('tiles/')

canvas = Canvas(ts, WIDTH, HEIGHT)

x = random.randint(0, WIDTH-1)
y = random.randint(0, HEIGHT-1)

print(x, y)

canvas.collapse_cell(x, y)

while not canvas.is_finished():
    x, y = canvas.find_candidate()
    canvas.collapse_cell(x, y)