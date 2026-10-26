import displayio
import pygame
import time

from blinka_displayio_pygamedisplay import PyGameDisplay

W = 128
H = 128
SCALE = 2

pygame.init()
displayio.release_displays
display = PyGameDisplay(
    width=W * SCALE,
    height =H * SCALE,
    caption = "App Drawer"
)

scene = displayio.Group(scale=SCALE)
display.root_group = scene

BG = 0x181923
WHITE = 0xFFFFFF
MUTED = 0xA0AEC0
ACCENT = 0x53B3ED
ICON_BG = 0x2D3748

background_bitmap = displayio.Bitmap(W, H, 1)
background_palette = displayio.Palette(1)
background_palette[0] = BG

background = displayio.TileGrid(
    background_bitmap,
    pixel_shader=background_palette,
)
scene.append(background)

def make_icon(color, size=20):
    bitmap = displayio.Bitmap(size, size, 2)
    palette = displayio.Palette(2)

    palette[0] = ICON_BG
    palette[1] = color

    for y in range(3, size - 3):
        for x in range(3, size -3):
            if x in (3, size - 4) or y in (3, size - 4):
                bitmap[x, y] = 1
            elif (x + y) % 4 == 0:
                bitmap[x, y] = 1

    return displayio.TileGrid(bitmap, pixel_shader=palette)

apps = [
    {"name": "Game", "color": 0xF6AD55},
    {"name": "Files", "color": 0x68D391},
    {"name": "Music", "color": 0xB794F4},
    {"name": "Settings", "color": 0x63B3ED},
]

positions = [(30, 25), (78, 25), (30, 75), (78, 75),]

icons = []

for app, (x, y) in zip(apps, positions):
    icon = make_icon(app["color"])
    icon.x = x
    icon.y = y
    scene.append(icon)
    icons.append(icon)

def make_outline(width, height, color):
    bitmap = displayio.Bitmap(width, height, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = color
    palette.make_transparent(0)

    for x in range(width):
        bitmap[x, 0] = 1
        bitmap[x, height - 1] = 1

    for y in range(height):
        bitmap[0, y] = 1
        bitmap[width - 1, y] = 1

    return displayio.TileGrid(bitmap, pixel_shader=palette)

selection = make_outline(30, 30, ACCENT)
scene.append(selection)

selected = 0
