from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio
import pygame
import math

from player import Player
from enemy import Enemy

SCALE = 4
W = 128
H = 128

display = PyGameDisplay(
    width=W*SCALE,
    height=H*SCALE,
    caption="windo"
)

scene = displayio.Group(scale=SCALE)
display.root_group = scene

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


player = Player(scene)
reticle = AimReticle(scene, radius=10)

enemy = Enemy(scene, x=10, y=10)

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dx, dy = player.get_direction()
            print(f"dir: ({dx:.2f}, {dy:.2f})")

    keys = pygame.key.get_pressed()

    player.update(dt, keys)
    player.draw()

    enemy.update(dt, player)
    enemy.draw()

    reticle.update(player.x + player.width / 2, player.y + player.height / 2, player.angle)

    display.refresh()

pygame.quit()
