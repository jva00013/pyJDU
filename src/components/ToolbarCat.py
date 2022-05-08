import arcade
from py_linq import Enumerable
from src.views import DressingView


class ToolbarCat:
    sprite_list: arcade.SpriteList
    dressing_view: DressingView

    def __init__(self, sprites: arcade.SpriteList, dressing_view: DressingView):
        filtered_sprites = Enumerable(sprites)\
            .where(lambda x: "type" in x.properties and x.properties["type"] == "toolbar")\
            .to_list()
        self.sprite_list = arcade.SpriteList()
        for sprite in filtered_sprites:
            self.sprite_list.append(sprite)
        self.dressing_view = dressing_view

    def check_clicked(self, position: tuple[float, float]):
        clicked_sprites = arcade.get_sprites_at_point(position, self.sprite_list)
        if len(clicked_sprites) <= 0:
            return
        clicked_sprite = clicked_sprites[0]
        property_name = clicked_sprite.properties["name"]
        self.dressing_view.inventory.change_cloth_type(property_name.capitalize())
