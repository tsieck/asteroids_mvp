import math

from asteroid import Asteroid


def test_craters_do_not_overlap():
    asteroid = Asteroid(0, 0, 40)
    craters = asteroid._craters
    for i, (offset_a, radius_a) in enumerate(craters):
        for offset_b, radius_b in craters[i + 1 :]:
            distance = offset_a.distance_to(offset_b)
            assert distance >= (radius_a + radius_b) - 1e-6
