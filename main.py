from blinka_displayio_pygamedisplay import PyGameDisplay
from player import Player
import displayio
import pygame

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
player = Player(scene)

running = True

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

    display.refresh()

pygame.quit()
