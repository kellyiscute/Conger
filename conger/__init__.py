from .Components import *
import eel

def get_input_value(serial: str):
    return eel.get_input_text(serial)()


def set_input_value(serial: str, text: str):
    return eel.set_input_text(serial, text)


def set_text(serial: str, text: str):
    eel.set_p_text(serial, text)


def set_image_src(serial: str, src: str):
    eel.set_image_src(serial, src)


def init(component: Component):
    html = component.html()
    with open('main.html', 'w') as f:
        f.write(html)
    print(html)
    eel.init('')


def start():
    eel.start('main.html')
