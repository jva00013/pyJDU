import arcade
import pathlib

from src.components.Actions import Actions
from src.components.EggCounter import EggCounter
from src.components.Inventory import Inventory
from src.components.Jagger import Jagger
from src.components.Toolbar import Toolbar
from src.utils.scaling import Scaling
from src.components.Tile import Tile


class DressingView(arcade.View):
    scene: arcade.Scene
    tile_map: arcade.TileMap
    toolbar: Toolbar
    actions: Actions
    inventory: Inventory
    egg_counter: EggCounter
    jagger: Jagger
    tile_dragged: Tile | None

    def __init__(self):
        super().__init__()
        self.tile_dragged = None

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
        self.toolbar = Toolbar(ui_sprites, self)
        self.actions = Actions(ui_sprites, self)

        tile_sprites = [Tile(x) for x in self.scene.get_sprite_list("ui_tile")]
        self.inventory = Inventory(ui_sprites, tile_sprites, self)
        self.inventory.setup(self.scene)
        self.inventory.change_cloth_type(self.inventory.config.types[0])

        self.jagger = Jagger(self.inventory.config.categories, self.inventory.config.images)
        self.jagger.setup(self.scene)

        arcade.load_font(pathlib.Path("resources/fonts/Liminality-Regular.ttf"))
        self.egg_counter = EggCounter(ui_sprites, self)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.toolbar.check_clicked((x, y))
        self.tile_dragged = self.inventory.check_clicked((x, y))
        self.actions.check_clicked((x, y))

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if not self.tile_dragged:
            return
        self.tile_dragged.sprite.center_x += dx
        self.tile_dragged.sprite.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if not self.tile_dragged:
            return
        self.jagger.check_collision(self.tile_dragged)
        self.tile_dragged.restart_position()
        self.tile_dragged = None
