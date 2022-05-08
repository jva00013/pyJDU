import json
import os
import pathlib
from itertools import islice

import arcade
from PIL import Image
from py_linq import Enumerable

from src.components.Tile import Tile
from src.views import DressingView


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


class Inventory:
    config: DressingConfiguration
    dressing_view: DressingView
    inventory_sprites: arcade.SpriteList
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

        sprites_filtered = Enumerable(ui_sprites) \
            .where(lambda x: "type" in x.properties and x.properties["type"] == "inventory") \
            .to_list()
        self.inventory_sprites = arcade.SpriteList()
        for sprite in sprites_filtered:
            self.inventory_sprites.append(sprite)

    def check_clicked(self, position: tuple[float, float]):
        sprites_clicked = arcade.get_sprites_at_point(position, self.inventory_sprites)
        if len(sprites_clicked) <= 0:
            return

        total_pages = self.total_pages
        actual_page = self.actual_page
        match sprites_clicked[0].properties["name"]:
            case "previous_page":
                actual_page -= 1
                if actual_page < 0:
                    actual_page = total_pages
                self.change_page(actual_page)
            case "next_page":
                actual_page += 1
                if actual_page == total_pages:
                    actual_page = 0
                self.change_page(actual_page)

    def change_page(self, page_number: int):
        self.actual_page = page_number
        tiles_count = len(self.tiles)
        start_index = page_number * tiles_count
        end_index = start_index + tiles_count
        images_to_show = islice(self.actual_images, start_index, end_index)
        for index, image in enumerate(images_to_show):
            self.tiles[index].set_image(image)

    def change_cloth_type(self, cloth_type: str):
        self.actual_page = 0
        cloth_index = self.config.types.index(cloth_type)
        images_name: list[str] = Enumerable(self.config.images) \
            .where(lambda x: x.type == cloth_index) \
            .select(lambda x: x.name) \
            .to_list()

        self.actual_images = Enumerable(self.images) \
            .where(lambda x: os.path.basename(x.filename) in images_name) \
            .to_list()

        self.total_pages = int(len(self.actual_images) / len(self.tiles))
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

        for index, layout_name in enumerate(self.config.categories):
            if index == 0:
                scene.add_sprite_list_before(layout_name, "jagger")
                continue
            prev_layout_name = self.config.categories[index - 1]
            scene.add_sprite_list_before(layout_name, prev_layout_name)

    def setup(self, scene: arcade.Scene):
        self.load_config(scene)
        self.load_images()
