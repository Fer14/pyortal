## create a class that is a menu where you can control things like wind or fov
## this class will be used in the main menu to change the options of the game

import pygame
from settings import *
from pygame import mixer
import sys
import os


class Options:
    def __init__(self) -> None:

        self.show = False

        self.fov = 60
        self.portals = True

        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font("Gliker-Bold.ttf", 30)
        self.font = pygame.font.Font("Gliker-Bold.ttf", 20)
        self.selected = 0

        self.options = [
            f"FOV: (- {self.fov} >",
            f"Portal Graphics: < {'On' if self.portals else 'Off'} >",
        ]

        self.colors = [(255, 255, 255)] * len(self.options)

    def update_options(self):
        # Update the options list with the current values of fov and music
        self.options[0] = f"FOV: (- {self.fov} -)"
        self.options[1] = f"Portal Graphics: (- {'On' if self.portals else 'Off'} -)"

    def render(self, screen):
        screen.fill((0, 0, 0))
        title = self.font_title.render("OPTIONS", True, (255, 255, 255))
        screen.blit(
            title,
            (WINDOW_WIDTH // 2 - title.get_width() // 2, 10),
        )

        line_y = 10 + title.get_height() + 5  # Position the line below the title
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (WINDOW_WIDTH // 2 - title.get_width() // 2, line_y),
            (WINDOW_WIDTH // 2 - title.get_width() // 2 + title.get_width(), line_y),
            2,
        )

        for i, option in enumerate(self.options):
            color = (255, 140, 0) if i == self.selected else (255, 255, 255)

            text = self.font.render(option, True, color)
            screen.blit(
                text,
                (WINDOW_WIDTH // 2 - text.get_width() // 2, 100 + i * 50),
            )

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    if self.selected == 0:  # Adjust FOV
                        self.fov = max(30, self.fov - 5)  # Minimum FOV is 30
                    elif self.selected == 1:  # Toggle Music
                        self.portals = not self.portals
                elif event.key == pygame.K_RIGHT:
                    if self.selected == 0:  # Adjust FOV
                        self.fov = min(120, self.fov + 5)  # Maximum FOV is 120
                    elif self.selected == 1:  # Toggle Music
                        self.portals = not self.portals
                if event.key == pygame.K_q:
                    self.show = not self.show
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        self.update_options()

    def handle(self, screen):

        if self.show:
            self.handle_input()
            self.render(screen)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.show = not self.show
