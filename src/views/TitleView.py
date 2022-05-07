import arcade.gui
import arcade
import pathlib
from src.utils.scaling import Scaling
from src.views.DressingView import DressingView


class TitleView(arcade.View):
    scene: arcade.Scene
    tile_map: arcade.TileMap
    camera: arcade.Camera
    start_button: arcade.SpriteList

    def __init__(self):
        super().__init__()

    def setup(self):
        map_path = pathlib.Path("maps/TitleView.json")
        scale = Scaling.get_scale(self.window.width, self.window.height)
        self.tile_map = arcade.load_tilemap(map_path, scale)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.start_button = self.scene["ButtonBg"]

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        selected_sprites = arcade.get_sprites_at_point((x, y), self.start_button)
        if len(selected_sprites) > 0:
            dress_view = DressingView()
            dress_view.setup()
            self.window.show_view(dress_view)
