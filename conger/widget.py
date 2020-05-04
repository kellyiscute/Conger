from conger.components import *
from conger import *
from conger.task_dispatcher import Process


class TaskWidget():

    def __init__(self, name: str, cmd: str, icon_path: str, color: str):
        self.cmd = cmd
        self.process: Union[None, Process] = None
        self.name = name
        self.txt_component: Text
        self.control_text_component: Text
        self.control_button_component: Button
        self.icon = icon_path
        self.color = color
        self.isRunning = False

    def _component(self):
        component = HorizontalStack((
                HorizontalStack((
                    HorizontalStack((Image(src=self.icon).width(20),))
                    .background("#00000010")
                    .height(35)
                    .width(35)
                    .justify_center()
                    .align_items_center()
                    .rounded_corner(9999),
                    txt := Text(self.name).font_color('#FFFFFF').font_size(20).margin(0, 0, 0, 10),
                )).align_items_center(),
                control_button := Button((control_text := Text('启动')
                                          .margin(0, 0, 0, 0)
                                          .font_color(self.color),))
                    .center_text()
                    .height(25)
                    .font_size(13)
                    .background("#FFFFFF")
                    .font_color('#FFFFFF')
                    .border(2, '#FFFFFF')
                    .rounded_corner(9999)
                    .on_click(self.on_start_click),
        ))  .padding(10, 10, 10, 10) \
            .background(self.color) \
            .align_items_center() \
            .justify_between() \
            .rounded_corner(10)\
            .shadow(self.color)\
            .margin(0, 0, 10, 0)

        self.txt_component = txt
        self.control_text_component = control_text
        self.control_button_component = control_button
        return component

    def create_component(self):
        return self._component()

    def exit_callback(self):
        set_background(self.control_button_component.serial, '#FFFFFF')
        set_font_color(self.control_text_component.serial, self.color)
        set_text(self.control_text_component.serial, '启动')

        self.isRunning = False

    def __call__(self, *args, **kwargs):
        return self._component()

    def on_start_click(self):
        if not self.isRunning:
            self.isRunning = True
            set_background(self.control_button_component.serial, self.color)
            set_font_color(self.control_text_component.serial, "#FFFFFF")
            self.process = Process(self.cmd, self.exit_callback)
            set_text(self.control_text_component.serial, '停止')

        else:
            self.process.kill()
