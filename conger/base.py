from typing import Union, Callable, Iterable
import eel


class BaseComponent:
    def __init__(self):
        self.serial = '_0'
        self._style = 'transition: all 0.5s; '
        self.on_click_callback = None

    def height(self, height: Union[str, int]) -> 'BaseComponent':
        if isinstance(height, int):
            self._style += f'height: {height}px; '
        else:
            self._style += f'height: {height}; '
        return self

    def width(self, width: Union[str, int]) -> 'BaseComponent':
        if isinstance(width, int):
            self._style += f'width: {width}px; '
        else:
            self._style += f'width: {width}; '
        return self

    def padding(self, t: int, r: int, b: int, l: int) -> 'BaseComponent':
        self._style += f'padding: {t}px {r}px {b}px {l}px; '
        return self

    def background(self, background: str) -> 'BaseComponent':
        self._style += f'background: {background}; '
        return self

    def font_color(self, color: str) -> 'BaseComponent':
        self._style += f'color: {color}; '
        return self

    def border(self, width: int, color: str) -> 'BaseComponent':
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

    def on_click(self, callback: Callable) -> 'BaseComponent':
        self.on_click_callback = callback

        return self

    def html(self):
        raise NotImplementedError


class BaseContainer(BaseComponent):
    def __init__(self, children: Union[Iterable, None]):
        super().__init__()
        self.children: Iterable[BaseComponent] = children if children is not None else []

    def html(self):
        print(self.serial)
        body = ''
        if self.children is None:
            return body
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
