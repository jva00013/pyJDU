import arcade
from PIL import Image


class Tile:
    sprite: arcade.Sprite
    original_size: tuple[float, float]
    original_aspect_ratio: float

    def __init__(self, sprite: arcade.Sprite):
        self.sprite = sprite
        self.original_size = (sprite.width, sprite.height)
        self.original_aspect_ratio = sprite.width / sprite.height

    def set_image(self, image: Image):
        bounding_box = image.getbbox()
        tiled_image: Image = image.crop(bounding_box)
        self.sprite.texture = arcade.Texture(f"tile_{image.filename}", tiled_image)
        # Math to preserve aspect ratio
        original_width, original_height = self.original_size
        image_width, image_height = (self.sprite.width, self.sprite.height)
        image_aspect_ratio = image_width / image_height
        if self.original_aspect_ratio > image_aspect_ratio:
            self.sprite.width, self.sprite.height = (image_width * original_height / image_height, original_height)
            return
        self.sprite.width, self.sprite.height = (original_width, image_height * original_width / image_width)
