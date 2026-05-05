from entities.car import Car
from entities.lap_tracker import LapTracker
import pygame

KEYBINDS = {
    "zqsd": {
        "up": pygame.K_z,
        "down": pygame.K_s,
        "left": pygame.K_q,
        "right": pygame.K_d
    },
    "wasd": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d
    }
}


class Player:
    def __init__(self, player_number, start_pos, start_angle,
                 finish_line, total_laps, car_stats, layout="zqsd"):

        color_key = "color_p1" if player_number == 1 else "color_p2"
        color = car_stats[color_key]

        if player_number == 1:
            controls = KEYBINDS[layout]
        else:
            controls = {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT
            }

        self.car = Car(
            x=start_pos[0], y=start_pos[1],
            color=color,
            controls=controls,
            stats=car_stats
        )
        self.car.angle = start_angle
        self.label = f"Player {player_number}"
        self.lap_tracker = LapTracker(finish_line, total_laps)
        self.camera_x = 0
        self.camera_y = 0

    def update(self, keys, outer_polygon, inner_polygon, view_width, view_height):
        self.car.handle_input(keys)
        self.car.update(outer_polygon, inner_polygon)
        self.lap_tracker.update(self.car.x, self.car.y, self.car.prev_x, self.car.prev_y)
        self.camera_x = self.car.x - view_width // 2
        self.camera_y = self.car.y - view_height // 2

    def draw(self, surface, camera_x, camera_y):
        self.car.draw(surface, camera_x, camera_y)