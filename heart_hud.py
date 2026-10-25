from sprites import load_spritesheet

class HeartHUD:
    def __init__(self, scene, max_health=3):
        self.max_health = max_health
        self.health = max_health
        self.hearts = []

        for i in range(max_health):
            sprite, _ = load_spritesheet(
                "assets/heart.png",
                frame_width=9,
                frame_height=9,
                return_palette=False
            )

            sprite.x = 5 + i * 10
            sprite.y = 5
            sprite[0] = 1

            scene.append(sprite)
            self.hearts.append(sprite)

    def set_health(self, health):
        self.health = max(0, min(health, self.max_health))

        for i, heart in enumerate(self.hearts):
            heart[0] = 1 if i < self.health else 0
