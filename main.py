import json
import pygame
import sys
from datetime import datetime
import random
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from logger import log_state
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from logger import log_event
from shot import Shot
from particle import Particle
from constants import PARTICLE_COUNT
from powerup import PowerUp
from powerup import choose_powerup_to_spawn
from constants import POWERUP_SPAWN_RATE_SECONDS
from constants import POWERUP_DURATION_SECONDS

LEADERBOARD_FILE = "leaderboard.json"


def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    return []


def save_leaderboard(entries):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2)


def update_leaderboard(entries, score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entries.append({"score": score, "timestamp": timestamp})
    entries.sort(key=lambda item: item["score"], reverse=True)
    return entries[:5]


def setup_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    return {
        "updatable": updatable,
        "drawable": drawable,
        "asteroids": asteroids,
        "shots": shots,
        "particles": particles,
        "powerups": powerups,
        "player": player,
        "asteroid_field": asteroid_field,
    }

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    high_score = 0
    asteroids_destroyed = 0
    powerup_spawn_timer = 0.0
    rapid_fire_time = 0.0
    time_stop_time = 0.0
    shield_time = 0.0
    leaderboard = load_leaderboard()
    if leaderboard:
        high_score = leaderboard[0]["score"]
    score_font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 48)
    print("Starting Asteroids with Pygame version: ", pygame.version.ver)
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    game_over = False
    leaderboard_updated = False

    state = setup_game()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    score = 0
                    game_over = False
                    leaderboard_updated = False
                    asteroids_destroyed = 0
                    powerup_spawn_timer = 0.0
                    rapid_fire_time = 0.0
                    time_stop_time = 0.0
                    shield_time = 0.0
                    state = setup_game()
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    state["player"].swap_weapons()
        screen.fill("black")
        if not game_over:
            powerup_spawn_timer += dt
            if powerup_spawn_timer >= POWERUP_SPAWN_RATE_SECONDS:
                powerup_spawn_timer = 0.0
                existing_types = {p.powerup_type for p in state["powerups"]}
                spawn_type = choose_powerup_to_spawn(existing_types)
                if spawn_type is not None:
                    PowerUp(
                        random.uniform(40, SCREEN_WIDTH - 40),
                        random.uniform(40, SCREEN_HEIGHT - 40),
                        powerup_type=spawn_type,
                    )

            if rapid_fire_time > 0:
                rapid_fire_time = max(0.0, rapid_fire_time - dt)
            if time_stop_time > 0:
                time_stop_time = max(0.0, time_stop_time - dt)
            if shield_time > 0:
                shield_time = max(0.0, shield_time - dt)

            state["player"].rapid_fire = rapid_fire_time > 0
            state["player"].shielded = shield_time > 0
            Asteroid.set_time_stopped(time_stop_time > 0)
            state["asteroid_field"].set_time_stopped(time_stop_time > 0)

            state["updatable"].update(dt)
            for asteroid in state["asteroids"]:
                if state["player"].collides_with(asteroid):
                    if state["player"].shielded:
                        continue
                    log_event("player_hit")
                    print("Game over!")
                    game_over = True
                    break

            if not game_over:
                for asteroid in list(state["asteroids"]):
                    if not asteroid.alive():
                        continue
                    for shot in list(state["shots"]):
                        if asteroid.collides_with(shot):
                            log_event("asteroid_shot")
                            score += 10
                            asteroids_destroyed += 1
                            speed_multiplier = 1.0 + 0.02 * (asteroids_destroyed // 10)
                            state["asteroid_field"].set_speed_multiplier(speed_multiplier)
                            shot.kill()
                            for _ in range(PARTICLE_COUNT):
                                Particle(
                                    asteroid.position.x,
                                    asteroid.position.y,
                                    asteroid.color,
                                )
                            asteroid.split()
                            break

            for powerup in list(state["powerups"]):
                if state["player"].collides_with(powerup):
                    if powerup.powerup_type == "rapid_fire":
                        rapid_fire_time = POWERUP_DURATION_SECONDS
                    elif powerup.powerup_type == "time_stop":
                        time_stop_time = POWERUP_DURATION_SECONDS
                    elif powerup.powerup_type == "shield":
                        shield_time = POWERUP_DURATION_SECONDS
                    elif powerup.powerup_type == "shotgun":
                        state["player"].add_weapon("shotgun")
                    powerup.kill()

        if score > high_score:
            high_score = score

        for obj in state["drawable"]:
            obj.draw(screen)
        score_surface = score_font.render(f"Score: {score}", True, "white")
        high_score_surface = score_font.render(
            f"High Score: {high_score}", True, "white"
        )
        screen.blit(score_surface, (10, 10))
        screen.blit(high_score_surface, (10, 40))
        weapon_primary = state["player"].weapon_primary
        weapon_backup = state["player"].weapon_backup or "None"
        weapon_surface = score_font.render(
            f"Weapon: {weapon_primary}", True, "white"
        )
        backup_surface = score_font.render(
            f"Backup: {weapon_backup}", True, "white"
        )
        screen.blit(weapon_surface, (10, 70))
        screen.blit(backup_surface, (10, 100))

        if game_over:
            if not leaderboard_updated:
                leaderboard = update_leaderboard(leaderboard, score)
                high_score = leaderboard[0]["score"] if leaderboard else 0
                save_leaderboard(leaderboard)
                leaderboard_updated = True
            message = "Game Over - Retry? (Y/N)"
            message_surface = game_over_font.render(message, True, "white")
            message_rect = message_surface.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            screen.blit(message_surface, message_rect)

            leaderboard_title = score_font.render("Top 5 Scores", True, "white")
            title_rect = leaderboard_title.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            )
            screen.blit(leaderboard_title, title_rect)

            for i, entry in enumerate(leaderboard):
                line = f"{i + 1}. {entry['score']} - {entry['timestamp']}"
                line_surface = score_font.render(line, True, "white")
                line_rect = line_surface.get_rect(
                    center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 90 + i * 26)
                )
                screen.blit(line_surface, line_rect)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
#       print(dt)
    

if __name__ == "__main__":
    main()
