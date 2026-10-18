import displayio
import math
import random

from pygame.cursors import sizer_x_strings

from projectile import Projectile

class Enemy:
    def __init__(self, scene, x=0, y=0, color=0xFF0000) -> None:
        self.x = float(x)
        self.y = float(y)

        self.width = 9
        self.height = 9
        self.speed = 20.0
        self.angle = 0.0

        self._scene = scene

        bitmap = displayio.Bitmap(self.width, self.height, 2)
        palette = displayio.Palette(2)

        palette[0] = 0x000000
        palette[1] = color
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

    def draw(self):
        self.sprite.x = round(self.x)
        self.sprite.y = round(self.y)


class ChaserEnemy(Enemy):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, x, y, color=0xFF5555)
        self.speed = 35.0

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

            self.x += dx / distance * self.speed * dt
            self.y += dy / distance * self.speed * dt

class ShooterEnemy(Enemy):
    def __init__(self, scene, x, y, player, screen_width, screen_height):
        super().__init__(scene, x, y, color=0xBB66FF)

        self.speed = 20.0

        min_distance = 30.0
        player_cx = player.x + player.width / 2
        player_cy = player.y + player.height / 2

        while True:
            self.target_x = float(
                random.randint(0, screen_width - self.width)
            )
            self.target_y = float(
                random.randint(0, screen_height - self.height)
            )

            target_cx = self.target_x + self.width / 2
            target_cy = self.target_y + self.height / 2

            if math.hypot(target_cx - player_cx, target_cy - player_cy,) >= min_distance:
                break

        self.state = "moving_to_position"

        self.fire_interval = 1.5
        self.fire_timer = self.fire_interval

    def update(self, dt, player, projecticles):
        dx = (
            player.x + player.width / 2 - self.x - self.width / 2
        )
        dy = (
            player.y + player.height / 2 - self.y - self.height / 2
        )

        distance_to_player = math.hypot(dx, dy)

        if distance_to_player > 0:
            self.angle = math.degrees(math.atan2(dy, dx)) % 360

        if self.state == "moving_to_position":
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.hypot(dx, dy)

            if distance <= self.speed * dt or distance < 0.5:
                self.x = self.target_x
                self.y = self.target_y
                self.state = "shooting"
            elif distance > 0:
                self.x += dx / distance * self.speed * dt
                self.y += dy / distance * self.speed * dt

            return

        self.fire_timer -= dt

        if self.fire_timer <= 0:
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2

            bullet = Projectile(
                self._scene,
                cx - 1.5,
                cy - 1.5,
                self.angle,
                speed=35.0,
                color=0xFF3333
            )

            projecticles.append(bullet)
            self.fire_timer = self.fire_interval


# 12-36
# 40-115
# 122-
