import pathlib

import arcade
import arcade.gui
from py_linq import Enumerable

from src.views import DressingView


class EggCounter:
    egg_sprite: arcade.Sprite
    list_sprite: arcade.Sprite
    dressing_view: DressingView
    easter_eggs: set[str]

    def __init__(self, ui_sprites: arcade.SpriteList, egg_counter: set[str], dressing_view: DressingView):
        self.easter_eggs = egg_counter
        self.dressing_view = dressing_view
        self.egg_sprite = Enumerable(ui_sprites) \
            .first_or_default(lambda x: "name" in x.properties and x.properties["name"] == "egg")
        self.list_sprite = Enumerable(ui_sprites) \
            .first_or_default(lambda x: "name" in x.properties and x.properties["name"] == "list")
        self.easters = [{"name": "Gertrudis", "field": "gertrudis"},
                        {"name": "Andiamo", "field": "andiamo"},
                        {"name": "Funzo", "field": "funzo"},
                        {"name": "Madre nuclear", "field": "madre_nuclear"},
                        {"name": "Doraemon", "field": "doraemon"},
                        {"name": "Finzo", "field": "finzo"},
                        {"name": "Britney Spears", "field": "britney"},
                        {"name": "Jagger Esland", "field": "esland"},
                        {"name": "Jagger profesor", "field": "profesor"},
                        {"name": "Jagger boxeador", "field": "boxeador"},
                        {"name": "Macho alfa total", "field": "macho_alfa"}]
        self.list_sound = arcade.load_sound(pathlib.Path("resources/sound/lista.wav"))

    def is_completed(self):
        return len(self.easters) == len(self.easter_eggs)

    def add(self, name: str):
        if name not in self.easter_eggs:
            self.dressing_view.alert_manager.toggle_easteregg_tops()
        self.easter_eggs.add(name)
        if self.is_completed():
            self.dressing_view.alert_manager.show_done_eggs()

    def contains_all_cloth(self, *args):
        return Enumerable(args) \
            .all(lambda name: self.dressing_view.jagger.check_if_cloth_present(name))

    def contains_any_cloth(self, *args):
        return Enumerable(args) \
            .any(lambda name: self.dressing_view.jagger.check_if_cloth_present(name))

    def check_clicked(self, position: tuple[float, float]):
        sprite_list = arcade.SpriteList()
        sprite_list.append(self.list_sprite)
        clicked_sprites = arcade.get_sprites_at_point(position, sprite_list)
        if len(clicked_sprites) <= 0:
            return
        self.list_sound.play()
        self.dressing_view.alert_manager.toggle_list()

    def check_easters(self):
        if self.contains_all_cloth("neon", "cono", "andi") and self.contains_any_cloth("zig-zag", "galaxy"):
            self.add("andiamo")
        elif self.contains_all_cloth("britney-1", "britney-1", "skirt-2", "3-black", "mocasines"):
            self.add("britney")
        elif self.contains_all_cloth("rubia", "guantes-2", "gertrudis", "bufandita", "cardigan", "makeup"):
            self.add("gertrudis")
        elif self.contains_all_cloth("gorrita", "funzo", "finzo-0", "rapado", "finzo-2"):
            self.add("funzo")
        elif self.contains_all_cloth("chaleco", "suelto", "cadenita", "botitas") \
                and self.contains_any_cloth("jeans-b", "cargo-b"):
            self.add("macho_alfa")
        elif self.contains_all_cloth("rulos", "musculosa-n", "skirt-2", "guantes", "bebe-nuclear"):
            self.add("madre_nuclear")
        elif self.contains_all_cloth("doraemon", " doraemon2", "short-s", "pantuflas"):
            self.add("doraemon")
        elif self.contains_all_cloth("perilla", "musculosa-n", "corto", "finzo"):
            self.add("finzo")
        elif self.contains_all_cloth("broccli", "vendas", "cinto", "boxeo-1", "coletita"):
            self.add("boxeador")
        elif self.contains_all_cloth("gag", "esland", "turtle-b", "jeans-b", "mocasines", "manbun"):
            self.add("esland")
        elif self.contains_all_cloth("glasses", "camisa-w", "jeans-b", "1-black"):
            self.add("profesor")


    def draw(self):
        x, y = self.egg_sprite.position
        arcade.draw_text(f"{len(self.easter_eggs)}/{len(self.easters)}",
                         start_x=x - 40,
                         start_y=y - 40,
                         align="center",
                         width=85,
                         font_size=16,
                         font_name="Liminality")

        if self.dressing_view.alert_manager.list.visible:
            selection = Enumerable(self.easters) \
                .select(lambda x: f"[OK] {x['name']}" if x["field"] in self.easter_eggs else f"[  ] {x['name']}") \
                .to_list()
            list_sprite = self.dressing_view.alert_manager.list
            x, y = list_sprite.position
            selection.insert(0, "Outfits para hacer:")
            arcade.draw_text("\n".join(selection),
                             width=int(list_sprite.width),
                             multiline=True,
                             start_x=30 + x - (list_sprite.width / 2),
                             start_y=y + (list_sprite.height / 2) - 30,
                             font_size=17,
                             color=(0, 0, 0),
                             font_name="Liminality")
