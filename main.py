import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, COLOR_BG
from entities.player import Player
from data.maps_registry import MAPS

def parse_args():
    layout = "zqsd"
    for arg in sys.argv[1:]:
        if arg in ("-zqsd", "-wasd"):
            layout = arg[1:]
    return layout

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Load first map
    current_map = MAPS[0]()
    outer = current_map.get_outer_polygon()
    inner = current_map.get_inner_polygon()

    layout = parse_args()

    # Each player starts at the map's defined start positions
    player1 = Player(1, current_map.start_positions[0], current_map.start_angle, layout=layout)
    player2 = Player(2, current_map.start_positions[1], current_map.start_angle)

    # Split screen: each half is SCREEN_WIDTH // 2 wide
    half_w = SCREEN_WIDTH // 2
    view_h = SCREEN_HEIGHT

    # Two surfaces, one per player view
    surface_p1 = pygame.Surface((half_w, view_h))
    surface_p2 = pygame.Surface((half_w, view_h))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Update both players
        player1.update(keys, outer, inner, half_w, view_h)
        player2.update(keys, outer, inner, half_w, view_h)

        # Draw Player 1 view
        surface_p1.fill((30, 120, 30))  # grass background
        current_map.draw(surface_p1, player1.camera_x, player1.camera_y)
        player1.draw(surface_p1, player1.camera_x, player1.camera_y)
        player2.draw(surface_p1, player1.camera_x, player1.camera_y)

        # Draw Player 2 view
        surface_p2.fill((30, 120, 30))  # grass background
        current_map.draw(surface_p2, player2.camera_x, player2.camera_y)
        player1.draw(surface_p2, player2.camera_x, player2.camera_y)
        player2.draw(surface_p2, player2.camera_x, player2.camera_y)

        # Blit both views onto main screen
        screen.blit(surface_p1, (0, 0))
        screen.blit(surface_p2, (half_w, 0))

        # Divider line between the two views
        pygame.draw.line(screen, (255, 255, 255), (half_w, 0), (half_w, view_h), 2)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()