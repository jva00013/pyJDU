import pathlib
import arcade
from PIL import Image
from py_linq import Enumerable


class Alert:
    def __init__(self, alerts_sprites: arcade.SpriteList):
        self.alert_sprites: arcade.SpriteList = alerts_sprites

        self.easter_normal: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "easter_normal")
        self.easter_top: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "easter_top")
        self.easter_accessories: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "easter_accessories")
        self.list: arcade.Sprite = Enumerable(self.alert_sprites).first(lambda x: x.properties["name"] == "lista")
        self.done_eggs: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "done_eggs")
        self.tuto: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "tuto")
        self.applause_sound = arcade.load_sound(pathlib.Path("resources/sound/aplausos.mp3")).play()
        self.applause_sound.pause()

        self.easter_normal.visible = False
        self.easter_top.visible = False
        self.easter_accessories.visible = False
        self.list.visible = False
        self.done_eggs.visible = False
        self.tuto.visible = True

    def toggle_list(self):
        self.list.visible = not self.list.visible

    def toggle_easter_normal(self, value: bool = None):
        self.easter_normal.visible = value if value is not None else not self.easter_normal.visible

    def toggle_easter_accessories(self, value: bool = None):
        self.easter_accessories.visible = value if value is not None else not self.easter_accessories.visible

    def toggle_easter_top(self, value: bool = None):
        self.easter_top.visible = value if value is not None else not self.easter_top.visible

    def show_done_eggs(self):
        self.done_eggs.visible = True
        self.applause_sound.play()

    def state_tuto(self, value):
        self.tuto.visible = value
