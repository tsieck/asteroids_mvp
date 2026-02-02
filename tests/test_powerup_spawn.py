from powerup import choose_powerup_to_spawn
from powerup import POWERUP_TYPES


def test_choose_powerup_to_spawn_only_missing():
    existing = {POWERUP_TYPES[0], POWERUP_TYPES[1]}
    chosen = choose_powerup_to_spawn(existing)
    assert chosen in set(POWERUP_TYPES) - existing


def test_choose_powerup_to_spawn_none_when_full():
    existing = set(POWERUP_TYPES)
    chosen = choose_powerup_to_spawn(existing)
    assert chosen is None
