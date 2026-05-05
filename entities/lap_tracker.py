import time
import math


def _cross_product(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def _point_near_segment(ax, ay, bx, by, px, py, margin=60):
    min_x = min(ax, bx) - margin
    max_x = max(ax, bx) + margin
    min_y = min(ay, by) - margin
    max_y = max(ay, by) + margin
    return min_x <= px <= max_x and min_y <= py <= max_y


class LapTracker:
    def __init__(self, finish_line, total_laps):
        self.finish_line = finish_line
        self.total_laps = total_laps

        self.laps = 0
        self.lap_times = []
        self._best_time = None        # NEW
        self.lap_start = time.time()
        self.finished = False

        self._last_side = None
        self._cooldown = 0
        self._first_crossing_done = False

        self._min_away_distance = 1200
        self._has_been_away = False

        fx1, fy1 = finish_line[0]
        fx2, fy2 = finish_line[1]
        self._finish_mid_x = (fx1 + fx2) / 2
        self._finish_mid_y = (fy1 + fy2) / 2

    def update(self, car_x, car_y, car_x_prev, car_y_prev):
        if self.finished:
            return

        if self._cooldown > 0:
            self._cooldown -= 1
            return

        dist = math.hypot(car_x - self._finish_mid_x, car_y - self._finish_mid_y)
        if dist > self._min_away_distance:
            self._has_been_away = True

        ax, ay = self.finish_line[0]
        bx, by = self.finish_line[1]

        if not _point_near_segment(ax, ay, bx, by, car_x, car_y):
            self._last_side = None
            return

        side = _cross_product(ax, ay, bx, by, car_x, car_y)
        current_side = 1 if side > 0 else -1

        if self._last_side is not None and current_side != self._last_side:
            going_correct = car_y < car_y_prev

            if going_correct:
                if not self._first_crossing_done:
                    self._first_crossing_done = True
                    self._has_been_away = False
                    self._cooldown = 60

                elif self._has_been_away:
                    elapsed = time.time() - self.lap_start
                    self.lap_times.append(elapsed)

                    # Update best time
                    if self._best_time is None or elapsed < self._best_time:
                        self._best_time = elapsed

                    self.lap_start = time.time()
                    self.laps += 1
                    self._has_been_away = False
                    self._cooldown = 60

                    if self.total_laps and self.laps >= self.total_laps + 1:
                        self.finished = True

        self._last_side = current_side

    def current_lap_time(self):
        return time.time() - self.lap_start

    def last_lap_time(self):
        if self.lap_times:
            return self.lap_times[-1]
        return None

    def best_lap_time(self):
        return self._best_time