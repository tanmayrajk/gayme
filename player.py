import displayio
import pygame
import math

class Player:
    def __init__(self, scene, x=60, y=60) -> None:
        self.x = float(x)
        self.y = float(y)
        self.width = 9
        self.height = 9
        self.angle = 0.0
        self.rotation_speed = 180.0

        bitmap = displayio.Bitmap(self.width, self.height, 2)

        palette = displayio.Palette(2)
        palette[0] = 0x000000
        palette[1] = 0x50D8FF
        palette.make_transparent(0)

        for py in range(self.height):
            for px in range(self.width):
                bitmap[px, py] = 1

        self.sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            x=int(self.x),
            y=int(self.y),
        )

        scene.append(self.sprite)

    def update(self, dt, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed * dt

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed * dt

        self.angle %= 360

    def draw(self):
        self.sprite.x = round(self.x)
        self.sprite.y = round(self.y)

    def get_direction(self):
        radians = math.radians(self.angle)

        return (
            math.cos(radians),
            math.sin(radians)
        )
