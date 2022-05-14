import arcade


class Utils:
    @staticmethod
    def get_scale(actual_width: int, actual_height: int):
        nominal_width, nominal_height = 1920, 1080
        xscale = actual_width / nominal_width
        yscale = actual_height / nominal_height
        if xscale < 1 and yscale < 1:
            return max(xscale, yscale)
        if xscale > 1 and yscale > 1:
            return min(xscale, yscale)
        return 1

    @staticmethod
    def load_layers(scene: arcade.Scene, categories: list[str]):
        for index, layout_name in enumerate(categories):
            if index == 0:
                scene.add_sprite_list_after(layout_name, "jagger")
                continue
            prev_layout_name = categories[index - 1]
            scene.add_sprite_list_before(layout_name, prev_layout_name)
