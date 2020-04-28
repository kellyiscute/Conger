from .Components import *
import eel

def get_input_value(serial: str):
    return eel.get_input_text(serial)()


def set_input_value(serial: str, text: str):
    return eel.set_input_text(serial, text)


def init(component: Component):
    html = component.html()
    with open('main.html', 'w') as f:
        f.write(html)
    print(html)
    eel.init('')


def start():
    eel.start('main.html')
