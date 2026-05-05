CARS = [
    {
        "name": "Bullet",
        "color_p1": (255, 50, 50),
        "color_p2": (200, 30, 30),
        "max_speed": 20,              # bumped from 15
        "max_reverse_speed": 0.8,     # almost impossible to reverse
        "acceleration": 0.5,
        "brake_power": 0.05,          # barely slows down, let alone reverses
        "friction": 0.98,
        "turn_speed": 3.0,
        "grip": 0.72,
        "description": "Blistering speed. Good luck with the corners.",
    },
    {
        "name": "Racer",
        "color_p1": (255, 165, 0),
        "color_p2": (200, 120, 0),
        "max_speed": 19,              # bumped from 14
        "max_reverse_speed": 5,
        "acceleration": 0.45,         # slightly snappier
        "brake_power": 0.4,
        "friction": 0.97,
        "turn_speed": 3.0,
        "grip": 0.67,
        "description": "Fast but drifts. For the experienced.",
    },
    {
        "name": "Balanced",
        "color_p1": (50, 200, 255),
        "color_p2": (30, 140, 200),
        "max_speed": 18,              # bumped from 11
        "max_reverse_speed": 5,
        "acceleration": 0.435,         # slightly snappier
        "brake_power": 0.4,
        "friction": 0.96,
        "turn_speed": 3.0,
        "grip": 0.90,
        "description": "Solid all-rounder. No surprises.",
    },
    {
        "name": "Grip",
        "color_p1": (50, 220, 50),
        "color_p2": (30, 160, 30),
        "max_speed": 19,              # bumped from 11
        "max_reverse_speed": 5,
        "acceleration": 0.41,         # slightly snappier
        "brake_power": 0.4,
        "friction": 0.94,
        "turn_speed": 3.0,
        "grip": 0.97,
        "description": "Glued to the road. Competitive speed, perfect handling.",
    },
]