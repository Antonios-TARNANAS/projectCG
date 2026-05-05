import pygame

class Car:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 35
        self.color = color
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.2
        self.friction = 0.05        # slows car down when no key pressed
        self.angle = 0              # degrees, 0 = facing up
        self.turn_speed = 3

        # controls is a dict: {"up", "down", "left", "right"}
        # this way each player just passes different keys
        self.controls = controls

    def handle_input(self, keys):
        if keys[self.controls["up"]]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[self.controls["down"]]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
        else:
            # friction: bleed speed toward 0
            if self.speed > 0:
                self.speed = max(self.speed - self.friction, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.friction, 0)

        if self.speed != 0:
            if keys[self.controls["left"]]:
                self.angle -= self.turn_speed
            if keys[self.controls["right"]]:
                self.angle += self.turn_speed

    def update(self):
        import math
        rad = math.radians(self.angle)
        self.x += self.speed * math.sin(rad)
        self.y -= self.speed * math.cos(rad)

    def draw(self, screen):
        import math, pygame

        # Build a rectangle and rotate it around its center
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (0, 0, self.width, self.height))

        rotated = pygame.transform.rotate(surface, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)