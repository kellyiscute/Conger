import re

import eel
from typing import Iterable, Union, List, Callable


class Component:
    def __init__(self):
        self.serial = '_0'
        self._style = 'transition: all 0.5s; '
        self.on_click_callback = None

    def height(self, height: Union[str, int]) -> 'Component':
        if isinstance(height, int):
            self._style += f'height: {height}px; '
        else:
            self._style += f'height: {height}; '
        return self

    def width(self, width: Union[str, int]) -> 'Component':
        if isinstance(width, int):
            self._style += f'width: {width}px; '
        else:
            self._style += f'width: {width}; '
        return self

    def padding(self, t: int, r: int, b: int, l: int) -> 'Component':
        self._style += f'padding: {t}px {r}px {b}px {l}px; '
        return self

    def background(self, background: str) -> 'Component':
        self._style += f'background: {background}; '
        return self

    def font_color(self, color: str) -> 'Component':
        self._style += f'color: {color}; '
        return self

    def border(self, width: int, color: str) -> 'Component':
        self._style += f'border: solid {width}px {color}; '
        return self

    def margin(self, t: int, r: int, b: int, l: int):
        self._style += f'margin: {t}px {r}px {b}px {l}px; '
        return self

    def center_text(self):
        self._style += f'text-align: center; '
        return self

    def font_size(self, size: int):
        self._style += f'font-size: {size}px; '
        return self

    def shadow(self, color: str):
        self._style += f'box-shadow: 0px 5px 6px {color}4f; '
        return self

    def rounded_corner(self, size: int):
        self._style += f'border-radius: {size}px; '
        return self

    def on_click(self, callback: Callable) -> 'Component':
        self.on_click_callback = callback

        return self

    def html(self):
        raise NotImplementedError



class Container(Component):
    def __init__(self, children: Union[Iterable, None]):
        super().__init__()
        self.children: Iterable[Component] = children if children is not None else []

    def html(self):
        print(self.serial)
        body = ''
        c = tuple(self.children)
        for i in range(c.__len__()):
            child = tuple(c)[i]
            child.serial = self.serial + '_' + str(i)
            if child.on_click_callback is not None:
                eel._expose(child.serial + 'click', child.on_click_callback)
            body += child.html()
        return body

    def justify_center(self):
        self._style += 'justify-content: center; '
        return self

    def justify_between(self):
        self._style += 'justify-content: space-between; '
        return self

    def justify_end(self):
        self._style += 'justify-content: end; '
        return self

    def align_items_center(self):
        self._style += 'align-items: center; '
        return self

class Root(Container):
    def __init__(self, title: str = '', children: Union[Iterable[Component], None] = None):
        super().__init__(children)
        self.children: List[Component] = children if children is not None else []
        self.title = title

    def html(self):
        body = super().html()
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script type="text/javascript" src="/eel.js"></script>
    <title>{self.title}</title>
    <script>
        eel.expose(get_input_text);
        eel.expose(set_input_text);
        eel.expose(set_image_src);
        eel.expose(set_p_text);
        eel.expose(set_background);
        eel.expose(set_text_color);
        function get_input_text(id){' {'}
            return document.getElementById(id).value
        {'}'}
        function set_input_text(id, value){' {'}
            document.getElementById(id).value = value
        {'}'}
        function set_image_src(id, value) {' {'}
            document.getElementById(id).src = value
        {'}'}
        function set_p_text(id, value) {' {'}
            document.getElementById(id).innerHTML = value
        {'}'}
        function set_background(id, value) {' {'}
            document.getElementById(id).style.background = value
        {'}'}
        function set_text_color(id, value) {' {'}
            document.getElementById(id).style.color = value
        {'}'}
    </script>
</head>
<body style='{self._style}'>
{body}
</body>
</html>
"""
        return html


class Stack(Container):
    def html(self):
        body = super().html()
        html = f"<div style='{self._style}' onClick='eel.{self.serial}click()'>\n{body}\n</div>\n"
        return html

    def __init__(self, children: Union[Iterable[Component], None]):
        super().__init__(children)
        self._style = ''


class HorizontalStack(Stack):
    def __init__(self, children: Union[Iterable[Component], None] = None):
        super().__init__(children)
        self._style = 'display: flex; '


class VerticalStack(Stack):
    def __init__(self, children: Union[Iterable, None] = None):
        super().__init__(children)


class Button(Container):
    def html(self):
        body = super().html()
        html = f'<Button id="{self.serial}" style="{self._style}user-select: none; outline: none;" onClick="eel.{self.serial}click()">{body}</Button>'
        return html

    def __init__(self, children: Union[Iterable[Component], None] = None):
        super().__init__(children)
        self._style = ''


class Input(Component):
    def html(self):
        if self._on_change_callback is not None:
            eel._expose(self.serial + 'change', self._on_change_callback)
        if self._on_keydown_callback is not None:
            eel._expose(self.serial + 'keydown', self._on_keydown_callback)
        html = f'<input id="{self.serial}" style="{self._style}" ' \
               f'placeholder="{self.place_holder_value}" value="{self.default_value}"' \
               f' onchange="eel.{self.serial}change(this.value)" onClick="eel.{self.serial}click()" onkeydown="eel.{self.serial}keydown()">'
        return html

    def __init__(self, place_holder: str = '', default: str = ''):
        super().__init__()
        self.place_holder_value = place_holder
        self.default_value = default
        self._on_change_callback = None
        self._on_keydown_callback = None

    def place_holder(self, s: str) -> 'Input':
        self.place_holder_value = s
        return self

    def set_default_value(self, s: str) -> 'Input':
        self.default_value = s
        return self

    def on_change(self, callback: Callable) -> 'Input':
        self._on_change_callback = callback

        return self

    def on_keydown(self, callback: Callable) -> 'Input':
        self._on_keydown_callback = callback

        return self

    def get_serial(self, serial: list) -> 'Input':
        serial.append(self.serial)
        return self


class Text(Component):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def html(self):
        html = f'<p id="{self.serial}" onClick="eel.{self.serial}click()" style="{self._style}">{self.text}</p>'
        return html

    def font_size(self, size: int):
        self._style += f'font-size: {size}px; '
        return self


class Image(Component):
    def html(self):
        html = f'<img id="{self.serial}" onClick="eel.{self.serial}click()" src="{self.src}" style="{self._style}"/>'
        return html

    def __init__(self, src: str):
        super().__init__()
        self.src = src

    def src(self, src: str):
        self.src = src


def style(stylesheet: str, override=True):
    with open(stylesheet, 'r') as ss:
        stylesheet = ss.read()
    css_pattern = re.compile(r'(^.[A-Za-z\-_0-9]*)(\s*:\s*([A-z]*))?\s*{($[^}]*)}$', flags=re.RegexFlag.MULTILINE)
    line_pattern = re.compile(r'[A-Za-z\-]*\s*:\s*[^;]*;$', flags=re.RegexFlag.MULTILINE)
    css_content = css_pattern.search(stylesheet).group(4)
    lines = line_pattern.findall(css_content)
    inline = ' '.join(lines)

    def decorator(f: Callable[[], Component]):
        component = f()
        if override:
            component._style += inline
        else:
            component._style = inline
        return lambda: component
    return decorator
