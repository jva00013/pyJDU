import arcade
from PIL import Image


class Tile:
    sprite: arcade.Sprite

    def __init__(self, sprite: arcade.Sprite):
        self.sprite = sprite

    def set_image(self, image: Image):
        bounding_box = image.getbbox()
        tiled_image = image.crop(bounding_box)
        self.sprite.texture = arcade.Texture("__", tiled_image)
