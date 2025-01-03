import pygame
from settings import *
from map import Map
from player import Player
from raycaster import RayCaster
from options import Options
from gun import Gun
import typer


# Initialize Typer app
app = typer.Typer()


@app.command()
def run_game(mode: int = typer.Option(3, help="Game mode: 2 for 2D, 3 for 3D")):
    """
    Run the game with the specified mode.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    menu = Options()
    gun = Gun()
    map = Map()
    player = Player(gun)
    raycaster = RayCaster(player, map, menu)
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player.update(map)
        raycaster.cast_rays()

        if mode == 3:
            screen.fill((13, 27, 30), (0, 0, WINDOW_WIDTH, player.center))
            screen.fill(
                (235, 242, 250), (0, player.center, WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            raycaster.render3d(screen)
            gun.render(screen)
        elif mode == 2:
            screen.fill((0, 0, 0))
            map.render(screen)
            raycaster.render2d(screen)
            player.render(screen)

        menu.handle(screen)
        pygame.display.update()


if __name__ == "__main__":
    app()
