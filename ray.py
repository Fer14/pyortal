import math, pygame
from settings import *


def normalize_angle(angle):
    angle = angle % (2 * math.pi)
    if angle <= 0:
        angle = (2 * math.pi) + angle
    return angle


def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


class Ray:
    def __init__(self, angle, player, map) -> None:
        self.ray_angle = normalize_angle(angle)
        self.player = player
        self.map = map

        self.is_facing_down = self.ray_angle > 0 and self.ray_angle < math.pi
        self.is_facing_up = not self.is_facing_down

        self.is_facing_right = (
            self.ray_angle < math.pi / 2 or self.ray_angle > math.pi * 1.5
        )
        self.is_facing_left = not self.is_facing_right

        self.wall_hit_x = 0
        self.wall_hit_y = 0

        self.distance = 0
        self.color = 255
        self.draw = None

        self.hit = None

    def cast(self):
        # horizontal check
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0

        first_intersection_x = None
        first_intersection_y = None

        if self.is_facing_up:
            first_intersection_y = ((self.player.y) // TILE_SIZE) * TILE_SIZE - 0.01
        elif self.is_facing_down:
            first_intersection_y = (
                (self.player.y // TILE_SIZE) * TILE_SIZE
            ) + TILE_SIZE

        first_intersection_x = self.player.x + (
            first_intersection_y - self.player.y
        ) / math.tan(self.ray_angle)

        next_horizontal_x = first_intersection_x
        next_horizontal_y = first_intersection_y

        xa = 0
        ya = 0

        if self.is_facing_up:
            ya = -TILE_SIZE
        elif self.is_facing_down:
            ya = TILE_SIZE

        xa = ya / math.tan(self.ray_angle)

        while (
            next_horizontal_x >= 0
            and next_horizontal_x <= WINDOW_WIDTH
            and next_horizontal_y >= 0
            and next_horizontal_y <= WINDOW_HEIGHT
        ):
            if self.map.is_wall(next_horizontal_x, next_horizontal_y):
                horizontal_hit_x = next_horizontal_x
                horizontal_hit_y = next_horizontal_y
                found_horizontal_wall = True
                break
            else:
                next_horizontal_x += xa
                next_horizontal_y += ya

        # vertical check

        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0

        if self.is_facing_right:
            first_intersection_x = (
                (self.player.x // TILE_SIZE) * TILE_SIZE
            ) + TILE_SIZE
        elif self.is_facing_left:
            first_intersection_x = ((self.player.x // TILE_SIZE) * TILE_SIZE) - 0.01

        first_intersection_y = self.player.y + (
            first_intersection_x - self.player.x
        ) * math.tan(self.ray_angle)

        next_vertical_x = first_intersection_x
        next_vertical_y = first_intersection_y

        if self.is_facing_right:
            xa = TILE_SIZE
        elif self.is_facing_left:
            xa = -TILE_SIZE

        ya = xa * math.tan(self.ray_angle)

        while (
            next_vertical_x >= 0
            and next_vertical_x <= WINDOW_WIDTH
            and next_vertical_y >= 0
            and next_vertical_y <= WINDOW_HEIGHT
        ):
            if self.map.is_wall(next_vertical_x, next_vertical_y):
                vertical_hit_x = next_vertical_x
                vertical_hit_y = next_vertical_y
                found_vertical_wall = True
                break
            else:
                next_vertical_x += xa
                next_vertical_y += ya

        # DISTANCE CALCULATION

        if found_horizontal_wall:
            horizontal_distance = math.dist(
                (self.player.x, self.player.y), (horizontal_hit_x, horizontal_hit_y)
            )
        else:
            horizontal_distance = 99999999
        if found_vertical_wall:
            vertical_distance = math.dist(
                (self.player.x, self.player.y), (vertical_hit_x, vertical_hit_y)
            )
        else:
            vertical_distance = 99999999

        if horizontal_distance < vertical_distance:
            self.wall_hit_x = horizontal_hit_x
            self.wall_hit_y = horizontal_hit_y
            self.distance = horizontal_distance
            self.color = 160
            self.hit = "horizontal"
        else:
            self.wall_hit_x = vertical_hit_x
            self.wall_hit_y = vertical_hit_y
            self.distance = vertical_distance
            self.color = 255
            self.hit = "vertical"

        self.distance *= math.cos(self.player.rotation_angle - self.ray_angle)

        self.color *= 60 / self.distance
        self.color = min(255, self.color)
        self.color = (self.color, self.color, self.color)

        if (
            self.map.is_wall(self.wall_hit_x, self.wall_hit_y) == 2
            and self.hit == self.map.blue_hit
        ):
            self.color = (1, 186, 239)

        if (
            self.map.is_wall(self.wall_hit_x, self.wall_hit_y) == 3
            and self.hit == self.map.orange_hit
        ):
            self.color = (255, 140, 0)

    def render(self, screen):
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (self.player.x, self.player.y),
            (
                self.wall_hit_x,
                self.wall_hit_y,
            ),
        )
