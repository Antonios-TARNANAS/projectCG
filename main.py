import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from entities.player import Player
from data.maps_registry import MAPS
from ui.menu import menu_screen, winner_screen
from ui.hud import draw_hud


def parse_args():
    layout = "zqsd"
    for arg in sys.argv[1:]:
        if arg in ("-zqsd", "-wasd"):
            layout = arg[1:]
    return layout


def run_race(screen, config, layout):
    clock = pygame.time.Clock()

    current_map = MAPS[0]()
    outer = current_map.get_outer_polygon()
    inner = current_map.get_inner_polygon()
    finish_line = current_map.get_finish_line()

    num_players = config["players"]
    mode = config["mode"]
    total_laps = config["laps"] if mode == "fixed" else None

    player1 = Player(1, current_map.start_positions[0], current_map.start_angle,
                     finish_line, total_laps, layout=layout)

    player2 = None
    if num_players == 2:
        player2 = Player(2, current_map.start_positions[1], current_map.start_angle,
                         finish_line, total_laps)

    # Split screen or full screen depending on player count
    if num_players == 2:
        view_w = SCREEN_WIDTH // 2
    else:
        view_w = SCREEN_WIDTH
    view_h = SCREEN_HEIGHT

    surface_p1 = pygame.Surface((view_w, view_h))
    surface_p2 = pygame.Surface((view_w, view_h)) if num_players == 2 else None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # back to menu

        keys = pygame.key.get_pressed()

        player1.update(keys, outer, inner, view_w, view_h)
        if player2:
            player2.update(keys, outer, inner, view_w, view_h)

        # Check for winner
        if mode == "fixed":
            if player1.lap_tracker.finished:
                winner_screen(screen, player1.label)
                return
            if player2 and player2.lap_tracker.finished:
                winner_screen(screen, player2.label)
                return

        # Draw P1 view
        surface_p1.fill((30, 120, 30))
        current_map.draw(surface_p1, player1.camera_x, player1.camera_y)
        player1.draw(surface_p1, player1.camera_x, player1.camera_y)
        if player2:
            player2.draw(surface_p1, player1.camera_x, player1.camera_y)
        draw_hud(surface_p1, player1, mode)
        screen.blit(surface_p1, (0, 0))

        # Draw P2 view
        if player2 and surface_p2:
            surface_p2.fill((30, 120, 30))
            current_map.draw(surface_p2, player2.camera_x, player2.camera_y)
            player1.draw(surface_p2, player2.camera_x, player2.camera_y)
            player2.draw(surface_p2, player2.camera_x, player2.camera_y)
            draw_hud(surface_p2, player2, mode)
            screen.blit(surface_p2, (view_w, 0))
            pygame.draw.line(screen, (255, 255, 255),
                             (view_w, 0), (view_w, view_h), 2)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    layout = parse_args()

    while True:
        config = menu_screen(screen)
        run_race(screen, config, layout)


if __name__ == "__main__":
    main()