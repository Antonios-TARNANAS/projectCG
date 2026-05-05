import pygame
import math


class Car:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 35
        self.color = color

        # Facing direction in degrees
        self.angle = 270

        # Actual velocity vector
        self.vx = 0.0
        self.vy = 0.0

        # Stats — will move to data/cars.py in Step 5
        self.max_speed = 12
        self.acceleration = 0.3
        self.brake_power = 0.4
        self.friction = 0.97       # multiplier per frame — 1.0 = no friction, 0.9 = heavy friction
        self.turn_speed = 3.0
        self.grip = 0.85           # 1.0 = no drift, 0.0 = full ice. 0.8-0.9 = fun drift

        self.controls = controls

        self.prev_x = x
        self.prev_y = y

    def handle_input(self, keys):
        # Current speed in the facing direction
        rad = math.radians(self.angle)
        facing_x = math.sin(rad)
        facing_y = -math.cos(rad)

        # Dot product of velocity and facing = how fast we're going forward
        forward_speed = self.vx * facing_x + self.vy * facing_y

        if keys[self.controls["up"]]:
            self.vx += facing_x * self.acceleration
            self.vy += facing_y * self.acceleration

        if keys[self.controls["down"]]:
            # Brake / reverse
            self.vx -= facing_x * self.brake_power
            self.vy -= facing_y * self.brake_power

        # Only turn if actually moving
        speed = math.hypot(self.vx, self.vy)
        if speed > 0.8:
            direction = 1 if forward_speed >= 0 else -1
            # Turn speed scales with speed — fluid at low speed, responsive at high speed
            effective_turn = self.turn_speed * min(speed / 4.0, 1.0)
            if keys[self.controls["left"]]:
                self.angle -= effective_turn * direction
            if keys[self.controls["right"]]:
                self.angle += effective_turn * direction

    def update(self, outer_polygon, inner_polygon):
        self.prev_x = self.x
        self.prev_y = self.y

        # Friction — bleeds speed every frame
        self.vx *= self.friction
        self.vy *= self.friction

        # Clamp to max speed
        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed:
            self.vx = self.vx / speed * self.max_speed
            self.vy = self.vy / speed * self.max_speed

        # Grip — blend velocity toward facing direction
        # Low grip = velocity changes slowly = drift
        rad = math.radians(self.angle)
        facing_x = math.sin(rad)
        facing_y = -math.cos(rad)

        # Project current velocity onto facing direction
        forward_speed = self.vx * facing_x + self.vy * facing_y

        # Target velocity = fully aligned with facing
        target_vx = facing_x * forward_speed
        target_vy = facing_y * forward_speed

        # Blend current velocity toward target by grip amount
        self.vx = self.vx * (1 - self.grip) + target_vx * self.grip
        self.vy = self.vy * (1 - self.grip) + target_vy * self.grip

        # Move
        self.x += self.vx
        self.y += self.vy

        # Wall collision — push back and kill velocity
        in_outer = point_in_polygon(self.x, self.y, outer_polygon)
        in_inner = point_in_polygon(self.x, self.y, inner_polygon)

        if not in_outer or in_inner:
            self.x = self.prev_x
            self.y = self.prev_y
            # Kill velocity on impact
            self.vx *= -0.3
            self.vy *= -0.3

    def draw(self, surface, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.width, self.height))

        rotated = pygame.transform.rotate(surf, -self.angle)
        rect = rotated.get_rect(center=(int(draw_x), int(draw_y)))
        surface.blit(rotated, rect)


def point_in_polygon(x, y, polygon):
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