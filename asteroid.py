import math
import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS
from logger import log_event

NEON_COLORS = [
    (57, 255, 20),   # neon green
    (255, 255, 0),   # neon yellow
    (0, 191, 255),   # neon blue
    (255, 20, 147),  # neon pink
]
class Asteroid(CircleShape):
    time_stopped = False

    @classmethod
    def set_time_stopped(cls, stopped):
        cls.time_stopped = stopped

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = random.choice(NEON_COLORS)
        self._shape_points = self._generate_shape_points()
        self._craters = self._generate_craters()

    def _generate_shape_points(self):
        points = []
        point_count = random.randint(8, 12)
        angle_step = (2 * math.pi) / point_count
        for i in range(point_count):
            angle = i * angle_step + random.uniform(-angle_step * 0.3, angle_step * 0.3)
            distance = self.radius * random.uniform(0.65, 1.1)
            points.append(
                pygame.Vector2(math.cos(angle), math.sin(angle)) * distance
            )
        return points

    def _generate_craters(self):
        craters = []
        crater_count = random.randint(2, 5)
        for _ in range(crater_count):
            angle = random.uniform(0, 2 * math.pi)
            distance = self.radius * random.uniform(0.15, 0.6)
            offset = pygame.Vector2(math.cos(angle), math.sin(angle)) * distance
            crater_radius = self.radius * random.uniform(0.12, 0.28)
            craters.append((offset, crater_radius))
        return craters

    def _darken(self, color, factor):
        return (
            max(0, int(color[0] * factor)),
            max(0, int(color[1] * factor)),
            max(0, int(color[2] * factor)),
        )

    def draw(self, screen):
        points = [self.position + point for point in self._shape_points]
        pygame.draw.polygon(screen, self.color, points, LINE_WIDTH)
        crater_fill = self._darken(self.color, 0.35)
        crater_outline = self._darken(self.color, 0.7)
        for offset, crater_radius in self._craters:
            crater_center = self.position + offset
            pygame.draw.circle(screen, crater_fill, crater_center, crater_radius)
            pygame.draw.circle(
                screen, crater_outline, crater_center, crater_radius, LINE_WIDTH
            )
    
    def update(self,dt):
        if self.time_stopped:
            return
        self.position += self.velocity * dt

    def split(self):
       self.kill()
       if self.radius <= ASTEROID_MIN_RADIUS:
        return
       log_event("asteroid_split")
       angle = random.uniform(20,50)
       velocity1 = self.velocity.rotate(angle)
       velocity2 = self.velocity.rotate(-angle)
       
       new_radius = self.radius - ASTEROID_MIN_RADIUS

       asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
       asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

       asteroid1.velocity = velocity1 * 1.2
       asteroid2.velocity = velocity2 * 1.2
