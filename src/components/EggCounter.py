import arcade
from py_linq import Enumerable

from src.views import DressingView


class EggCounter:
    egg_sprite: arcade.Sprite
    dressing_view: DressingView
    counter: int

    def __init__(self, ui_sprites: arcade.SpriteList, dressing_view: DressingView):
        self.counter = 0
        self.dressing_view = dressing_view
        self.egg_sprite = Enumerable(ui_sprites)\
            .first_or_default(lambda x: "name" in x.properties and x.properties["name"] == "egg")

    def add(self):
        self.counter += 1

    def draw(self):
        x, y = self.egg_sprite.position
        arcade.draw_text(f"{self.counter}/4",
                         start_x=x-40,
                         start_y=y-40,
                         align="center",
                         width=85,
                         font_size=16,
                         font_name="Liminality")
