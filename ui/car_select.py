import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.cars import CARS


def car_select_screen(screen, num_players):
    """
    Returns a list of selected car dicts.
    P1 picks first, then P2 if num_players == 2.
    """
    selected_cars = []
    for player_num in range(1, num_players + 1):
        car = _pick_car(screen, player_num, selected_cars)
        selected_cars.append(car)
    return selected_cars


def _pick_car(screen, player_num, already_picked):
    clock = pygame.time.Clock()
    selected = 0
    font_title = pygame.font.SysFont(None, 64)
    font_name = pygame.font.SysFont(None, 48)
    font_desc = pygame.font.SysFont(None, 30)
    font_stats = pygame.font.SysFont(None, 28)
    font_hint = pygame.font.SysFont(None, 26)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                import sys
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(CARS)
                if event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(CARS)
                if event.key == pygame.K_RETURN:
                    return CARS[selected]

        screen.fill((0, 0, 40))

        # Title
        title = font_title.render(f"Player {player_num} — Pick Your Car", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))

        car = CARS[selected]

        # Car rectangle preview
        color_key = "color_p1" if player_num == 1 else "color_p2"
        preview_color = car[color_key]
        preview_rect = pygame.Rect(0, 0, 60, 100)
        preview_rect.center = (SCREEN_WIDTH // 2, 220)
        pygame.draw.rect(screen, preview_color, preview_rect)

        # Car name
        name_surf = font_name.render(car["name"], True, (255, 220, 0))
        screen.blit(name_surf, name_surf.get_rect(center=(SCREEN_WIDTH // 2, 300)))

        # Description
        desc_surf = font_desc.render(car["description"], True, (180, 180, 180))
        screen.blit(desc_surf, desc_surf.get_rect(center=(SCREEN_WIDTH // 2, 345)))

        # Stats bars
        stats = [
            ("Speed",    car["max_speed"],    20),
            ("Accel",    car["acceleration"], 0.6),
            ("Grip",     car["grip"],         1.0),
            ("Friction", car["friction"],     1.0),
        ]

        bar_x = SCREEN_WIDTH // 2 - 150
        bar_y = 390
        for label, value, max_val in stats:
            ratio = min(value / max_val, 1.0)
            label_surf = font_stats.render(label, True, (200, 200, 200))
            screen.blit(label_surf, (bar_x, bar_y))
            pygame.draw.rect(screen, (60, 60, 60), (bar_x + 90, bar_y + 4, 200, 16))
            pygame.draw.rect(screen, (50, 200, 100), (bar_x + 90, bar_y + 4, int(200 * ratio), 16))
            bar_y += 34

        # Arrow indicators
        if selected > 0:
            pygame.draw.polygon(screen, (255,255,255), [
                (SCREEN_WIDTH//2 - 220, 220),
                (SCREEN_WIDTH//2 - 190, 205),
                (SCREEN_WIDTH//2 - 190, 235),
            ])
        if selected < len(CARS) - 1:
            pygame.draw.polygon(screen, (255,255,255), [
                (SCREEN_WIDTH//2 + 220, 220),
                (SCREEN_WIDTH//2 + 190, 205),
                (SCREEN_WIDTH//2 + 190, 235),
            ])

        # Already picked indicator
        if already_picked:
            hint = font_hint.render(
                f"P1 chose: {already_picked[0]['name']}", True, (150, 150, 150))
            screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)))

        hint_surf = font_hint.render(
            "LEFT/RIGHT to browse   ENTER to confirm", True, (100, 100, 100))
        screen.blit(hint_surf, hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)))

        pygame.display.flip()
        clock.tick(30)