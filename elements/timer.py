from typing import Tuple

import arcade
from datetime import datetime, timedelta
from arcade import gui


class Timer(arcade.Text):
    ELEMENT_SIZE = 20

    def __init__(self, position: Tuple[float, float], hour: int = 0, minute: int = 0):
        self.current_time = datetime(year=2023, month=12, day=19, hour=hour, minute=minute)
        super().__init__(text=self.current_time.strftime("%H:%M"), start_x=position[0], start_y=position[1],
                         color=arcade.color.BLACK, font_size=25, anchor_x="left")
        self.speed = 1

        self.manager = gui.UIManager()
        self.manager.enable()
        box = gui.UIBoxLayout(vertical=False, align="center")
        plus = gui.UIFlatButton(text="+", width=self.ELEMENT_SIZE, height=self.ELEMENT_SIZE)
        plus.on_click = self.speed_up
        self.time_speed = gui.UILabel(text="x1", text_color=arcade.color.BLACK, font_size=18, width=35,
                                      height=25, font_name='times new roman')
        minus = gui.UIFlatButton(text="–", width=self.ELEMENT_SIZE, height=self.ELEMENT_SIZE)
        minus.on_click = self.speed_down
        box.add(minus.with_space_around(right=7))
        box.add(self.time_speed)
        box.add(plus.with_space_around(left=7))
        self.manager.add(gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", align_x=position[0],
                                            align_y=position[1] - 35, child=box))

    def speed_up(self, event):
        if self.speed == 64:
            return
        self.speed *= 2
        self.time_speed.text = f"x{self.speed}"

    def speed_down(self, event):
        if self.speed == 1:
            return
        self.speed //= 2
        self.time_speed.text = f"x{self.speed}"

    def draw(self):
        super().draw()
        self.manager.draw()

    def increase(self):
        self.current_time += timedelta(seconds=1 * self.speed)
        self.text = self.current_time.strftime("%H:%M")
