import arcade
from PIL import Image
from py_linq import Enumerable

from src.components.Tile import Tile
from src.components.Inventory import DressingConfiguration


class Jagger:
    categories: list[str]
    cloth_configuration: list[DressingConfiguration.ClothConfiguration]

    def __init__(self, categories: list[str], cloth_configuration: list[DressingConfiguration.ClothConfiguration]):
        self.sprite: arcade.Sprite | None = None
        self.cloth_configuration = cloth_configuration
        self.categories = categories
        self.cloth_layers: dict[str, arcade.SpriteList | None] = dict()
        for category in categories:
            self.cloth_layers[category] = None

    def setup(self, scene: arcade.Scene):
        self.sprite = scene \
            .get_sprite_list("jagger") \
            .sprite_list[0]
        for category in self.cloth_layers:
            self.cloth_layers[category] = scene.get_sprite_list(category)

    def clear(self):
        for sprite_list in self.cloth_layers.values():
            sprite_list.clear()

    def set_cloth(self, image: Image, category_name: str):
        sprite_list = self.cloth_layers[category_name]
        sprite_list.clear()
        sprite = arcade.Sprite(texture=arcade.Texture(image.filename, image, hit_box_algorithm="None"))
        sprite.set_position(self.sprite.center_x, self.sprite.center_y)
        sprite.width = self.sprite.width
        sprite.height = self.sprite.height
        sprite_list.append(sprite)

    def check_if_cloth_present(self, name: str) -> bool:
        clothes_sprites = list(map(lambda x: x.sprite_list, self.cloth_layers.values()))
        value = Enumerable(clothes_sprites) \
            .where(lambda x: len(x) > 0) \
            .select(lambda x: x[0]) \
            .any(lambda x: name in x.texture.image.filename)
        return value

    def check_collision(self, tile: Tile):
        collision = arcade.check_for_collision(self.sprite, tile.sprite)
        if not collision:
            return
        cloth_configuration: DressingConfiguration.ClothConfiguration = Enumerable(self.cloth_configuration) \
            .first_or_default(lambda x: x.name == tile.name)
        category_name = cloth_configuration.category
        self.set_cloth(tile.original_image, category_name)
