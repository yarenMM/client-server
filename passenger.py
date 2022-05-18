import math


class Passenger:
    def __init__(self, id, rect, ttl):
        self.id = id
        self.direction = 0
        x, y, w, h = rect
        self.cx = (x + w) // 2
        self.cy = (y + h) // 2
        self.ttl = ttl
        self.init_coord_y = self.cy
        self.passed_upper = False
        self.passed_lower = False
