import arcade
import arcade.gui
from py_linq import Enumerable

from src.views import DressingView


class EggCounter:
    egg_sprite: arcade.Sprite
    list_sprite: arcade.Sprite
    dressing_view: DressingView
    easter_eggs: set[str]

    def __init__(self, ui_sprites: arcade.SpriteList, dressing_view: DressingView):
        self.easter_eggs = set()
        self.dressing_view = dressing_view
        self.egg_sprite = Enumerable(ui_sprites) \
            .first_or_default(lambda x: "name" in x.properties and x.properties["name"] == "egg")
        self.list_sprite = Enumerable(ui_sprites) \
            .first_or_default(lambda x: "name" in x.properties and x.properties["name"] == "list")

    def add(self, name: str):
        self.easter_eggs.add(name)

    def _contains_cloth(self, name: str):
        return self.dressing_view.jagger.check_if_cloth_present(name)

    def check_clicked(self, position: tuple[float, float]):
        sprite_list = arcade.SpriteList()
        sprite_list.append(self.list_sprite)
        clicked_sprites = arcade.get_sprites_at_point(position, sprite_list)
        if len(clicked_sprites) <= 0:
            return
        self.show_list()

    def show_list(self):
        gertrudis = "✓" if "gertrudis" in self.easter_eggs else " "
        andiamo = "✓" if "andiamo" in self.easter_eggs else " "
        funzo = "✓" if "funzo" in self.easter_eggs else " "
        madre_nuclear = "✓" if "madre_nuclear" in self.easter_eggs else " "
        macho_alfa = "✓" if "macho_alfa" in self.easter_eggs else " "
        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=(
                "Outfits para hacer:\n"
                f"[{gertrudis}] Gertrudis\n"
                f"[{andiamo}] Andiamo\n"
                f"[{funzo}] Funzo\n"
                f"[{madre_nuclear}] Madre nuclear\n"
                f"[{macho_alfa}] Macho alfa total\n"
            ),
            buttons=["Listo"]
        )
        self.dressing_view.manager.add(message_box)

    def check_easters(self):
        if self._contains_cloth("neon") \
                and self._contains_cloth("zig-zag") \
                and self._contains_cloth("cono"):
            self.add("andiamo")
        elif self._contains_cloth("rubia") \
                and self._contains_cloth("guantes-2") \
                and self._contains_cloth("gertrudis"):
            self.add("gertrudis")
        elif self._contains_cloth("gorrita") \
                and self._contains_cloth("funzo") \
                and self._contains_cloth("finzo-0") \
                and self._contains_cloth("rapado") \
                and self._contains_cloth("finzo-2"):
            self.add("funzo")
        elif self._contains_cloth("chaleco") \
                and self._contains_cloth("suelto") \
                and self._contains_cloth("jeans-b") \
                and self._contains_cloth("cadenita"):
            self.add("macho_alfa")
        elif self._contains_cloth("rulos") \
                and self._contains_cloth("musculosa-n") \
                and self._contains_cloth("skirt-2") \
                and self._contains_cloth("guantes") \
                and self._contains_cloth("bebe-nuclear"):
            self.add("madre_nuclear")

    def draw(self):
        x, y = self.egg_sprite.position
        arcade.draw_text(f"{len(self.easter_eggs)}/5",
                         start_x=x - 40,
                         start_y=y - 40,
                         align="center",
                         width=85,
                         font_size=16,
                         font_name="Liminality")
