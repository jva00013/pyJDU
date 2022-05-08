import arcade
from py_linq import Enumerable

from src.views import DressingView


class EggCounter:
    sprites: arcade.SpriteList
    dressing_view: DressingView

    def __init__(self, ui_sprites: arcade.SpriteList, dressing_view: DressingView):
        self.dressing_view = dressing_view
        self.sprites = arcade.SpriteList()
        sprites = Enumerable(ui_sprites)\
            .where(lambda x: "name" in x.properties and x.properties["name"] == "egg_counter")\
            .to_list()
        for sprite in sprites:
            self.sprites.append(sprite)


    def add(self):
        pass