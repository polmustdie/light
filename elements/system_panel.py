from typing import Tuple

import arcade
from arcade import gui

from enums import SystemItem, ButtonState


class SystemPanel(gui.UIManager):
    BUTTON_HEIGHT = 30
    BUTTON_WIDTH = 180

    def __init__(self, position: Tuple[float, float]):
        super().__init__()
        self.enable()
        box = gui.UIBoxLayout(vertical=True, align='center', space_between=10)
        on_button_style = dict(font_color=arcade.color.BLACK, font_name='times new roman', bg_color=(32, 241, 51))
        off_button_style = dict(font_color=arcade.color.BLACK, font_name='times new roman', bg_color=(251, 51, 32))
        self.elements = {}
        for item in SystemItem:
            element = gui.UIFlatButton(text=item.value, width=self.BUTTON_WIDTH, height=self.BUTTON_HEIGHT,
                                       style=off_button_style if item.value.find('ВКЛ') == -1 else on_button_style)
            element.on_click = self.click_element
            box.add(element)
            self.elements[item] = element
        self.add(gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", align_x=position[0], align_y=position[1],
                                    child=box))

        self.system = ButtonState.NULL
        self.backlight = ButtonState.NULL
        self.light = ButtonState.NULL
        self.saving = ButtonState.NULL

    def click_element(self, event):
        if event.source.text.find('ВКЛ') != -1:
            if event.source.text == SystemItem.SYSTEM_ON.value:
                self.system = ButtonState.ON
            elif event.source.text == SystemItem.BACKLIGHT_ON.value:
                self.backlight = ButtonState.ON
            elif event.source.text == SystemItem.LIGHT_ON.value:
                self.light = ButtonState.ON
            else:
                self.saving = ButtonState.ON
        else:
            if event.source.text == SystemItem.SYSTEM_OFF.value:
                self.system = ButtonState.OFF
            elif event.source.text == SystemItem.BACKLIGHT_OFF.value:
                self.backlight = ButtonState.OFF
            elif event.source.text == SystemItem.LIGHT_OFF.value:
                self.light = ButtonState.OFF
            else:
                self.saving = ButtonState.OFF
