import enum


class SystemItem(enum.Enum):
    SYSTEM_ON = 'ВКЛ системы'
    SYSTEM_OFF = 'ВЫКЛ системы'
    BACKLIGHT_ON = 'ВКЛ подсветки'
    BACKLIGHT_OFF = 'ВЫКЛ подсветки'
    LIGHT_ON = 'ВКЛ света'
    LIGHT_OFF = 'ВЫКЛ света'
    SAVING_ON = 'ВКЛ сбережения'
    SAVING_OFF = 'ВЫКЛ сбережения'


class SystemState(enum.Enum):
    SYSTEM_OFF = 'Система выключена'
    SYSTEM_ON = 'Система включена'
    LIGHT = 'Свет'
    BACKLIGHT = 'Подсветка'
    ENERGY_SAVING = 'Сбережение'
    BACKLIGHT_AND_ENERGY_SAVING = 'Подсветка и сбережение'


class IlluminationState(enum.Enum):
    DARK = (0, 0, 0, 200)
    LIGHT = (0, 0, 0, 0)
    BACKLIGHT = (255, 0, 0, 55)
    SAVING = (0, 0, 0, 155)
    BACKLIGHT_AND_SAVING = (100, 0, 0, 55)


class ButtonState(enum.Enum):
    NULL = 0
    OFF = 1
    ON = 2
