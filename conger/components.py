import re

import eel
from typing import Iterable, Union, List, Callable
from conger import BaseComponent
from conger.base import BaseContainer


class Root(BaseContainer):
    def __init__(self, title: str = 'Conger', children: Union[Iterable[BaseComponent], None] = None):
        super().__init__(children)
        self.children: List[BaseComponent] = children if children is not None else []
        self.title = title

    def html(self):
        body = super().html()
        html = f"""<!DOCTYPE html>
<html lang="zh-cn">
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


class Container(BaseContainer):
    def html(self):
        body = super().html()
        html = f"<div style='{self._style}' onClick='eel.{self.serial}click()'>\n{body}\n</div>\n"
        return html

    def __init__(self, children: Union[Iterable[BaseComponent], None]):
        super().__init__(children)


class HorizontalStack(Container):
    def __init__(self, children: Union[Iterable[BaseComponent], None] = None):
        super().__init__(children)
        self._style = 'display: flex; '


class VerticalStack(Container):
    def __init__(self, children: Union[Iterable, None] = None):
        super().__init__(children)


class Button(BaseContainer):
    def html(self):
        body = super().html()
        html = f'<Button id="{self.serial}" style="{self._style}user-select: none; outline: none;" onClick="eel.{self.serial}click()">{body}</Button>'
        return html

    def __init__(self, children: Union[Iterable[BaseComponent], None] = None):
        super().__init__(children)


class Input(BaseComponent):
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


class Text(BaseComponent):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def html(self):
        html = f'<p id="{self.serial}" onClick="eel.{self.serial}click()" style="{self._style}">{self.text}</p>'
        return html

    def font_size(self, size: int):
        self._style += f'font-size: {size}px; '
        return self


class Image(BaseComponent):
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

    def decorator(f: Callable[[], BaseComponent]):
        component = f()
        if override:
            component._style += inline
        else:
            component._style = inline
        return lambda: component
    return decorator
