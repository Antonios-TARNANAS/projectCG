import pygame


def draw_hud(surface, player, mode, x=10, y=10):
    font = pygame.font.SysFont(None, 32)
    tracker = player.lap_tracker
    total = tracker.total_laps

    if mode == "freeride":
        lap_text = f"Lap: {tracker.laps}"
    else:
        displayed_laps = min(tracker.laps, total)
        lap_text = f"Lap: {displayed_laps} / {total}"

    t = tracker.current_lap_time()
    time_text = f"Time: {t:.2f}s"

    last = tracker.last_lap_time()
    last_text = f"Last: {last:.2f}s" if last else "Last: --"

    lines = [lap_text, time_text, None, last_text]

    # Best lap time — only shown in freeride
    if mode == "freeride":
        best = tracker.best_lap_time()
        best_text = f"Best: {best:.2f}s" if best else "Best: --"
        lines[2] = best_text

    for i, text in enumerate(lines):
        rendered = font.render(text, True, (255, 255, 255))
        surface.blit(rendered, (x, y + i * 30))