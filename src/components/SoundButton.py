import pathlib
from PIL import Image
import arcade


class SoundButton(arcade.Sprite):
    actual_view: any
    on_texture: arcade.Texture
    off_texture: arcade.Texture

    def __init__(self):
        super().__init__()
        self.on_texture = arcade.Texture("on_texture", Image.open(pathlib.Path("resources/interface/common/on.png")))
        self.off_texture = arcade.Texture("off_texture", Image.open(pathlib.Path("resources/interface/common/off.png")))
        self.actual_view = None
        self.bg_music = arcade.load_sound(pathlib.Path("resources/sound/bg_music.wav")).play(loop=True)
        self.playing = True
        self.texture = self.on_texture
        self.scale = 0.25

    def setup(self, window: arcade.Window):
        self.set_position(self.width, window.height - 30)

    def check_clicked(self, position: tuple[float, float]):
        if not self.collides_with_point(position):
            return
        if self.playing:
            self.bg_music.pause()
            self.texture = self.off_texture
        else:
            self.bg_music.play()
            self.texture = self.on_texture
        self.playing = not self.playing
