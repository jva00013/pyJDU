import arcade.gui
import arcade
import pathlib

from src.components.SoundButton import SoundButton
from src.utils import Utils
from src.views.DressingView import DressingView


class TitleView(arcade.View):
    scene: arcade.Scene
    tile_map: arcade.TileMap
    camera: arcade.Camera
    start_button: arcade.SpriteList

    def __init__(self):
        super().__init__()
        self.sound_sprite_list: arcade.SpriteList = None
        self.sound_button: SoundButton = None

    def setup(self):
        map_path = pathlib.Path("maps/TitleView.json")
        scale = Utils.get_scale(self.window.width, self.window.height)
        self.tile_map = arcade.load_tilemap(map_path, scale)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.start_button = self.scene["ButtonBg"]
        
        self.sound_sprite_list = arcade.SpriteList()
        
        self.sound_button = SoundButton()
        self.sound_button.setup(self.window)
        self.scene.add_sprite("SoundButton", self.sound_button)
        self.sound_sprite_list.append(self.sound_button)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.sound_sprite_list.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        selected_sprites = arcade.get_sprites_at_point((x, y), self.start_button)
        if len(selected_sprites) > 0:
            dress_view = DressingView()
            dress_view.setup(self.sound_button)
            self.window.show_view(dress_view)
        self.sound_button.check_clicked((x, y))
