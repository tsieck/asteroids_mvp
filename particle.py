import pygame
import random
import math
from constants import (
    PARTICLE_GRAVITY,
    PARTICLE_LIFETIME,
    PARTICLE_MAX_SPEED,
    PARTICLE_MIN_SPEED,
    PARTICLE_RADIUS,
)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(PARTICLE_MIN_SPEED, PARTICLE_MAX_SPEED)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        self.max_lifetime = PARTICLE_LIFETIME

    def update(self, dt):
        self.velocity.y += PARTICLE_GRAVITY * dt
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        fade = max(self.lifetime / self.max_lifetime, 0)
        color = (
            int(self.color[0] * fade),
            int(self.color[1] * fade),
            int(self.color[2] * fade),
        )
        pygame.draw.circle(screen, color, self.position, PARTICLE_RADIUS)
