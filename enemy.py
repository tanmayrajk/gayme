import displayio
import math

class Enemy:
    def __init__(self, scene, x=0, y=0) -> None:
        self.x = float(x)
        self.y = float(y)

        self.width = 9
        self.height = 9
        self.speed = 20.0
        self.angle = 0.0

        bitmap = displayio.Bitmap(self.width, self.height, 2)
        palette = displayio.Palette(2)

        palette[0] = 0x000000
        palette[1] = 0xFF0000
        palette.make_transparent(0)

        for py in range(self.height):
            for px in range(self.width):
                bitmap[px, py] = 1

        self.sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            x=int(self.x),
            y=int(self.y)
        )

        scene.append(self.sprite)

    def update(self, dt, player):
        enemy_cx = self.x + self.width / 2
        enemy_cy = self.y + self.height / 2

        player_cx = player.x + player.width / 2
        player_cy = player.y + player.height / 2

        dx = player_cx - enemy_cx
        dy = player_cy - enemy_cy

        distance = math.hypot(dx, dy)

        if distance > 0:
            self.angle = math.degrees(math.atan2(dy, dx)) % 360

            dx /= distance
            dy /= distance

            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt

    def draw(self):
        self.sprite.x = round(self.x)
        self.sprite.y = round(self.y)
