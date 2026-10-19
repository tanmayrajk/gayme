import displayio
from PIL import Image

def load_spritesheet(path, frame_width=9, frame_height=9):
    image = Image.open(path).convert("RGBA")
    width, height = image.size

    colors = list(dict.fromkeys(image.getdata()))
    palette = displayio.Palette(len(colors))

    color_indices = {}

    for index, (r, g, b, a) in enumerate(colors):
        palette[index] = (r << 16) | (g << 8) | b
        if a == 0:
            palette.make_transparent(index)
        color_indices[(r, g, b, a)] = index

    bitmap = displayio.Bitmap(width, height, len(colors))

    for y in range(height):
        for x in range(width):
            bitmap[x, y] = color_indices[image.getpixel((x, y))]

    grid = displayio.TileGrid(
        bitmap,
        pixel_shader=palette,
        width=1,
        height=1,
        tile_width=frame_width,
        tile_height=frame_height
    )

    return grid, width // frame_width
