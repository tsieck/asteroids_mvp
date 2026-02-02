import pygame

from shot import Shot


def test_shot_expires_after_max_distance():
    group = pygame.sprite.Group()
    Shot.containers = (group,)
    shot = Shot(0, 0, max_distance=10)
    shot.velocity = pygame.Vector2(10, 0)

    shot.update(0.5)
    assert shot.alive()

    shot.update(0.6)
    assert not shot.alive()
