import displayio
import math

class Projectile:
    def __init__(self, scene, x, y, angle, speed=80.0, color=0xFFAA00):
        self.x = float(x)
        self.y = float(y)

        self.width = 3
        self.height = 3
        self.speed = speed
        self.angle = angle

        radians = math.radians(self.angle)
        self.dx = math.cos(radians)
        self.dy = math.sin(radians)

        bitmap = displayio.Bitmap(self.width, self.height, 1)
        palette = displayio.Palette(1)
        palette[0] = color

        for py in range(self.height):
            for px in range(self.width):
                bitmap[px, py] = 0

        self.sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            x=round(self.x),
            y=round(self.y)
        )

        scene.append(self.sprite)

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

    def draw(self):
        self.sprite.x = round(self.x)
        self.sprite.y = round(self.y)

    def is_offscreen(self, screen_width, screen_height):
        return(
            self.x + self.width < 0
            or self.x > screen_width
            or self.y + self.height < 0
            or self.y > screen_height
        )
