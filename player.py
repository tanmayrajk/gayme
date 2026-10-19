import displayio
import pygame
import math
from sprites import load_spritesheet

class Player:
    def __init__(self, scene, x=60, y=60) -> None:
        self.x = float(x)
        self.y = float(y)
        self.width = 9
        self.height = 9
        self.angle = 0.0
        self.rotation_speed = 360.0

        self.sprite, self.frame_count = load_spritesheet(
            "assets/playa.png"
        )

        self.sprite[0]

        scene.append(self.sprite)

    def update(self, dt, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed * dt

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed * dt

        self.angle %= 360

        direction = round(self.angle / 90) % 4
        self.sprite[0] = direction

    def draw(self):
        self.sprite.x = round(self.x)
        self.sprite.y = round(self.y)

    def get_direction(self):
        radians = math.radians(self.angle)

        return (
            math.cos(radians),
            math.sin(radians)
        )
