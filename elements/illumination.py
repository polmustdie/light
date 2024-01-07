from typing import Tuple

import arcade

from enums import IlluminationState


class Illumination:
    def __init__(self, position: Tuple[float, float], size: Tuple[int, int]):
        self.position = position
        self.size = size
        self.light = IlluminationState.DARK

    def draw(self):
        arcade.draw_rectangle_filled(*self.position, *self.size, color=self.light.value)
