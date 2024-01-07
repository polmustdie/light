from datetime import timedelta

import arcade
from arcade import gui
from arcade.gui import UILabel, UIManager, UIInputText, UITextArea

from elements import Timer, Illumination, SystemPanel
from enums import SystemState, IlluminationState, ButtonState

SIZE_COEFFICIENT = 1.6
SCREEN_WIDTH = int(620 * SIZE_COEFFICIENT)
SCREEN_HEIGHT = int(465 * SIZE_COEFFICIENT)


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, center_window=True, title="Управление светом")

        self.background = None
        self.timer = Timer((SCREEN_WIDTH + 55, SCREEN_HEIGHT - 40), hour=7)
        self.illumination_item = Illumination(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                              size=(SCREEN_WIDTH, SCREEN_HEIGHT))

        self.manager = UIManager()
        self.manager.enable()
        box = gui.UIBoxLayout(vertical=True, align='center')
        self.state_label = UITextArea(text="Состояние:", text_color=arcade.color.BLACK, font_size=18,
                                      width=140, height=80, font_name='times new roman')
        box.add(self.state_label.with_space_around(bottom=30))
        box.add(UILabel(text="Освещённость:", text_color=arcade.color.BLACK, font_size=18, width=175, height=25,
                        font_name='times new roman', align='center'))
        line = gui.UIBoxLayout(vertical=False, align='center')
        line.add(UILabel(text="%:", text_color=arcade.color.BLACK, font_size=18, width=25, height=25,
                         font_name='times new roman', align='center').with_space_around(right=7))
        self.illumination = UIInputText(width=50, height=28, text_color=arcade.color.BLACK, font_size=18,
                                        font_name='times new roman')
        self.illumination.text = '100'
        line.add(self.illumination.with_background(texture=arcade.load_texture("images/illumination_background.jpg")))
        box.add(line.with_space_around(bottom=30))
        box.add(UILabel(text="Настроение:", text_color=arcade.color.BLACK, font_size=18, width=175, height=25,
                        font_name='times new roman', align='center').with_space_around(bottom=5))
        mood_button = gui.UIFlatButton(text="Обычное", width=100, height=30)
        mood_button.on_click = self.change_mood
        self.good_mood = False
        box.add(mood_button)
        self.manager.add(gui.UIAnchorWidget(anchor_x="left", anchor_y="bottom", align_x=SCREEN_WIDTH + 10,
                                            align_y=SCREEN_HEIGHT - 350, child=box))
        self.illumination_value = '100'

        self.system_panel = SystemPanel(position=(SCREEN_WIDTH + 10, 50))
        self.drag_mode = False

        self.state = SystemState.SYSTEM_OFF

    def change_mood(self, event):
        self.good_mood = not self.good_mood
        event.source.text = 'Хорошее' if self.good_mood else 'Обычное'

    def setup(self):
        self.background = arcade.load_texture("images/room.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_rectangle_filled(SCREEN_WIDTH + 100, SCREEN_HEIGHT // 2, 200, SCREEN_HEIGHT,
                                     arcade.color.LIGHT_GRAY)
        self.timer.draw()
        self.manager.draw()
        self.illumination_item.draw()
        self.system_panel.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.drag_mode = not self.drag_mode

    def illumination_is_low(self):
        if self.illumination_value == '':
            return True
        return int(self.illumination_value) < 50

    def update(self, delta_time):
        self.timer.increase()
        if self.illumination.text != self.illumination_value:
            if self.illumination.text != "":
                try:
                    if not 0 <= int(self.illumination.text) <= 100:
                        raise ValueError
                except ValueError:
                    self.illumination.text = "100"
            self.illumination_value = self.illumination.text
        if self.state == SystemState.SYSTEM_OFF:
            if self.system_panel.system == ButtonState.ON:
                self.system_panel.light = self.system_panel.backlight = self.system_panel.saving = ButtonState.NULL
                self.state = SystemState.SYSTEM_ON
        elif self.state == SystemState.SYSTEM_ON:
            if self.system_panel.system == ButtonState.OFF:
                self.state = SystemState.SYSTEM_OFF
            elif self.system_panel.backlight == ButtonState.ON or self.system_panel.backlight == ButtonState.NULL and \
                    (self.good_mood or (self.timer.current_time.hour == 23 or self.timer.current_time.hour < 7) and
                     self.drag_mode):
                self.system_panel.saving = self.system_panel.light = ButtonState.NULL
                self.illumination_item.light = IlluminationState.BACKLIGHT
                self.state = SystemState.BACKLIGHT
            elif self.system_panel.light == ButtonState.ON or self.system_panel.light == ButtonState.NULL and \
                    self.drag_mode and self.illumination_is_low():
                self.system_panel.backlight = self.system_panel.saving = ButtonState.NULL
                self.illumination_item.light = IlluminationState.LIGHT
                self.state = SystemState.LIGHT
            elif self.system_panel.saving == ButtonState.ON or self.system_panel.saving == ButtonState.NULL and \
                    (self.drag_mode and not self.illumination_is_low() or self.timer.current_time.hour == 7):
                self.system_panel.backlight = self.system_panel.light = ButtonState.NULL
                self.illumination_item.light = IlluminationState.SAVING
                self.state = SystemState.ENERGY_SAVING
        elif self.state == SystemState.LIGHT:
            if self.system_panel.system == ButtonState.OFF:
                self.illumination_item.light = IlluminationState.DARK
                self.state = SystemState.SYSTEM_OFF
            elif self.system_panel.light == ButtonState.OFF or self.system_panel.light == ButtonState.NULL and \
                    not self.drag_mode:
                self.illumination_item.light = IlluminationState.DARK
                self.state = SystemState.SYSTEM_ON
            elif self.system_panel.saving == ButtonState.ON or self.system_panel.saving == ButtonState.NULL and \
                    self.drag_mode and not self.illumination_is_low():
                self.system_panel.backlight = self.system_panel.light = ButtonState.NULL
                self.illumination_item.light = IlluminationState.SAVING
                self.state = SystemState.ENERGY_SAVING
        elif self.state == SystemState.BACKLIGHT:
            if self.system_panel.system == ButtonState.OFF:
                self.illumination_item.light = IlluminationState.DARK
                self.state = SystemState.SYSTEM_OFF
            elif self.system_panel.backlight == ButtonState.OFF or self.system_panel.backlight == ButtonState.NULL and \
                    (not self.good_mood and not ((self.timer.current_time.hour == 23 or
                                                  self.timer.current_time.hour < 7) and self.drag_mode) or
                     (self.timer.current_time.hour == 23 or self.timer.current_time.hour < 7) and not self.drag_mode):
                self.illumination_item.light = IlluminationState.DARK
                self.state = SystemState.SYSTEM_ON
            elif self.system_panel.light == ButtonState.ON:
                self.system_panel.saving = ButtonState.NULL
                self.illumination_item.light = IlluminationState.LIGHT
                self.state = SystemState.LIGHT
            elif self.system_panel.saving == ButtonState.ON:
                self.system_panel.light = ButtonState.NULL
                self.illumination_item.light = IlluminationState.BACKLIGHT_AND_SAVING
                self.state = SystemState.BACKLIGHT_AND_ENERGY_SAVING
        elif self.state == SystemState.ENERGY_SAVING:
            if self.system_panel.system == ButtonState.OFF:
                self.illumination_item.light = IlluminationState.DARK
                self.state = SystemState.SYSTEM_OFF
            elif self.system_panel.saving == ButtonState.OFF or self.system_panel.saving == ButtonState.NULL and not \
                    self.drag_mode and self.timer.current_time.hour != 7:
                self.illumination_item.light = IlluminationState.DARK
                self.state = SystemState.SYSTEM_ON
            elif self.system_panel.light == ButtonState.ON or self.system_panel.light == ButtonState.NULL and \
                    self.drag_mode and self.illumination_is_low():
                self.system_panel.backlight = self.system_panel.saving = ButtonState.NULL
                self.illumination_item.light = IlluminationState.LIGHT
                self.state = SystemState.LIGHT
            elif self.system_panel.backlight == ButtonState.ON or self.system_panel.backlight == ButtonState.NULL and \
                    self.good_mood:
                self.system_panel.light = ButtonState.NULL
                self.illumination_item.light = IlluminationState.BACKLIGHT_AND_SAVING
                self.state = SystemState.BACKLIGHT_AND_ENERGY_SAVING
        else:
            if self.system_panel.system == ButtonState.OFF:
                self.illumination_item.light = IlluminationState.DARK
                self.state = SystemState.SYSTEM_OFF
            elif self.system_panel.saving == ButtonState.OFF:
                self.system_panel.light = ButtonState.NULL
                self.illumination_item.light = IlluminationState.BACKLIGHT
                self.state = SystemState.BACKLIGHT
            elif self.system_panel.backlight == ButtonState.OFF or self.system_panel.backlight == ButtonState.NULL \
                    and not self.good_mood:
                self.system_panel.light = ButtonState.NULL
                self.illumination_item.light = IlluminationState.SAVING
                self.state = SystemState.ENERGY_SAVING
        self.state_label.text = f'Состояние:\n{self.state.value}'


if __name__ == "__main__":
    game = MyGame(SCREEN_WIDTH + 200, SCREEN_HEIGHT)
    game.setup()
    arcade.run()
