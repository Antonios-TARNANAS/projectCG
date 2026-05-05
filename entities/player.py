# Player is a thin wrapper that links a car to a player number.
# Later it will also track laps, score, selected car skin, etc.

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
    def __init__(self, player_number, layout="zqsd"):
        if player_number == 1:
            controls = KEYBINDS[layout]
            self.car = Car(x=350, y=300, color=(255, 50, 50), controls=controls)

        elif player_number == 2:
            controls = {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT
            }
            self.car = Car(x=450, y=300, color=(50, 255, 50), controls=controls)

    def update(self, keys):
        self.car.handle_input(keys)
        self.car.update()

    def draw(self, screen):
        self.car.draw(screen)