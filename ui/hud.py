import pygame

def draw_hud(surface, player, mode, x=10, y=10):
    font = pygame.font.SysFont(None, 32)
    tracker = player.lap_tracker
    total = tracker.total_laps

    if mode == "freeride":
        lap_text = f"Lap: {tracker.laps}"
    else:
        # Cap display at total_laps so it never shows 4/3 etc.
        displayed_laps = min(tracker.laps, total)
        lap_text = f"Lap: {displayed_laps} / {total}"

    t = tracker.current_lap_time()
    time_text = f"Time: {t:.2f}s"

    last = tracker.last_lap_time()
    last_text = f"Last: {last:.2f}s" if last else "Last: --"

    for i, text in enumerate([lap_text, time_text, last_text]):
        rendered = font.render(text, True, (255, 255, 255))
        surface.blit(rendered, (x, y + i * 30))