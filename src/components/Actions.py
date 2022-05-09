from src.views import DressingView
from py_linq import Enumerable
import arcade
import random

from src.views.DoneView import DoneView


class Actions:
    buttons_sprites = arcade.SpriteList
    dressing_view = DressingView

    def __init__(self, ui_sprites: arcade.SpriteList, dressing_view: DressingView):
        self.buttons_sprites = arcade.SpriteList()
        self.dressing_view = dressing_view
        sprites = Enumerable(ui_sprites) \
            .where(lambda x: "type" in x.properties and x.properties["type"] == "button") \
            .to_list()
        for sprite in sprites:
            self.buttons_sprites.append(sprite)

    def check_clicked(self, position: tuple[float, float]):
        sprites = arcade.get_sprites_at_point(position, self.buttons_sprites)
        if len(sprites) <= 0:
            return
        sprite_selected = sprites[0]
        match sprite_selected.properties["name"]:
            case "reset":
                self.dressing_view.jagger.clear()

            case "done":
                done_view = DoneView()
                self.dressing_view.window.show_view(done_view)
                done_view.setup(self.dressing_view.jagger)

            case "random":
                # Amount of categories to select
                len_categories = len(self.dressing_view.inventory.config.categories) - 1
                categories_count = random.randint(0, len_categories)
                for _ in range(categories_count):
                    category_index = random.randint(0, len_categories)
                    category_name = self.dressing_view.inventory.config.categories[category_index]
                    images_from_category = Enumerable(self.dressing_view.inventory.config.images)\
                        .where(lambda x: x.category == category_name)\
                        .select(lambda x: x.name)\
                        .to_list()

                    random_image_index = random.randint(0, len(images_from_category) - 1)
                    image_name = images_from_category[random_image_index]

                    image = Enumerable(self.dressing_view.inventory.images).first(lambda x: image_name in x.filename)
                    self.dressing_view.jagger.set_cloth(image, category_name)
