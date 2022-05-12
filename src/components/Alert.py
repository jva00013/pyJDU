import arcade
from py_linq import Enumerable


class Alert:
    def __init__(self, alerts_sprites: arcade.SpriteList):
        self.alert_sprites: arcade.SpriteList = alerts_sprites
        self.easteregg_accesories: arcade.Sprite | None = None
        self.easteregg_tops: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "tops")
        self.easteregg_accesories: arcade.Sprite = Enumerable(self.alert_sprites).first(
            lambda x: x.properties["name"] == "accesorios")
        self.list: arcade.Sprite = Enumerable(self.alert_sprites).first(lambda x: x.properties["name"] == "lista")
        self.easteregg_tops.visible = False
        self.easteregg_accesories.visible = False
        self.list.visible = False

    def toggle_list(self):
        self.list.visible = not self.list.visible

    def toggle_easteregg_accesories(self, value: bool = None):
        self.easteregg_accesories.visible = value if value is not None else not self.easteregg_accesories.visible

    def toggle_easteregg_tops(self, value: bool = None):
        self.easteregg_tops.visible = value if value is not None else not self.easteregg_tops.visible
