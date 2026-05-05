from entities.car import Car
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
    def __init__(self, player_number, start_pos, start_angle, layout="zqsd"):
        if player_number == 1:
            controls = KEYBINDS[layout]
            self.car = Car(x=start_pos[0], y=start_pos[1], color=(255, 50, 50), controls=controls)

        elif player_number == 2:
            controls = {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT
            }
            self.car = Car(x=start_pos[0], y=start_pos[1], color=(50, 200, 255), controls=controls)

        self.car.angle = start_angle

        # Camera tracks the car — top left corner of what we see
        self.camera_x = 0
        self.camera_y = 0

    def update(self, keys, outer_polygon, inner_polygon, view_width, view_height):
        self.car.handle_input(keys)
        self.car.update(outer_polygon, inner_polygon)

        # Camera centers on the car
        self.camera_x = self.car.x - view_width // 2
        self.camera_y = self.car.y - view_height // 2

    def draw(self, surface, camera_x, camera_y):
        self.car.draw(surface, camera_x, camera_y)