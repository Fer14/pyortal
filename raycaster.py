import pygame
from settings import (
    NUM_RAYS,
    WALL_HEIGHT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    RES,
    FOV,
    degrees_to_radiants,
)
from ray import Ray, normalize_angle
import math
import time


class RayCaster:
    def __init__(self, player, map, options) -> None:
        self.rays = []
        self.player = player
        self.map = map
        self.options = options
        self.portal_image = pygame.image.load("portal1.png")
        self.scaled_portal_image_blue = pygame.transform.scale(
            self.portal_image,
            (self.portal_image.get_width() // 8, self.portal_image.get_height() // 8),
        )
        self.portal_image_2 = pygame.image.load("portal2.png")
        self.scaled_portal_image_orange = pygame.transform.scale(
            self.portal_image_2,
            (
                self.portal_image_2.get_width() // 8,
                self.portal_image_2.get_height() // 8,
            ),
        )

    def cast_rays(self):
        self.rays = []

        ray_angle = (
            self.player.rotation_angle - degrees_to_radiants(self.options.fov) / 2
        )
        for i in range(NUM_RAYS):
            ray = Ray(ray_angle, self.player, self.map)
            ray.cast()
            self.rays.append(ray)
            ray_angle += degrees_to_radiants(self.options.fov) / NUM_RAYS

        ray = Ray(self.player.rotation_angle, self.player, self.map)
        ray.cast()
        self.rays.append(ray)

        # for ray in self.rays:
        #     if math.isclose(
        #         ray.ray_angle, normalize_angle(self.player.rotation_angle), abs_tol=1e-6
        #     ):
        #         print(time.time(), "si")
        #         print(ray.ray_angle, self.player.rotation_angle)

    def handle_shooting(self, ray):
        if self.player.shoot_blue:
            self.map.blue_hit = ray.hit
            self.map.set_blue(ray.wall_hit_x, ray.wall_hit_y)

        if self.player.shoot_orange:
            self.map.orange_hit = ray.hit
            self.map.set_orange(ray.wall_hit_x, ray.wall_hit_y)
            self.map.orange_angle = self.player.rotation_angle

    def render3d(
        self,
        screen,
    ):
        i = 0

        blue_rays = []
        orange_rays = []

        for ray in self.rays:
            # ray.render(screen)

            line_height = (WALL_HEIGHT / ray.distance) * (
                (WINDOW_WIDTH / 2) / math.tan(degrees_to_radiants(self.options.fov) / 2)
            )

            draw_begin = self.player.center - (line_height / 2)
            draw_end = line_height

            ray.draw = (i * RES, draw_begin, RES, draw_end)

            is_aligned = math.isclose(
                ray.ray_angle, normalize_angle(self.player.rotation_angle), abs_tol=1e-6
            )

            if is_aligned:
                self.handle_shooting(ray)

            pygame.draw.rect(
                screen,
                ray.color,
                ray.draw,
            )

            if ray.color == (1, 186, 239) and not is_aligned:
                blue_rays.append(ray)

            if ray.color == (255, 140, 0) and not is_aligned:
                orange_rays.append(ray)

            i += 1

        if self.options.portals:
            if blue_rays:
                self.render_portal(screen, blue_rays)
            if orange_rays:
                self.render_portal(screen, orange_rays, blue=False)

    def render_portal(self, screen, rays, blue=True):

        min_left = min(r.draw[0] for r in rays)
        min_top = min(r.draw[1] for r in rays)
        max_left = max(r.draw[0] + r.draw[2] for r in rays)
        max_top = max(r.draw[1] + r.draw[3] for r in rays)

        # Ensure the bounding box has positive dimensions
        box_width = max(0, max_left - min_left)
        box_height = max(0, max_top - min_top)

        # pygame.draw.rect(
        #     screen, (255, 0, 0), (min_left, min_top, box_width, box_height), 2
        # )

        total_distance = sum(ray.distance for ray in rays)
        average_distance = total_distance / len(rays)

        # Calculate the width and height of the portal image
        scaled_portal = (
            self.scaled_portal_image_blue if blue else self.scaled_portal_image_orange
        )
        portal_width, portal_height = scaled_portal.get_size()

        scale_factor = max(
            0.1, min(2.0, 1 / (average_distance / 100))
        )  # Adjust scale factor as needed
        scaled_portal_width = int(portal_width * scale_factor)
        scaled_portal_height = int(portal_height * scale_factor)

        # Calculate the position to center the portal image inside the bounding box
        center_x = min_left + (box_width - scaled_portal_width) // 2
        center_y = min_top + (box_height - scaled_portal_height) // 2

        # Blit the pre-scaled portal image onto the screen at the calculated position
        screen.blit(
            pygame.transform.scale(
                scaled_portal,
                (scaled_portal_width, scaled_portal_height),
            ),
            (center_x, center_y),
        )

    def render2d(self, screen):
        for ray in self.rays:
            ray.render(screen)
            if math.isclose(
                ray.ray_angle, normalize_angle(self.player.rotation_angle), abs_tol=1e-6
            ):
                pygame.draw.line(
                    screen,
                    (1, 186, 239),
                    (ray.player.x, ray.player.y),
                    (
                        ray.wall_hit_x,
                        ray.wall_hit_y,
                    ),
                )

                if self.player.shoot_blue:
                    self.map.blue_hit = ray.hit
                    self.map.set_blue(ray.wall_hit_x, ray.wall_hit_y)

                if self.player.shoot_orange:
                    self.map.orange_hit = ray.hit
                    self.map.set_orange(ray.wall_hit_x, ray.wall_hit_y)
                    self.map.orange_angle = self.player.rotation_angle
