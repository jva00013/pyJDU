import arcade


class Heart(arcade.AnimatedTimeBasedSprite):
    def __init__(self, filename, **kwargs):
        super().__init__(scale=1.4644333333333333333333333333333)


    def update(self, delta_time: float = 1 / 60):
        self.update_animation()
        super().update()
