import pygame
from settings import *
import copy


class Map:
    def __init__(self) -> None:
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.original_grid = copy.deepcopy(self.grid)

        self.blue_door = None
        self.old_blue_value = None

        self.orange_door = None
        self.old_orange_value = None

    def reset_grid(self):
        self.grid = copy.deepcopy(self.original_grid)

    def render(self, screen):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                tile_x = j * TILE_SIZE
                tile_y = i * TILE_SIZE
                color = (255, 255, 255)
                if self.grid[i][j] == 1:
                    color = (40, 40, 40)
                elif (i, j) == self.blue_door:
                    color = (1, 186, 239)
                elif (i, j) == self.orange_door:
                    color = (255, 140, 0)
                pygame.draw.rect(
                    screen, color, (tile_x, tile_y, TILE_SIZE - 1, TILE_SIZE - 1)
                )

    def is_wall(self, x, y):
        return self.grid[int(y // TILE_SIZE)][int(x // TILE_SIZE)]

    def set_blue(self, x, y):
        if self.orange_door == (
            int(y // TILE_SIZE),
            int(x // TILE_SIZE),
        ):
            return

        if self.old_blue_value and self.blue_door:
            self.grid[self.blue_door[0]][self.blue_door[1]] = self.old_blue_value

        self.old_blue_value = self.grid[int(y // TILE_SIZE)][int(x // TILE_SIZE)]
        self.grid[int(y // TILE_SIZE)][int(x // TILE_SIZE)] = 2
        self.blue_door = (int(y // TILE_SIZE), int(x // TILE_SIZE))

    def set_orange(self, x, y):
        if not self.blue_door or self.blue_door == (
            int(y // TILE_SIZE),
            int(x // TILE_SIZE),
        ):
            return

        if self.old_orange_value and self.orange_door:
            self.grid[self.orange_door[0]][self.orange_door[1]] = self.old_orange_value

        self.old_orange_value = self.grid[int(y // TILE_SIZE)][int(x // TILE_SIZE)]
        self.grid[int(y // TILE_SIZE)][int(x // TILE_SIZE)] = 3
        self.orange_door = (int(y // TILE_SIZE), int(x // TILE_SIZE))

    def xy_to_coords(self, x, y):
        return (int(y // TILE_SIZE), int(x // TILE_SIZE))

    def coords_to_xy(self, coords, angle):
        x = coords[1] * TILE_SIZE + TILE_SIZE // 2
        y = coords[0] * TILE_SIZE + TILE_SIZE // 2

        if abs(math.cos(angle)) > abs(math.sin(angle)):
            distance = (TILE_SIZE / 2) / abs(math.cos(angle))
            offset_x = 1 if math.cos(angle) > 0 else -1
            offset_y = 0
        else:
            distance = (TILE_SIZE / 2) / abs(math.sin(angle))
            offset_x = 0
            offset_y = 1 if math.sin(angle) > 0 else -1

        dx = distance * math.cos(angle) + offset_x
        dy = distance * math.sin(angle) + offset_y

        return (x + dx, y + dy)
