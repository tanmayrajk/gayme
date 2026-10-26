import time
import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
from PIL import Image, ImageDraw, ImageFont

from main import background

W = 128
H = 128
SCALE = 2

display = PyGameDisplay(
    width=W * SCALE,
    height=H * SCALE,
    caption="desktop"
)

scene = displayio.Group(scale=SCALE)
display.root_group = scene

def load_background(path):
    image = Image.open(path).convert("RGB")
    width, height = image.size

    colors = list(dict.fromkeys(image.getdata()))
    palette = displayio.Palette(len(colors))
    color_indices = {}

    for i, (r, g, b) in enumerate(colors):
        palette[i] = (r << 16) | (g << 8) | b
        color_indices[(r, g, b)] = i

    bitmap = displayio.Bitmap(
        width, height, max(1, len(colors) - 1).bit_length()
    )

    for y in range(height):
        for x in range(width):
            bitmap[x, y] = color_indices[image.getpixel((x, y))]

    return displayio.TileGrid(bitmap, pixel_shader=palette)

background = load_background("assets/desktop-bg.png")
scene.append(background)

def make_clock(text):
    font = ImageFont.load_default()
    bbox = font.getbbox(text)

    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((-bbox[0], -bbox[1]), text, font=font, fill="black")

    colors = list(dict.fromkeys(image.getdata()))
    palette = displayio.Palette(len(colors))
    indices = {}

    for i, (r, g, b, a) in enumerate(colors):
        palette[i] = (r << 16) | (g << 8) | b

        if a == 0:
            palette.make_transparent(i)

        indices[(r, g, b, a)] = i

    bitmap = displayio.Bitmap(
        width, height, max(1, (len(colors) - 1).bit_length()),
    )

    for y in range(height):
        for x in range(width):
            bitmap[x, y] = indices[image.getpixel((x, y))]

    return displayio.TileGrid(bitmap, pixel_shader=palette)

clock_sprite = make_clock("00:00")
clock_sprite.x = 4
clock_sprite.y = 4
scene.append(clock_sprite)

pygame.init()
running = True
last_time = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.strftime("%H:%M")

    if current_time != last_time:
        scene.remove(clock_sprite)
        clock_sprite = make_clock(current_time)
        clock_sprite.x = 4
        clock_sprite.y = 4
        scene.append(clock_sprite)
        last_time = current_time

    display.refresh()
    time.sleep(0.05)

pygame.quit()

# hi i am going to kill myself very very soon
#
# asdfasd
