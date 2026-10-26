from sprites import load_spritesheet

class GameOverScreen:
    def __init__(self, scene, screen_width=128, screen_height=128):
        self.sprite, self.frame_count = load_spritesheet(
            "assets/game-over.png",
            frame_width=101,
            frame_height=67
        )

        self.width = 101
        self.height = 67
        self.sprite.x = (screen_width - self.width) // 2
        self.sprite.y = -self.height
        self.sprite.hidden = True
        scene.append(self.sprite)

        self.target_y = (screen_height - self.height) // 2
        self.speed = 300.0
        self.frame_timer = 0.0
        self.frame_duration = 0.25
        self.state = "hidden"

    def show(self):
        self.sprite.hidden = False
        self.sprite.y = -self.height
        self.sprite[0] = 0
        self.frame_timer = 0.0
        self.state = "entering"

    def start_restart(self):
        if self.state == "waiting":
            self.state = "leaving"

    def update(self, dt):
        if self.state == "entering":
            self.sprite.y = round(self.sprite.y + self.speed * dt)
            if self.sprite.y >= self.target_y:
                self.sprite.y = self.target_y
                self.state = "waiting"

        elif self.state == "leaving":
            self.sprite.y = round(self.sprite.y - self.speed * dt)

            if self.sprite.y <= -self.height:
                self.sprite.y = -self.height
                self.sprite.hidden = True
                self.state = "done"

        if self.state in ("entering", "waiting"):
            self.frame_timer += dt

            if self.frame_timer >= self.frame_duration:
                self.frame_timer -= self.frame_duration
                self.sprite[0] = (self.sprite[0] + 1) % self.frame_count
