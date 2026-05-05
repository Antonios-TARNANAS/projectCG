import pygame

class MapBase:
    def draw(self, surface, camera_x, camera_y):
        raise NotImplementedError

    def get_outer_polygon(self):
        raise NotImplementedError

    def get_inner_polygon(self):
        raise NotImplementedError