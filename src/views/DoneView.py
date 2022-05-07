import arcade.gui
import arcade
import pathlib
from arcade.gui import UIOnClickEvent
from src.utils.scaling import Scaling
from src.views import DressingView


class StartButton(arcade.gui.UIFlatButton):
    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window
    def on_click(self, event: UIOnClickEvent):
        dressing_view = DressingView()
        self.window.show_view(dressing_view)
        dressing_view.setup()


class DoneView(arcade.View):
    scene: arcade.Scene
    tile_map: arcade.TileMap
    camera: arcade.Camera

    def __init__(self):
        super().__init__()

    def setup(self):
        map_path = pathlib.Path("maps/DoneView.json")
        self.camera = arcade.Camera(self.window.width, self.window.height)
        scale = Scaling.get_scale(self.window.width, self.window.height)
        self.tile_map = arcade.load_tilemap(map_path, scale)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def update(self, delta_time: float):

