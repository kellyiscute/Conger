from .components import *
import eel

def get_input_value(serial: str):
    return eel.get_input_text(serial)()


def set_input_value(serial: str, text: str):
    return eel.set_input_text(serial, text)


def set_text(serial: str, text: str):
    eel.set_p_text(serial, text)


def set_image_src(serial: str, src: str):
    eel.set_image_src(serial, src)


def set_background(serial: str, color: str):
    eel.set_background(serial, color)


def set_font_color(serial: str, color: str):
    eel.set_text_color(serial, color)


def init(component: Component):
    html = component.html()
    with open('main.html', 'w') as f:
        f.write(html)
    print(html)
    eel.init('')


def start():
    eel.start('main.html')
