from itertools import islice

import arcade
import pathlib

import os

from PIL import Image
from src.utils.scaling import Scaling
from src.Tile import Tile
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
        for obj in data["images"]:
            cloth_config = DressingConfiguration.ClothConfiguration(obj)
            self.images.append(cloth_config)


def toolbar_click(ui_clicked: arcade.SpriteList):
    sprite_clicked = ui_clicked[0]
    if "name" not in sprite_clicked.properties:
        return
    match sprite_clicked.properties["name"]:
        case "shirt":
            pass


class DressingView(arcade.View):
    scene: arcade.Scene
    tile_map: arcade.TileMap
    config: DressingConfiguration
    ui_sprites: arcade.SpriteList
    tiles: list[Tile]
    images: list[Image]
    actual_images: list[Image]
    actual_cloth_type: str
    actual_page: int
    total_pages: int
    unlocked_eggs: int

    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def setup(self):
        map_path = pathlib.Path("maps/DressingView.json")
        scale = Scaling.get_scale(self.window.width, self.window.height)
        self.tile_map = arcade.load_tilemap(map_path, scaling=scale, hit_box_algorithm="None")
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self._setup_dress_layers()
        self.ui_sprites = self.scene.get_sprite_list("ui")
        self.tiles = [Tile(x) for x in self.scene.get_sprite_list("ui_tile")]
        self.change_cloth_type(self.config.types[0])

    def change_cloth_type(self, cloth_type: str):
        self.actual_page = 0
        images_name = map(lambda x: x.name,
                          filter(lambda x: x.type == self.config.types.index(cloth_type),
                                 self.config.images))
        self.actual_images = list(filter(lambda x: os.path.basename(x.filename) in images_name, self.images))
        self.change_page(0)

    def change_page(self, page_number: int):
        tiles_count = len(self.tiles)
        images_to_show = islice(self.actual_images, page_number * tiles_count, tiles_count)
        for index, image in enumerate(images_to_show):
            self.tiles[index].set_image(image)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        ui_clicked = arcade.get_sprites_at_point((x, y), self.ui_sprites)
        if len(ui_clicked) <= 0:
            return
        toolbar_click(ui_clicked)

    def load_images(self):
        self.images = []
        for image_config in self.config.images:
            path = pathlib.Path(f"resources/clothes/{image_config.name}")
            image = Image.open(path)
            self.images.append(image)

    def _setup_dress_layers(self):
        with open(pathlib.Path("config/cloth.json"), "r") as file:
            data = json.load(file)
            self.config = DressingConfiguration(data)

        for index, layout_name in enumerate(self.config.categories):
            if index == 0:
                self.scene.add_sprite_list_before(layout_name, "jagger")
                continue
            prev_layout_name = self.config.categories[index - 1]
            self.scene.add_sprite_list_before(layout_name, prev_layout_name)
        self.load_images()
