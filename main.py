import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay

SCALE = 4
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128

display = PyGameDisplay(
    width=SCREEN_WIDTH * SCALE,
    height=SCREEN_HEIGHT * SCALE,
    caption="windo",
)

scene = displayio.Group(scale=SCALE)
display.root_group = scene

while True:
    if display.check_quit():
        break
