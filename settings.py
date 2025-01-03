import math


def degrees_to_radiants(degrees):
    return degrees * (math.pi / 180)


def radiants_to_degrees(radiants):
    return round(radiants * (180 / math.pi))


TILE_SIZE = 32

ROWS = 10
COLS = 15

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

FOV = degrees_to_radiants(60)

RES = 4
NUM_RAYS = WINDOW_WIDTH // RES

WALL_HEIGHT = 32
