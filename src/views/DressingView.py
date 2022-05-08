import arcade
import pathlib

from src.components.EggCounter import EggCounter
from src.components.Inventory import Inventory
from src.components.ToolbarCat import ToolbarCat
from src.utils.scaling import Scaling
from src.components.Tile import Tile


class DressingView(arcade.View):
    scene: arcade.Scene
    tile_map: arcade.TileMap
    toolbar: ToolbarCat
    inventory: Inventory
    egg_counter: EggCounter

    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.egg_counter.draw()

    def setup(self):
        scale = Scaling.get_scale(self.window.width, self.window.height)
        map_path = pathlib.Path("maps/DressingView.json")
        self.tile_map = arcade.load_tilemap(map_path, scaling=scale, hit_box_algorithm="None")
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        ui_sprites = self.scene.get_sprite_list("ui")
        self.toolbar = ToolbarCat(ui_sprites, self)

        tile_sprites = [Tile(x) for x in self.scene.get_sprite_list("ui_tile")]
        self.inventory = Inventory(ui_sprites, tile_sprites, self)
        self.inventory.setup(self.scene)
        self.inventory.change_cloth_type(self.inventory.config.types[0])

        arcade.load_font(pathlib.Path("resources/fonts/Liminality-Regular.ttf"))
        self.egg_counter = EggCounter(ui_sprites, self)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.toolbar.check_clicked((x, y))
        self.inventory.check_clicked((x, y))
