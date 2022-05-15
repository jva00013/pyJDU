import json
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

    class EasterConfig:
        name: str
        field: str
        clothes: dict[str, list[str]]

        def __init__(self, data: dict):
            self.name = data["name"]
            self.field = data["field"]
            self.clothes = data["clothes"]

    def __init__(self, ui_sprites: arcade.SpriteList, egg_counter: set[str], dressing_view: DressingView):
        self.easter_eggs = egg_counter
        self.dressing_view = dressing_view
        self.egg_sprite = Enumerable(ui_sprites) \
            .first_or_default(lambda x: "name" in x.properties and x.properties["name"] == "egg")
        self.list_sprite = Enumerable(ui_sprites) \
            .first_or_default(lambda x: "name" in x.properties and x.properties["name"] == "list")
        with open("config/easter_egg.json", "r") as file:
            self.all_easters = list(map(lambda x: EggCounter.EasterConfig(x), json.load(file)))

        self.list_sound = arcade.load_sound(pathlib.Path("resources/sound/lista.wav"))

    def is_completed(self):
        return len(self.all_easters) == len(self.easter_eggs)

    def add(self, name: str):
        if name in self.easter_eggs:
            return
        self.easter_eggs.add(name)
        if self.is_completed():
            self.dressing_view.sound_button.bg_music.pause()
            self.dressing_view.alert_manager.show_done_eggs()
            return
        else:
            self.dressing_view.alert_manager.toggle_easter_egg_unlocked()

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
        for easter_config in self.all_easters:
            all_clothes = easter_config.clothes["all"]
            any_clothes = None
            if "any" in easter_config.clothes:
                any_clothes = easter_config.clothes["any"]
            result = self.contains_all_cloth(*all_clothes)
            if any_clothes is not None:
                result = result and self.contains_any_cloth(*any_clothes)
            if result:
                self.add(easter_config.field)

    def draw(self):
        x, y = self.egg_sprite.position
        arcade.draw_text(f"{len(self.easter_eggs)}/{len(self.all_easters)}",
                         start_x=x - 40,
                         start_y=y - 40,
                         align="center",
                         width=85,
                         font_size=16,
                         font_name="Liminality")

        if self.dressing_view.alert_manager.list.visible:
            selection = Enumerable(self.all_easters) \
                .select(
                lambda config: f"[OK] {config.name}" if config.field in self.easter_eggs else f"[  ] {config.name}") \
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
                             color=(187, 125, 234),
                             font_name="Liminality")
