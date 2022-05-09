class Scaling:
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
