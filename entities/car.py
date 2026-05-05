import pygame
import math

def point_in_polygon(x, y, polygon):
    """Ray casting algorithm — returns True if point is inside polygon."""
    n = len(polygon)
    inside = False
    px, py = x, y
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

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
        self.friction = 0.05
        self.angle = 270
        self.turn_speed = 3

        self.controls = controls

        # Store previous position to push back on collision
        self.prev_x = x
        self.prev_y = y

    def handle_input(self, keys):
        if keys[self.controls["up"]]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[self.controls["down"]]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
        else:
            if self.speed > 0:
                self.speed = max(self.speed - self.friction, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.friction, 0)

        if self.speed != 0:
            if keys[self.controls["left"]]:
                self.angle -= self.turn_speed
            if keys[self.controls["right"]]:
                self.angle += self.turn_speed

    def update(self, outer_polygon, inner_polygon):
        self.prev_x = self.x
        self.prev_y = self.y

        rad = math.radians(self.angle)
        self.x += self.speed * math.sin(rad)
        self.y -= self.speed * math.cos(rad)

        # Collision: must be inside outer and outside inner
        in_outer = point_in_polygon(self.x, self.y, outer_polygon)
        in_inner = point_in_polygon(self.x, self.y, inner_polygon)

        if not in_outer or in_inner:
            # Push back to previous position and kill speed
            self.x = self.prev_x
            self.y = self.prev_y
            self.speed = 0

    def draw(self, surface, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.width, self.height))

        rotated = pygame.transform.rotate(surf, -self.angle)
        rect = rotated.get_rect(center=(int(draw_x), int(draw_y)))
        surface.blit(rotated, rect)