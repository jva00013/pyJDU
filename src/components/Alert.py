import pathlib
import arcade
from py_linq import Enumerable


class Alert:
    def __init__(self, alerts_sprites: arcade.SpriteList):
        self.alert_sprites: arcade.SpriteList = alerts_sprites

        self.easter_unlocked: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "easter_unlocked")
        self.list: arcade.Sprite = Enumerable(self.alert_sprites).first(lambda x: x.properties["name"] == "lista")
        self.done_eggs: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "done_eggs")
        self.applause_sound = arcade.load_sound(pathlib.Path("resources/sound/aplausos.mp3")).play()
        self.applause_sound.pause()

        self.easter_unlocked.visible = False
        self.list.visible = False
        self.done_eggs.visible = False

    def toggle_list(self):
        self.list.visible = not self.list.visible

    def toggle_easter_egg_unlocked(self, value: bool = None):
        self.easter_unlocked.visible = value if value is not None else not self.easter_unlocked.visible

    def show_done_eggs(self):
        self.done_eggs.visible = True
        self.applause_sound.play()

