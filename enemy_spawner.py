import random

from enemy import ChaserEnemy, ShooterEnemy

class EnemySpawner:
    def __init__(self, scene, screen_width, screen_height):
        self.scene = scene
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.spawn_interval = 2.5
        self.spawn_timer = self.spawn_interval

        self.enemy_size = 9

    def spawn_enemy(self, player, enemies):
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "left":
            x = -self.enemy_size
            y = random.randint(0, self.screen_height - 1)

        elif side == "right":
            x = self.screen_width
            y = random.randint(0, self.screen_height - 1)

        elif side == "top":
            x = random.randint(0, self.screen_width - 1)
            y = -self.enemy_size

        else:
            x = random.randint(0, self.screen_width - 1)
            y = self.screen_height

        enemy_type = random.choice(["chaser", "shooter"])

        if enemy_type == "chaser":
            enemy = ChaserEnemy(self.scene, x, y)

        else:
            enemy = ShooterEnemy(
                self.scene,
                x,
                y,
                player,
                self.screen_width,
                self.screen_height
            )

        enemies.append(enemy)

    def update(self, dt, player, enemies):
        self.spawn_timer -= dt

        if self.spawn_timer <= 0:
            self.spawn_enemy(player, enemies)
            self.spawn_timer = self.spawn_interval
