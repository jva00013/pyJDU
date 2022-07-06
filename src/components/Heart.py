import arcade


class Heart(arcade.AnimatedTimeBasedSprite):
    def __init__(self, width, filename, **kwargs):
        scale = float((float(439.33/1920)*width)/300)
        super().__init__(scale=scale)

    def update(self, delta_time: float = 1 / 60):
        self.update_animation()
        super().update()
