from player import Player


def test_weapon_inventory_and_swap():
    player = Player(0, 0)
    assert player.weapon_primary == "blaster"
    assert player.weapon_backup is None

    player.add_weapon("shotgun")
    assert player.weapon_primary == "blaster"
    assert player.weapon_backup == "shotgun"

    player.swap_weapons()
    assert player.weapon_primary == "shotgun"
    assert player.weapon_backup == "blaster"

    player.add_weapon("laser")
    assert player.weapon_primary == "shotgun"
    assert player.weapon_backup == "laser"
