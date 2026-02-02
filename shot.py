import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS
from constants import LINE_WIDTH

class Shot(CircleShape):
    def __init__(self, x, y, max_distance=None):
        super().__init__(x, y, SHOT_RADIUS)
        self.start_position = pygame.Vector2(x, y)
        self.max_distance = max_distance

    def draw(self, screen):
        center = self.position 
        pygame.draw.circle(screen, "white", center , self.radius ,LINE_WIDTH)
    
    def update(self,dt):
        self.position += self.velocity * dt
        if self.max_distance is not None:
            if self.position.distance_to(self.start_position) >= self.max_distance:
                self.kill()
