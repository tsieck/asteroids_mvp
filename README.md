# Asteroid Game

Neon-styled arcade Asteroids with powerups, particle effects, mouse-aim, and persistent high scores.

## Features
- Irregular, cratered neon asteroids with particle debris
- Mouse aim, WASD thrust + strafe
- Powerups: Rapid Fire, Time Stop, Shielding, Shotgun
- Weapon inventory with swap (`V`)
- Persistent Top 5 leaderboard with timestamps
- Difficulty ramp (asteroids accelerate as you destroy them)

## Controls
- `W` / `S`: Forward / backward
- `A` / `D`: Strafe left / right
- Mouse: Aim/rotate ship
- `Space`: Fire
- `V`: Swap weapons
- `Y`: Retry after game over
- `N`: Quit after game over

## Powerups (20s duration)
- Rapid Fire: Removes shot cooldown
- Time Stop: Freezes asteroids and spawns
- Shielding: Invulnerability + neon shield ring
- Shotgun: Spread shots with limited range

Powerups spawn every 20 seconds, with at most one of each type on-screen at a time.

## Weapons
- Blaster: Default single shot
- Shotgun: 5‑pellet spread, range limited to 25% of screen size

You can carry a primary and a backup weapon. Pickups fill the backup slot (or replace it if full). Use `V` to swap.

## Scoring
- +10 points per asteroid destroyed
- Top 5 scores are stored in `leaderboard.json` with end-of-run timestamps

## How to Run
```bash
python main.py
```

## Tests
This project uses pytest (dev dependency).

```bash
python -m pytest
```

## Project Layout
- `main.py`: Game loop, HUD, leaderboard, powerups
- `asteroid.py`: Asteroid rendering, craters, time stop
- `player.py`: Ship movement, weapons, shooting
- `shot.py`: Projectiles + range limiter
- `powerup.py`: Powerup rendering and selection
- `particle.py`: Debris particles
- `constants.py`: Tunables

## Notes
- Leaderboard persists in `leaderboard.json`.
- If you want different visuals (colors, glow intensity, ship style), adjust in `asteroid.py`, `powerup.py`, and `player.py`.
