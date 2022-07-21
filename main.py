import re

from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy import utils
from kivy.base import EventLoop
from kivymd.toast import toast

from kivymd.uix.textfield import MDTextField

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"

if utils.platform != 'android':
    Window.size = (412, 732)


class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnlyField, self).insert_text(s, from_undo=from_undo)


class MainApp(MDApp):
    size_x, size_y = NumericProperty(0), NumericProperty(0)
    sm = ObjectProperty()

    # screen
    screens = ["genesis"]
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    # DUMMY VARS
    dummy_cash = StringProperty("0")

    # ACCOUNT VARS
    user_name = StringProperty("")
    passcode = StringProperty("")
    code_bool = False

    def on_start(self):
        self.sm = self.root
        self.keyboard_hooker()
        self.backgrounds()

    def backgrounds(self):
        plus_button = self.root.ids.plus
        plus_button.md_bg_color = 36 / 255, 146 / 255, 255 / 255, 1

    """
    
                ACCOUNTS FUNCTIONS!
    
    """

    def passcode_verify(self, id):
        code = self.root.ids.code
        code1 = id.text
        if code.text != code1:
            code.password = True
            id.password = True
            self.code_bool = False
            return True
        elif code.text == code1:
            id.error = False
            code.password = False
            id.password = False
            self.code_bool = True
            return False

    def code_save(self):
        if self.code_bool:
            code = self.root.ids.code
            self.passcode = code.text
            self.sm.current = "genesis"
        if not self.code_bool:
            toast("Code not Match!")

    def username_verify(self, name):
        if name != "":
            self.user_name = name
            self.sm.current = "passcode"
        else:
            toast("Please enter username!")

    def cash_verify(self, cash):
        if cash == "":
            self.dummy_cash = "0"
        else:
            self.dummy_cash = cash
            self.dummy_cash = '{:,}'.format(int(self.dummy_cash))

    """

                    END OF ACCOUNTS FUNCTIONS!

        """

    """
            Down Here Stays Screen Function
    
    """

    def keyboard_hooker(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)

    """End of Screen Functions"""

    """
    
        TESTING FUNCTIONS DOWN HERE
    
    """

    def test(self):
        sm = self.root
        sm.current = 'sec'

    def build(self):
        self.size_x, self.size_y = Window.size
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent = "Brown"
        self.size_x, self.size_y = Window.size
        self.title = "POCKET"


MainApp().run()
