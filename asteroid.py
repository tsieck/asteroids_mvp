import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS
from logger import log_event
class Asteroid(CircleShape):
    def __init___(self, x, y, radius):
        super().__init__(x,y,radius)
        
   
    
    def draw(self, screen):
        center = self.position 
        pygame.draw.circle(screen, "white", center , self.radius ,LINE_WIDTH)
    
    def update(self,dt):
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