import os

import arcade
from PIL import Image


class Tile:
    sprite: arcade.Sprite
    original_size: tuple[float, float]
    original_aspect_ratio: float
    original_position: tuple[float, float]
    original_hit_box: arcade.PointList
    original_image: Image
    name: str

    def __init__(self, sprite: arcade.Sprite):
        self.sprite = sprite
        self.original_size = (sprite.width, sprite.height)
        self.original_aspect_ratio = sprite.width / sprite.height
        self.original_position = (sprite.center_x, sprite.center_y)
        self.original_hit_box = sprite.get_hit_box()

    def set_image(self, image: Image):
        self.original_image = image
        self.name = os.path.basename(image.filename)
        bounding_box = image.getbbox()
        tiled_image: Image = image.crop(bounding_box)
        self.sprite.texture = arcade.Texture(f"tile_{image.filename}", tiled_image, hit_box_algorithm="Detailed")
        # Math to preserve aspect ratio
        original_width, original_height = self.original_size
        image_width, image_height = (self.sprite.width, self.sprite.height)
        image_aspect_ratio = image_width / image_height
        if self.original_aspect_ratio > image_aspect_ratio:
            self.sprite.width, self.sprite.height = (image_width * original_height / image_height, original_height)
            return
        self.sprite.width, self.sprite.height = (original_width, image_height * original_width / image_width)
        self.sprite.set_hit_box(self.original_hit_box)

    def check_clicked(self, position: tuple[float, float]) -> bool:
        sprite_list = arcade.SpriteList()
        sprite_list.append(self.sprite)
        clicked_tile = arcade.get_sprites_at_point(position, sprite_list)
        if len(clicked_tile) <= 0:
            return False
        return True

    def restart_position(self):
        self.sprite.center_x, self.sprite.center_y = self.original_position