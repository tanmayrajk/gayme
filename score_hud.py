import displayio
from PIL import Image, ImageDraw, ImageFont

class ScoreHUD:
    def __init__(self, scene, x=123, y=5):
        self.scene = scene
        self.x = x
        self.y = y
        self.sprite = None
        self.set_score(0)

    def set_score(self, score):
        text = str(score)

        font = ImageFont.truetype(
            "assets/Tiny5-Regular.ttf",
            16
        )
        bbox = font.getbbox(text)
        width = max(1, bbox[2] + bbox[0])
        height = max(1, bbox[3] - bbox[1])

        image = Image.new("RGBA", (width, height), (0, 0, 0 , 0))
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
            width, height, max(1, (len(colors) - 1).bit_length())
        )

        for py in range(height):
            for px in range(width):
                bitmap[px, py] = indices[image.getpixel((px, py))]

        new_sprite = displayio.TileGrid(bitmap, pixel_shader=palette)
        new_sprite.x = self.x - width
        new_sprite.y = self.y

        if self.sprite is not None:
            new_sprite.hidden = self.sprite.hidden
            self.scene.remove(self.sprite)

        self.sprite = new_sprite
        self.scene.append(self.sprite)
