import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, COLOR_BG
from entities.player import Player



def parse_args():
    layout = "zqsd"  # default
    for arg in sys.argv[1:]:
        if arg in ("-zqsd", "-wasd"):
            layout = arg[1:]  # strip the "-"
    return layout


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Create both players
    layout = parse_args()
    player1 = Player(1, layout=layout)
    player2 = Player(2)

    while True:
        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Update ---
        keys = pygame.key.get_pressed()
        player1.update(keys)
        player2.update(keys)

        # --- Draw ---
        screen.fill(COLOR_BG)
        player1.draw(screen)
        player2.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()