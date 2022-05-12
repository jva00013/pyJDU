import json
import math
import os
import pathlib

import arcade
from PIL import Image
from py_linq import Enumerable

from src.utils import Utils
from src.views import DressingView
from src.components.PageSelector import PageSelector
from src.components.Tile import Tile


class DressingConfiguration:
    class ClothConfiguration:
        name: str
        category: str
        type: str

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


class Inventory:
    config: DressingConfiguration
    dressing_view: DressingView
    page_selector: PageSelector
    tiles: list[Tile]
    images: list[Image]
    actual_images: list[Image]
    actual_cloth_type: str
    actual_page: int
    total_pages: int
    unlocked_eggs: int

    def __init__(self, ui_sprites: arcade.SpriteList, tiles: list[Tile], dressing_view: DressingView):
        self.actual_page = 0
        self.total_pages = 0
        self.actual_images = []
        self.unlocked_eggs = 0
        self.dressing_view = dressing_view
        self.tiles = tiles
        self.page_selector = PageSelector(ui_sprites, self.dressing_view)
        self.dummy_image = Image.open(pathlib.Path("resources/interface/dressing/frame.png"))
        self.drag_sound = arcade.load_sound(pathlib.Path("resources/sound/grab.wav"))

    def check_clicked(self, position: tuple[float, float], button: int) -> None | Tile:
        self.page_selector.check_clicked(position)
        clicked_tile = Enumerable(self.tiles).first_or_default(lambda x: x.check_clicked(position, button))
        if clicked_tile is None:
            return None
        self.drag_sound.play()
        return clicked_tile

    def change_page(self, page_number: int):
        self.actual_page = page_number
        tiles_count = len(self.tiles)
        start_index = (page_number-1) * tiles_count
        end_index = start_index + tiles_count
        images_to_show = self.actual_images[start_index:end_index]
        for index, image in enumerate(images_to_show):
            self.tiles[index].set_image(image)
        for tile in self.tiles[len(images_to_show):tiles_count]:
            tile.set_image(self.dummy_image)

    def change_cloth_type(self, cloth_type: str):
        self.actual_page = 0
        images_name: list[str] = Enumerable(self.config.images) \
            .where(lambda x: x.type == cloth_type) \
            .select(lambda x: x.name) \
            .to_list()

        self.actual_images = Enumerable(self.images) \
            .where(lambda x: os.path.basename(x.filename) in images_name) \
            .to_list()

        self.total_pages = math.ceil(len(self.actual_images) / len(self.tiles))
        self.change_page(1)

    def load_images(self):
        self.images = []
        for image_config in self.config.images:
            path = pathlib.Path(f"resources/clothes/{image_config.name}")
            image = Image.open(path)
            self.images.append(image)

    def load_config(self, scene: arcade.Scene):
        with open(pathlib.Path("config/cloth.json"), "r") as file:
            data = json.load(file)
            self.config = DressingConfiguration(data)

        Utils.load_layers(scene, self.config.categories)

    def setup(self, scene: arcade.Scene):
        self.load_config(scene)
        self.load_images()
