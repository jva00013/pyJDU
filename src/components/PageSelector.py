import arcade
from py_linq import Enumerable

from src.views import DressingView


class PageSelector:
    dressing_view: DressingView
    inventory_sprites: arcade.SpriteList

    def __init__(self, ui_sprites: arcade.SpriteList, dressing_view: DressingView):
        self.dressing_view = dressing_view
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

        total_pages = self.dressing_view.inventory.total_pages
        actual_page = self.dressing_view.inventory.actual_page
        match sprites_clicked[0].properties["name"]:
            case "previous_page":
                actual_page -= 1
                if actual_page < 0:
                    actual_page = total_pages
                self.dressing_view.inventory.change_page(actual_page)
            case "next_page":
                actual_page += 1
                if actual_page == total_pages:
                    actual_page = 0
                self.dressing_view.inventory.change_page(actual_page)
