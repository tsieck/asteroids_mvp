import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH
from constants import PLAYER_RADIUS
from constants import PLAYER_TURN_SPEED
from constants import PLAYER_SPEED
from constants import PLAYER_SHOOT_SPEED
from shot import Shot
from constants import PLAYER_SHOOT_COOLDOWN_SECONDS
from constants import SHOTGUN_PELLETS
from constants import SHOTGUN_SPREAD_DEGREES
from constants import SHOTGUN_RANGE_PIXELS





class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.rapid_fire = False
        self.shielded = False
        self.weapon_primary = "blaster"
        self.weapon_backup = None


    def ship_points(self):
        scale = self.radius
        local_points = [
            pygame.Vector2(0, 1.2 * scale),     # nose
            pygame.Vector2(0.55 * scale, 0.35 * scale),
            pygame.Vector2(0.95 * scale, -0.2 * scale),  # right wing tip
            pygame.Vector2(0.35 * scale, -0.35 * scale),
            pygame.Vector2(0, -1.0 * scale),    # tail
            pygame.Vector2(-0.35 * scale, -0.35 * scale),
            pygame.Vector2(-0.95 * scale, -0.2 * scale), # left wing tip
            pygame.Vector2(-0.55 * scale, 0.35 * scale),
        ]
        return [self.position + point.rotate(self.rotation) for point in local_points]
    
    def draw(self,screen):
        pygame.draw.polygon(screen, "white", self.ship_points(), LINE_WIDTH)
        cockpit_center = self.position + pygame.Vector2(0, 0.3 * self.radius).rotate(
            self.rotation
        )
        pygame.draw.circle(
            screen,
            "white",
            cockpit_center,
            int(self.radius * 0.18),
            LINE_WIDTH,
        )
        if self.shielded:
            pygame.draw.circle(
                screen,
                (0, 191, 255),
                self.position,
                int(self.radius * 1.4),
                LINE_WIDTH,
            )

    def swap_weapons(self):
        if self.weapon_backup is None:
            return
        self.weapon_primary, self.weapon_backup = (
            self.weapon_backup,
            self.weapon_primary,
        )

    def add_weapon(self, weapon_name):
        if weapon_name == self.weapon_primary or weapon_name == self.weapon_backup:
            return
        if self.weapon_backup is None:
            self.weapon_backup = weapon_name
            return
        self.weapon_backup = weapon_name

    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        direction = mouse_pos - self.position
        if direction.length_squared() > 0:
            self.rotation = pygame.Vector2(0, 1).angle_to(direction)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.strafe(-dt)
        if keys[pygame.K_d]:
            self.strafe(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.shot_cooldown >0:
            self.shot_cooldown -= dt
    def move(self,dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def strafe(self, dt):
        unit_vector = pygame.Vector2(1, 0)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown > 0:
            return
        if not self.rapid_fire:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        if self.weapon_primary == "shotgun":
            base_direction = pygame.Vector2(0, 1).rotate(self.rotation)
            half_spread = SHOTGUN_SPREAD_DEGREES / 2
            for i in range(SHOTGUN_PELLETS):
                if SHOTGUN_PELLETS == 1:
                    angle = 0
                else:
                    angle = -half_spread + (i * SHOTGUN_SPREAD_DEGREES / (SHOTGUN_PELLETS - 1))
                direction = base_direction.rotate(angle)
                shot = Shot(
                    self.position.x,
                    self.position.y,
                    max_distance=SHOTGUN_RANGE_PIXELS,
                )
                shot.velocity = direction * PLAYER_SHOOT_SPEED
        else:
            shot = Shot(self.position.x, self.position.y)
            direction = pygame.Vector2(0,1)
            direction = direction.rotate(self.rotation)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
