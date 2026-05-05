import pygame
import math


class Car:
    def __init__(self, x, y, color, controls, stats):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 35
        self.color = color

        self.angle = 270
        self.vx = 0.0
        self.vy = 0.0

        # Load stats from dict
        self.max_speed = stats["max_speed"]
        # NEW — fallback to 5 if key is missing
        self.max_reverse_speed = stats.get("max_reverse_speed", 5)
        self.acceleration = stats["acceleration"]
        self.brake_power = stats["brake_power"]
        self.friction = stats["friction"]
        self.turn_speed = stats["turn_speed"]
        self.grip = stats["grip"]

        self.controls = controls
        self.prev_x = x
        self.prev_y = y

    def handle_input(self, keys):
        rad = math.radians(self.angle)
        facing_x = math.sin(rad)
        facing_y = -math.cos(rad)

        forward_speed = self.vx * facing_x + self.vy * facing_y

        if keys[self.controls["up"]]:
            self.vx += facing_x * self.acceleration
            self.vy += facing_y * self.acceleration

        if keys[self.controls["down"]]:
            self.vx -= facing_x * self.brake_power
            self.vy -= facing_y * self.brake_power

        speed = math.hypot(self.vx, self.vy)
        if speed > 0.8:
            direction = 1 if forward_speed >= 0 else -1
            effective_turn = self.turn_speed * min(speed / 4.0, 1.0)
            if keys[self.controls["left"]]:
                self.angle -= effective_turn * direction
            if keys[self.controls["right"]]:
                self.angle += effective_turn * direction

    def update(self, outer_polygon, inner_polygon):
        self.prev_x = self.x
        self.prev_y = self.y

        self.vx *= self.friction
        self.vy *= self.friction

        # NEW — separate forward and reverse cap
        rad = math.radians(self.angle)
        facing_x = math.sin(rad)
        facing_y = -math.cos(rad)
        forward_speed = self.vx * facing_x + self.vy * facing_y
        speed = math.hypot(self.vx, self.vy)

        if forward_speed >= 0 and speed > self.max_speed:
            self.vx = self.vx / speed * self.max_speed
            self.vy = self.vy / speed * self.max_speed
        elif forward_speed < 0 and speed > self.max_reverse_speed:
            self.vx = self.vx / speed * self.max_reverse_speed
            self.vy = self.vy / speed * self.max_reverse_speed

        rad = math.radians(self.angle)
        facing_x = math.sin(rad)
        facing_y = -math.cos(rad)

        forward_speed = self.vx * facing_x + self.vy * facing_y
        target_vx = facing_x * forward_speed
        target_vy = facing_y * forward_speed

        self.vx = self.vx * (1 - self.grip) + target_vx * self.grip
        self.vy = self.vy * (1 - self.grip) + target_vy * self.grip

        self.x += self.vx
        self.y += self.vy

        in_outer = point_in_polygon(self.x, self.y, outer_polygon)
        in_inner = point_in_polygon(self.x, self.y, inner_polygon)

        if not in_outer or in_inner:
            self.x = self.prev_x
            self.y = self.prev_y
            self.vx *= -0.3
            self.vy *= -0.3

    def draw(self, surface, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        # Main car body
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.width, self.height))

        # Front lights — two small yellow rectangles at the top of the surface
        light_w = 5
        light_h = 4
        light_y = 2  # near the top = front of car
        pygame.draw.rect(surf, (255, 255, 100), (2, light_y, light_w, light_h))
        pygame.draw.rect(surf, (255, 255, 100), (self.width - light_w - 2, light_y, light_w, light_h))

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



def resolve_car_collision(car_a, car_b):
    """Bounce + push two cars away from each other based on their velocities."""
    dx = car_b.x - car_a.x
    dy = car_b.y - car_a.y
    dist = math.hypot(dx, dy)

    # Collision threshold — sum of approximate radii
    min_dist = 35

    if dist == 0 or dist > min_dist:
        return  # no collision

    # Normalize collision vector
    nx = dx / dist
    ny = dy / dist

    # Push cars apart so they don't overlap
    overlap = min_dist - dist
    car_a.x -= nx * overlap * 0.5
    car_a.y -= ny * overlap * 0.5
    car_b.x += nx * overlap * 0.5
    car_b.y += ny * overlap * 0.5

    # Relative velocity along collision normal
    dvx = car_a.vx - car_b.vx
    dvy = car_a.vy - car_b.vy
    dot = dvx * nx + dvy * ny

    # Only resolve if cars are moving toward each other
    if dot <= 0:
        return

    # Restitution — bounciness (1.0 = full elastic, 0.5 = heavy thud)
    restitution = 0.6

    impulse = (1 + restitution) * dot / 2  # equal mass assumed

    car_a.vx -= impulse * nx
    car_a.vy -= impulse * ny
    car_b.vx += impulse * nx
    car_b.vy += impulse * ny