import pathlib

import arcade

from src.components.Explosion import Explosion
from src.components.Jagger import Jagger
from src.components.SoundButton import SoundButton
from src.utils import Utils

from src.views import DressingView


class DoneView(arcade.View):
    def __init__(self):
        super().__init__()
        self.easter_eggs = None
        self.jagger: Jagger | None = None
        self.tile_map: arcade.TileMap | None = None
        self.scene: arcade.Scene | None = None
        self.sprites: arcade.SpriteList | None = None
        self.explosion: Explosion | None = None
        self.explosion_list: arcade.SpriteList | None = None
        self.sound_button: SoundButton | None = None

    def setup(self, jagger: Jagger, categories: list[str], easter_eggs: set[str], sound_button: SoundButton):
        self.sound_button = sound_button
        self.easter_eggs: set[str] = easter_eggs
        scale = Utils.get_scale(self.window.width, self.window.height)
        map_path = pathlib.Path("maps/DoneView.json")
        self.tile_map = arcade.load_tilemap(map_path, scaling=scale, hit_box_algorithm="None")
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        Utils.load_layers(self.scene, categories)
        self.jagger = jagger
        jagger.load_sprites(self.scene)

        self.sprites = self.scene.get_sprite_list("ui")

        self.explosion_list = arcade.SpriteList()
        self.explosion = Explosion(
            arcade.load_spritesheet(file_name=pathlib.Path("resources/interface/done/explosion.png"),
                                    sprite_width=100, sprite_height=100,
                                    columns=7, count=1000))
        self.explosion.center_x = self.jagger.sprite.center_x + 160
        self.explosion.center_y = self.jagger.sprite.center_y
        self.explosion.scale = 10
        self.explosion_list.append(self.explosion)

    def on_draw(self):
        self.clear()
        self.explosion_list.draw()
        self.scene.draw()
        self.sound_button.draw()

    def on_update(self, delta_time: float):
        self.explosion.update()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.sound_button.check_clicked((x, y))
        sprites_clicked = arcade.get_sprites_at_point((x, y), self.sprites)
        if len(sprites_clicked) <= 0:
            return
        restart_button = next(
            (x for x in sprites_clicked if "name" in x.properties and x.properties["name"] == "restart"), None)
        if not restart_button:
            return
        dressing_view = DressingView.DressingView()
        self.window.show_view(dressing_view)
        dressing_view.setup(self.sound_button, self.easter_eggs)
