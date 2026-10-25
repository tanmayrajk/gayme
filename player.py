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

        self.sprite, self.frame_count, self.palette = load_spritesheet(
            "assets/playa.png",
            return_palette=True
        )

        scene.append(self.sprite)

        self.original_colors = [
            self.palette[i] for i in range(len(self.palette))
        ]

        self.invincible_timer = 0.0
        self.flash_timer = 0.0
        self.blink_timer = 0.0
        self.is_flashing = False
        self.is_invincible = False
        self.blink_visible = True

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

    def take_damage(self):
        if self.is_invincible:
            return False

        self.is_invincible = True
        self.invincible_timer = 0.75
        self.flash_timer = 0.12
        self.blink_timer = 0.0
        self.is_flashing = True
        self.blink_visible = True

        for i in range(1, len(self.palette)):
            self.palette[i] = 0xFFFFFF

        return True

    def update_hit_effect(self, dt):
        if not self.is_invincible:
            return

        if self.is_flashing:
            self.flash_timer -= dt

            if self.flash_timer <= 0:
                self.is_flashing = False

                for i in range(1, len(self.palette)):
                    self.palette[i] = self.original_colors[i]

        self.blink_timer += dt

        if self.blink_timer >= 0.08:
            self.blink_timer = 0.0
            self.blink_visible = not self.blink_visible
            self.sprite.hidden = not self.blink_visible

        self.invincible_timer -= dt

        if self.invincible_timer <= 0:
            self.is_invincible = False
            self.is_flashing = False
            self.blink_visible = True
            self.sprite.hidden = False

            for i in range(1, len(self.palette)):
                self.palette[i] = self.original_colors[i]
