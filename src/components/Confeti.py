import arcade

class Confeti(arcade.AnimatedTimeBasedSprite):
    def __init__(self, width, filename, **kwargs):
        scale = float((float(1216.00/1920)*width)/480)
        super().__init__(scale=scale)

    def update(self, delta_time: float = 1 / 60):
        if self.cur_frame_idx >= len(self.frames):
            self.visible = False
        else:
            self.update_animation()
            super().update()