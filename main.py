from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio
import pygame
import math

from pygame.mixer_music import play

from player import Player
from enemy import ChaserEnemy, ShooterEnemy
from projectile import Projectile
from enemy_spawner import EnemySpawner
from explosion import Explosion

from sprites import load_background

SCALE = 1
W = 128
H = 128

display = PyGameDisplay(
    width=W*SCALE,
    height=H*SCALE,
    caption="windwhg repodo"
)

scene = displayio.Group(scale=SCALE)
display.root_group = scene

background = load_background("assets/bg.png")
scene.append(background)

clock = pygame.time.Clock()
running = True

def make_circle(radius, color, filled=True):
    size = radius * 2 + 1

    bitmap = displayio.Bitmap(size, size, 2)
    palette = displayio.Palette(2)

    palette[0] = 0x000000
    palette[1] = color
    palette.make_transparent(0)

    center = radius

    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center

            distance_squared = dx * dx + dy * dy

            if filled:
                if distance_squared <= radius * radius:
                    bitmap[x, y] = 1

            else:
                if (radius - 1) ** 2 <= distance_squared <= radius ** 2:
                    bitmap[x, y] = 1

    return displayio.TileGrid(
        bitmap,
        pixel_shader=palette
    )

def make_dot(color):
    bitmap = displayio.Bitmap(3, 3, 1)
    palette = displayio.Palette(1)
    palette[0] = color

    return displayio.TileGrid(bitmap, pixel_shader=palette)

class AimReticle:
    def __init__(self, scene, radius=8):
        self.radius = radius

        self.circle = make_circle(radius, 0x50D8FF, filled=False)
        self.dot = make_dot(0xFFAA00)

        scene.append(self.circle)
        scene.append(self.dot)

    def update(self, player_x, player_y, angle):
        self.circle.x = round(player_x - self.radius)
        self.circle.y = round(player_y - self.radius)

        radians = math.radians(angle)

        dot_x = player_x + math.cos(radians) * self.radius
        dot_y = player_y + math.sin(radians) * self.radius

        self.dot.x = round(dot_x - 1)
        self.dot.y = round(dot_y - 1)

def remove_sprite(scene, sprite):
    for i in range(len(scene)):
        if scene[i] is sprite:
            scene.pop(i)
            return

def collides(a, b):
    return (
        a.x < b.x + b.width
        and a.x + a.width > b.x
        and a.y < b.y + b.height
        and a.y + a.height > b.y
    )

player = Player(scene)
reticle = AimReticle(scene, radius=10)

enemies = []
spawner = EnemySpawner(scene, W, H)

projectiles = []

explosions = []

score = 0

while running:
    dt = clock.tick(60) / 1000
    print(f"FPS: {clock.get_fps(): 1f}", end="\r")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            center_x = player.x + player.width / 2
            center_y = player.y + player.height / 2

            radians = math.radians(player.angle)
            radius = reticle.radius

            spawn_x = center_x + math.cos(radians) * radius
            spawn_y = center_y + math.sin(radians) * radius

            projectile = Projectile(
                scene,
                spawn_x - 1.5,
                spawn_y - 1.5,
                player.angle
            )

            projectiles.append(projectile)

    keys = pygame.key.get_pressed()

    player.update(dt, keys)
    player.draw()

    for projectile in projectiles[:]:
        projectile.update(dt)
        projectile.draw()

        if projectile.owner == "enemy" and collides(player, projectile):
            print("wraps bruh")
            running = False
            break

        if projectile.owner == "player":
            hit_bullet = None

            for other in projectiles:
                if other is projectile:
                    continue

                if other.owner == "enemy" and projectile.collides_with(other):
                    hit_bullet = other
                    break

            if hit_bullet is not None:
                remove_sprite(scene, projectile.sprite)
                projectiles.remove(projectile)

                remove_sprite(scene, hit_bullet.sprite)
                projectiles.remove(hit_bullet)

                continue

        if projectile.owner == "player":
            hit_enemy = None

            for enemy in enemies:
                if projectile.collides_with(enemy):
                    hit_enemy = enemy
                    break

            if hit_enemy is not None:
                remove_sprite(scene, projectile.sprite)
                projectiles.remove(projectile)

                explosion_x = hit_enemy.x
                explosion_y = hit_enemy.y

                explosions.append(
                    Explosion(scene, explosion_x, explosion_y)
                )

                remove_sprite(scene, hit_enemy.sprite)
                enemies.remove(hit_enemy)

                if isinstance(hit_enemy, ChaserEnemy):
                    score += 10
                elif isinstance(hit_enemy, ShooterEnemy):
                    score += 20

                print(f"score: {score}")

                continue

        if projectile.is_offscreen(W, H):
            remove_sprite(scene, projectile.sprite)
            projectiles.remove(projectile)


    spawner.update(dt, player, enemies)

    for enemy in enemies:
        if isinstance(enemy, ChaserEnemy):
            enemy.update(dt, player)
        elif isinstance(enemy, ShooterEnemy):
            enemy.update(dt, player, projectiles)

        enemy.draw()

        if collides(player, enemy):
            print("wraps")
            running = False
            break

    for explosion in explosions[:]:
        explosion.update(dt)

        if explosion.finished:
            explosions.remove(explosion)

    reticle.update(player.x + player.width / 2, player.y + player.height / 2, player.angle)

    display.refresh()

pygame.quit()
