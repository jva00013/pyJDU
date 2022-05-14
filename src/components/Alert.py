import pathlib

import arcade
from PIL import Image
from py_linq import Enumerable


class Alert:
    def __init__(self, alerts_sprites: arcade.SpriteList):
        self.alert_sprites: arcade.SpriteList = alerts_sprites

        self.easteregg_tops: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "tops")
        self.easteregg_accesories: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "accesorios")
        self.list: arcade.Sprite = Enumerable(self.alert_sprites).first(lambda x: x.properties["name"] == "lista")
        self.done_eggs: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "done_eggs")
        self.confetti: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "confetti")
        self.load_confetti()
        self.applause_sound = arcade.load_sound(pathlib.Path("resources/sound/aplausos.mp3")).play()
        self.applause_sound.pause()

        self.easteregg_tops.visible = False
        self.easteregg_accesories.visible = False
        self.list.visible = False
        self.done_eggs.visible = False

    def load_confetti(self):
        gif = Image.open(pathlib.Path("resources/interface/done_eggs/confetti.gif"))
        self.confetti.texture = arcade.Texture("confetti", gif)
        self.confetti.visible = False

    def toggle_list(self):
        self.list.visible = not self.list.visible

    def toggle_easteregg_accesories(self, value: bool = None):
        self.easteregg_accesories.visible = value if value is not None else not self.easteregg_accesories.visible

    def toggle_easteregg_tops(self, value: bool = None):
        self.easteregg_tops.visible = value if value is not None else not self.easteregg_tops.visible

    def show_done_eggs(self):
        self.done_eggs.visible = True
        self.confetti.visible = True
        self.applause_sound.play()
