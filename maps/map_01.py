import pygame
import math
from maps.map_base import MapBase

def build_oval(cx, cy, rx, ry, steps=60):
    """Returns a list of (x, y) points forming an ellipse."""
    points = []
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append((x, y))
    return points

class Map01(MapBase):
    def __init__(self):
        self.name = "Big Oval"

        cx, cy = 1000, 700  # center of the oval in world space

        # Outer wall — big ellipse
        self.outer = build_oval(cx, cy, rx=800, ry=550)

        # Inner wall — smaller ellipse (road width = difference between them)
        self.inner = build_oval(cx, cy, rx=550, ry=300)

        # Start position for players (right side of oval, on the road)
        self.start_positions = [
            (cx + 680, cy - 60),  # player 1
            (cx + 680, cy + 60),  # player 2
        ]
        self.start_angle = 270  # facing up at start

    def draw(self, surface, camera_x, camera_y):
        # Shift all points by camera offset
        def cam(points):
            return [(x - camera_x, y - camera_y) for x, y in points]

        # Fill road color between outer and inner
        # Draw outer polygon (dark blue road)
        pygame.draw.polygon(surface, (0, 0, 100), cam(self.outer))
        # Draw inner polygon (green grass — cuts out the middle)
        pygame.draw.polygon(surface, (30, 120, 30), cam(self.inner))

        # Draw wall lines
        pygame.draw.polygon(surface, (255, 255, 255), cam(self.outer), 3)
        pygame.draw.polygon(surface, (255, 255, 255), cam(self.inner), 3)

    def get_outer_polygon(self):
        return self.outer

    def get_inner_polygon(self):
        return self.inner