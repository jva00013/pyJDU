import arcade
import pathlib
from src.utils.scaling import Scaling
import json


class DressingConfiguration:
    class ClothConfiguration:
        name: str
        category: int
        type: int

        def __init__(self, data: dict):
            self.name = data["name"]
            self.category = data["category"]
            self.type = data["type"]

    categories: list[str]
    types: list[str]
    images: list[ClothConfiguration]

    def __init__(self, data: dict):
        self.categories = data["categories"]
        self.types = data["types"]
        self.images = []
        for obj in data["images"].values():
            cloth_config = DressingConfiguration.ClothConfiguration(obj)
            self.images.append(cloth_config)


class DressingView(arcade.View):
    scene: arcade.Scene
    tile_map: arcade.TileMap
    config: DressingConfiguration

    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def setup(self):
        map_path = pathlib.Path("maps/DressingView.json")
        scale = Scaling.get_scale(self.window.width, self.window.height)
        self.tile_map = arcade.load_tilemap(map_path, scale)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # self._setup_dress_layers()

    def _setup_dress_layers(self):
        with open(pathlib.Path("config/cloth.json"), "r") as file:
            data = json.loads(file)
            self.config = DressingConfiguration(data)

        for index, layout_name in enumerate(self.config.categories):
            if index == 0:
                self.scene.add_sprite_list_before(layout_name, "jagger")
                continue
            prev_layout_name = self.config.categories[-1]
            self.scene.add_sprite_list_before(layout_name, prev_layout_name)
