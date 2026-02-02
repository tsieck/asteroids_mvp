import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS
from constants import LINE_WIDTH

class Shot(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y,SHOT_RADIUS)

    def draw(self, screen):
        center = self.position 
        pygame.draw.circle(screen, "white", center , self.radius ,LINE_WIDTH)
    
    def update(self,dt):
        self.position += self.velocity * dt