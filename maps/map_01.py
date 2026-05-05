import pygame
import math
from maps.map_base import MapBase


def build_oval(cx, cy, rx, ry, steps=60):
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
        cx, cy = 1000, 700

        self.outer = build_oval(cx, cy, rx=800, ry=550)
        self.inner = build_oval(cx, cy, rx=550, ry=300)

        # NEW — behind the finish line (positive Y = below the line)
        self.start_positions = [
            (cx + 650, cy + 80),
            (cx + 720, cy + 80),
        ]
        self.start_angle = 270

        # Finish line: a vertical segment on the right side of the oval
        # between inner and outer wall, cars must cross going upward (angle ~270)
        # NEW — horizontal line on the right side, between inner and outer wall
        self.finish_line = (
            (cx + 550, cy),   # inner wall edge
            (cx + 800, cy),   # outer wall edge
        )

        # Direction arrows: points around the outside of the track
        # These mark where to place arrow indicators
        self.arrow_positions = [
            (cx, cy - 620, 0),        # top — arrow pointing right
            (cx - 870, cy, 90),       # left — arrow pointing down
            (cx, cy + 620, 180),      # bottom — arrow pointing left
            (cx + 870, cy, 270),      # right — arrow pointing up
        ]

    def draw(self, surface, camera_x, camera_y):
        def cam(points):
            return [(x - camera_x, y - camera_y) for x, y in points]

        def cam_pt(x, y):
            return (x - camera_x, y - camera_y)

        pygame.draw.polygon(surface, (0, 0, 100), cam(self.outer))
        pygame.draw.polygon(surface, (30, 120, 30), cam(self.inner))
        pygame.draw.polygon(surface, (255, 255, 255), cam(self.outer), 3)
        pygame.draw.polygon(surface, (255, 255, 255), cam(self.inner), 3)

        # Draw finish line
        p1 = cam_pt(*self.finish_line[0])
        p2 = cam_pt(*self.finish_line[1])
        pygame.draw.line(surface, (255, 220, 0), p1, p2, 4)

        # Draw direction arrows outside the track
        for wx, wy, angle in self.arrow_positions:
            self._draw_arrow(surface, *cam_pt(wx, wy), angle)

    def _draw_arrow(self, surface, x, y, angle_deg):
        """Draws a simple triangle arrow at (x,y) pointing in angle_deg direction."""
        import math
        size = 30
        rad = math.radians(angle_deg)

        # Tip of arrow
        tip = (x + size * math.sin(rad), y - size * math.cos(rad))
        # Two base corners
        left = (x + size * 0.5 * math.sin(rad - math.pi * 0.75),
                y - size * 0.5 * math.cos(rad - math.pi * 0.75))
        right = (x + size * 0.5 * math.sin(rad + math.pi * 0.75),
                 y - size * 0.5 * math.cos(rad + math.pi * 0.75))

        pygame.draw.polygon(surface, (255, 220, 0), [tip, left, right])

    def get_outer_polygon(self):
        return self.outer

    def get_inner_polygon(self):
        return self.inner

    def get_finish_line(self):
        return self.finish_line