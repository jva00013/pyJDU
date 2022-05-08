from src.views import DressingView
from py_linq import Enumerable
import arcade


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
                pass

            case "random":
                pass

            case "list":
                pass
