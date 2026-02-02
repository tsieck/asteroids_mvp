import random
import pygame
from circleshape import CircleShape
from constants import POWERUP_RADIUS


POWERUP_TYPES = [
    "rapid_fire",
    "time_stop",
    "shield",
    "shotgun",
]

POWERUP_COLORS = {
    "rapid_fire": (255, 255, 0),  # neon yellow
    "time_stop": (0, 191, 255),   # neon blue
    "shield": (57, 255, 20),      # neon green
    "shotgun": (255, 20, 147),    # neon pink
}

def choose_powerup_to_spawn(existing_types):
    missing_types = [t for t in POWERUP_TYPES if t not in existing_types]
    if not missing_types:
        return None
    return random.choice(missing_types)


class PowerUp(CircleShape):
    def __init__(self, x, y, powerup_type=None):
        super().__init__(x, y, POWERUP_RADIUS)
        self.powerup_type = powerup_type or random.choice(POWERUP_TYPES)
        self.color = POWERUP_COLORS[self.powerup_type]

    def draw(self, screen):
        scale = self.radius / 14
        glow_phase = (pygame.time.get_ticks() % 1000) / 1000.0
        glow_strength = 0.6 + 0.4 * (1 - abs(2 * glow_phase - 1))
        glow_color = (
            min(255, int(self.color[0] * (0.6 + glow_strength))),
            min(255, int(self.color[1] * (0.6 + glow_strength))),
            min(255, int(self.color[2] * (0.6 + glow_strength))),
        )
        for radius in range(int(self.radius * 1.6), int(self.radius * 0.9), -3):
            pygame.draw.circle(screen, glow_color, self.position, radius, 1)
        local_points = [
            pygame.Vector2(-4, 9),
            pygame.Vector2(2, 2),
            pygame.Vector2(-1, 2),
            pygame.Vector2(4, -9),
            pygame.Vector2(-2, -2),
            pygame.Vector2(1, -2),
        ]
        points = [self.position + (point * scale) for point in local_points]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, glow_color, points, 2)

    def update(self, dt):
        pass
