import pygame
from settings import *


class Player:
    def __init__(self, gun) -> None:
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.z = 0
        self.radius = 3
        self.rotation_angle = degrees_to_radiants(0)
        self.turn_direction = 0
        self.walk_direction = 0
        self.move_speed = 2.5
        self.ration_speed = degrees_to_radiants(1)
        self.jump_height = WALL_HEIGHT * 2
        self.max_jump_timer = 20
        self.jump_timer = self.max_jump_timer
        self.set_jump_timer = False
        self.shoot_blue = False
        self.shoot_orange = False

    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)

        pygame.draw.line(
            screen,
            (0, 255, 0),
            (self.x, self.y),
            (
                self.x + math.cos(self.rotation_angle) * 50,
                self.y + math.sin(self.rotation_angle) * 50,
            ),
        )

    def reset_jump(self):
        self.z = 0
        self.jump_timer = self.max_jump_timer
        self.set_jump_timer = False

    def reset_gun(self):
        self.shoot_blue = False
        self.shoot_orange = False

    def update(self, map):
        self.reset_gun()

        if self.set_jump_timer:
            self.jump_timer -= 1
            self.z = self.jump_timer / self.max_jump_timer
            if self.jump_timer == 0:
                self.reset_jump()

        keys = pygame.key.get_pressed()

        self.turn_direction = 0
        self.walk_direction = 0

        if keys[pygame.K_RIGHT]:
            self.turn_direction = 1
        if keys[pygame.K_LEFT]:
            self.turn_direction = -1
        if keys[pygame.K_UP]:
            self.walk_direction = 1
        if keys[pygame.K_DOWN]:
            self.walk_direction = -1
        if keys[pygame.K_SPACE]:
            if not self.set_jump_timer:
                self.z = 1
                self.set_jump_timer = True
        if keys[pygame.K_a]:
            self.shoot_blue = True
        if keys[pygame.K_s]:
            self.shoot_orange = True

        move_step = self.walk_direction * self.move_speed

        self.rotation_angle += self.turn_direction * self.ration_speed

        new_x = self.x + math.cos(self.rotation_angle) * move_step
        new_y = self.y + math.sin(self.rotation_angle) * move_step

        if map.blue_door == map.xy_to_coords(new_x, new_y) and map.orange_door:
            self.rotation_angle = map.orange_angle + math.pi
            self.x, self.y = map.coords_to_xy(map.orange_door, self.rotation_angle)

        elif not map.is_wall(
            new_x,
            new_y,
        ):
            self.x = new_x
            self.y = new_y

        if self.z == 0:
            self.center = WINDOW_HEIGHT / 2
        else:
            self.center = (WINDOW_HEIGHT / 2) + (self.jump_height * self.z)
