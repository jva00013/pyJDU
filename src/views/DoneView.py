import pathlib

import arcade

from src.components.Jagger import Jagger
from src.utils.scaling import Scaling

from src.views import DressingView

class DoneView(arcade.View):
    def __init__(self):
        super().__init__()
        self.jagger: Jagger = None
        self.tile_map: arcade.TileMap = None
        self.scene: arcade.Scene = None
        self.sprites: arcade.SpriteList = None

    def setup(self, jagger: Jagger):
        scale = Scaling.get_scale(self.window.width, self.window.height)
        map_path = pathlib.Path("maps/DoneView.json")
        self.tile_map = arcade.load_tilemap(map_path, scaling=scale, hit_box_algorithm="None")
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.sprites = self.scene.get_sprite_list("ui")
        self.jagger = jagger

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        sprites_clicked = arcade.get_sprites_at_point((x, y), self.sprites)
        if len(sprites_clicked) <= 0:
            return
        restart_button = next((x for x in sprites_clicked if "name" in x.properties and x.properties["name"] == "restart"), None)
        if not restart_button:
            return
        dressing_view = DressingView.DressingView()
        self.window.show_view(dressing_view)
        dressing_view.setup()