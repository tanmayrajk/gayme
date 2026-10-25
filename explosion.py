from sprites import load_spritesheet

class Explosion:
    def __init__(self, scene, x, y, frame_duration=0.06):
        self.scene = scene
        self.x = x
        self.y = y
        self.frame_duration = frame_duration
        self.timer = 0.0
        self.frame = 0
        self.finished = False

        self.sprite, self.frame_count = load_spritesheet(
            "assets/explosion.png"
        )
        self.sprite.x = round(x)
        self.sprite.y = round(y)
        self.sprite[0] = 0

        scene.append(self.sprite)

    def update(self, dt):
        if self.finished:
            return

        self.timer += dt

        if self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.frame += 1

            if self.frame >= self.frame_count:
                for i in range(len(self.scene)):
                    if self.scene[i] is self.sprite:
                        self.scene.pop(i)
                        break

                self.finished = True
                return

            self.sprite[0] = self.frame
