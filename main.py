from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio
import pygame
import math

SCALE = 4
W = 128
H = 128

player_angle = 0

display = PyGameDisplay(
    width=W*SCALE,
    height=H*SCALE,
    caption="windo"
)

scene = displayio.Group(scale=SCALE)
display.root_group = scene

player_bitmap = displayio.Bitmap(16, 16, 1)
bullet_bitmap = displayio.Bitmap(8, 8, 1)
palette = displayio.Palette(1)
palette[0] = 0xFF0000

player = displayio.TileGrid(
    player_bitmap,
    pixel_shader=palette,
    x=54,
    y=54
)

scene.append(player)

running = True

while running:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        player_angle += 15
        player_angle = player_angle % 360

    if keys[pygame.K_a]:
        player_angle -= 15
        player_angle = player_angle % 360

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("hi lol")

    if display.check_quit():
        break

    radians = math.radians(player_angle)
    dx = math.cos(radians)
    dy = math.sin(radians)
    # print(dx, dy)

pygame.quit()
