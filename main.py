import os
import re

from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, DictProperty, ListProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy import utils
from kivy.base import EventLoop
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.textfield import MDTextField

from database_query import Database_query as DQ
from database import Database as DT

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

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

    # INPUTS VARS
    amount = StringProperty("0")
    data_name = StringProperty("Chagua Aina!")
    data_icon = StringProperty("exclamation")
    category = StringProperty("")
    matumizi = DictProperty(DT.exp_list(DT()))
    kipato = DictProperty(DT.inc_list(DT()))
    date = StringProperty(DT.get_date(DT()))
    date_frm = StringProperty(DT.date_format(DT()))

    # progressbar values
    percentage = StringProperty("")
    amount_per = NumericProperty(0)
    exp_perc = NumericProperty(0)

    # ACCOUNT VARS
    user_name = StringProperty("")
    passcode = StringProperty("")
    code_bool = False
    account_amount = StringProperty(DQ.account_info(DQ())[0])
    income = StringProperty(DQ.account_info(DQ())[1])
    expenses = StringProperty(DQ.account_info(DQ())[2])

    # DUMMY VARS
    dummy_cash = StringProperty("0")
    dummy_amount = StringProperty("0")

    def on_start(self):
        self.sm = self.root
        self.keyboard_hooker()
        self.backgrounds()
        Clock.schedule_once(lambda x: self.register_check(), .1)

    def backgrounds(self):
        plus_button = self.root.ids.plus
        plus_button.md_bg_color = 36 / 255, 146 / 255, 255 / 255, 1

    """
    
                ACCOUNTS FUNCTIONS!
    
    """

    def register_check(self):
        file_size = os.path.getsize("database/user.json")
        self.symbol_calc()
        if file_size == 0:
            self.sm.current = "username"
        else:
            self.sm.current = "login"

    def login_auto(self):
        cd = self.root.ids.lgn_code
        lk = self.root.ids.lock
        lg = self.root.ids.lgn
        if cd.text == DT.login(DT()):
            toast("Succes!")
            cd.password = False
            lk.icon = "lock-open-variant"
            lg.pos_hint = {'center_x': .65, 'center_y': .45}
        else:
            cd.password = True
            lk.icon = "lock"
            lg.pos_hint = {'center_x': .65, 'center_y': 2}

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
            self.database_user()
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

    def database_user(self):
        DT.user_register(DT(), self.user_name, self.passcode)

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

    """
    
    End of Screen Functions
    
    """
    """
            Down here Stays Data inputs Functions
    """

    # MY keyboard functions
    def amount_update(self, num):
        if self.amount == "0":
            self.amount = num
            self.dummy_amount = num
        else:
            if len(self.dummy_amount) < 8:
                self.dummy_amount += num
                self.amount = '{:,}'.format(int(self.dummy_amount))

    def perc_update(self):
        exp = int(self.expenses.replace(",", ""))
        acc = int(self.account_amount.replace(",", ""))
        self.exp_perc = exp
        self.amount_per = acc
        percentage = (int(exp) * 100) / int(acc)
        self.percentage = "{:.1f}".format(percentage)

    def back_space(self):
        self.dummy_amount = self.amount.replace(",", "")
        leng = len(self.dummy_amount) - 1
        self.dummy_amount = self.dummy_amount[0:leng]
        if self.dummy_amount == '':
            self.amount = "0"
        else:
            self.dummy_amount = self.dummy_amount
            self.amount = '{:,}'.format(int(self.dummy_amount))

    # The Data types and sheets

    def callback_for_menu_items(self, y, z):
        toast(y)
        self.data_name = y
        self.data_icon = z

    def category_sheet(self, data):
        bottom_sheet_menu = MDListBottomSheet()
        vimbweta = data
        count = 1
        for i in vimbweta.items():
            bottom_sheet_menu.add_item(
                i[0],
                lambda x, y=i[0], z=i[1]: self.callback_for_menu_items(y, z),
                icon=i[1],
            )
            count += 1
        bottom_sheet_menu.radius_from = 'top'
        bottom_sheet_menu.open()

    def container_maker(self):
        self.data_container(self.data_name, self.amount, self.category, self.data_icon)
        self.refresh()

    def data_container(self, name, amount, cate, icon):
        DT.data_input(DT(), name, amount, cate, icon)

    """
        End of Data Inputs Functions
    """

    """
        WEAK FUNCTIONS
    
    """

    def toasting(self):
        toast("chagua matumizi au kipato!")

    def symbol_calc(self):
        inc = self.income.replace(",", "")
        exp = self.expenses.replace(",", "")
        acc = int(inc) - int(exp)
        self.perc_update()
        if acc > 0:
            self.account_amount = f"+{self.account_amount}/="
        elif acc < 0:
            self.account_amount = f"-{self.account_amount}/="
        else:
            self.account_amount = f"{self.account_amount}/="

    def refresh(self):
        self.perc_update()
        self.account_amount = DQ.account_info(DQ())[0]
        self.income = DQ.account_info(DQ())[1]
        self.expenses = DQ.account_info(DQ())[2]
        self.symbol_calc()

    """
        END OF WEAK FUNCTIONS
    """

    """
    
        TESTING FUNCTIONS DOWN HERE
    
    """

    def test(self):
        sm = self.root
        sm.current = 'sec'

    def build(self):
        self.size_x, self.size_y = Window.size
        self.theme_cls.theme_style = "Light"
        # self.theme_cls.primary_palette = "DeepPurple"
        # self.theme_cls.accent = "Brown"
        self.size_x, self.size_y = Window.size
        self.title = "POCKET"


MainApp().run()
