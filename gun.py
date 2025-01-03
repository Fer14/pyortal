import pygame
from settings import *


class Gun:
    def __init__(self) -> None:

        self.image = pygame.image.load("gun.png")

        self.pointer = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def render(self, screen):
        screen.blit(self.image, (0, 0, 0, 0))
        pygame.draw.circle(screen, (0, 0, 0), self.pointer, 2)
