from sprites import load_spritesheet

class TitleMenu:
    def __init__(self, scene, screen_width=128, screen_height=128):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.sprite, self.frame_count = load_spritesheet(
            "assets/title.png",
            frame_width=128,
            frame_height=43
        )

        self.sprite.x = 0
        self.sprite.y = -43
        scene.append(self.sprite)

        self.state = "entering"

        self.target_y = (screen_height - 43) // 2
        self.speed = 300.0

        self.frame_timer = 0.0
        self.frame_duration = 0.25

    def update(self, dt):
        if self.state == "entering":
            self.sprite.y = round(self.sprite.y + self.speed * dt)

            if self.sprite.y >= self.target_y:
                self.sprite.y = self.target_y
                self.state = "waiting"

        elif self.state == "leaving":
            self.sprite.y = round(self.sprite.y - self.speed * dt)

            if self.sprite.y <= -43:
                self.sprite.y = -43
                self.state = "done"
                self.sprite.hidden = True

        if self.state != "done":
            self.frame_timer += dt

            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0.0
                self.sprite[0] = (self.sprite[0] + 1) % self.frame_count

    def start_game(self):
        if self.state == "waiting":
            self.state = "leaving"
