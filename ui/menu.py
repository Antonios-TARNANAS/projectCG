import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


def draw_text(surface, text, size, x, y, color=(255, 255, 255), center=True):
    font = pygame.font.SysFont(None, size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)


def menu_screen(screen):
    """Returns a dict: { players: 1|2, mode: 'freeride'|'fixed', laps: int }"""
    clock = pygame.time.Clock()

    players = _pick_option(screen, clock,
        title="RACING GAME",
        prompt="Number of players",
        options=[("1 Player", 1), ("2 Players", 2)]
    )

    mode = _pick_option(screen, clock,
        title="RACING GAME",
        prompt="Race mode",
        options=[("Freeride", "freeride"), ("Fixed Laps", "fixed")]
    )

    laps = 3
    if mode == "fixed":
        laps = _pick_option(screen, clock,
            title="RACING GAME",
            prompt="Number of laps",
            options=[("1 Lap", 1), ("3 Laps", 3), ("5 Laps", 5), ("10 Laps", 10)]
        )

    return {"players": players, "mode": mode, "laps": laps}


def winner_screen(screen, winner_label):
    """Blocks until player presses ENTER."""
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        screen.fill((0, 0, 40))
        draw_text(screen, f"{winner_label} WINS!", 80, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        draw_text(screen, "Press ENTER to return to menu", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        pygame.display.flip()
        clock.tick(30)


def _pick_option(screen, clock, title, prompt, options):
    """Generic option picker. Returns the value of the selected option."""
    selected = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return options[selected][1]

        screen.fill((0, 0, 40))
        draw_text(screen, title, 72, SCREEN_WIDTH // 2, 120)
        draw_text(screen, prompt, 40, SCREEN_WIDTH // 2, 230)

        for i, (label, _) in enumerate(options):
            color = (255, 220, 0) if i == selected else (180, 180, 180)
            draw_text(screen, label, 48, SCREEN_WIDTH // 2, 320 + i * 70, color=color)

        draw_text(screen, "UP/DOWN to select, ENTER to confirm", 28,
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, color=(120, 120, 120))

        pygame.display.flip()
        clock.tick(30)