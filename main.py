import os
import re
import threading

from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, DictProperty, ListProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy import utils
from kivy.base import EventLoop
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from database_query import Database_query as DQ
from database import Database as DT

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = (412, 732)


class More(MDCard):
    icon = StringProperty("")


class WalletsInputs(MDBoxLayout):
    pass


class Wallet(MDDialog):
    name = StringProperty("")
    color = ListProperty([])
    amount = StringProperty("")


class RowCard(MDCard):
    date = StringProperty("")
    icon = StringProperty("")
    cate = StringProperty("")
    name = StringProperty("")
    price = StringProperty("")

    def price_symb(self, cat, prc):
        if cat == "expenses":
            self.price = "-" + prc + "/="
        else:
            self.price = "+" + prc + "/="
        return self.price


class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    input_type = "number"

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

    # dialog
    wallet_inpt = None

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
    td_exp = StringProperty("0")
    td_inc = StringProperty("0")

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

    # Mobile Wallets
    wallets = ListProperty([DQ.mobile_wallets(DQ())])
    mpesa = StringProperty("0")
    airtel = StringProperty("0")
    tigo = StringProperty("0")
    halotel = StringProperty("0")

    # DUMMY VARS
    dummy_cash = StringProperty("0")
    dummy_amount = StringProperty("0")
    dummy_account_amount = StringProperty("0")

    def on_start(self):
        self.sm = self.root
        self.keyboard_hooker()
        self.backgrounds()
        kbd = self.root.ids.lgn_code
        kbd.input_type = "number"
        Clock.schedule_once(lambda x: self.register_check(), .1)

    def backgrounds(self):
        plus_button = self.root.ids.plus
        plus_button.md_bg_color = 36 / 255, 146 / 255, 255 / 255, 1

    """
    
                ACCOUNTS FUNCTIONS!
    
    """

    def register_check(self):
        file_size = os.path.getsize("database/user.json")
        if file_size == 0:
            self.sm.current = "username"
        else:
            self.sm.current = "login"
            Clock.schedule_once(lambda x: self.add_item(), 2)

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
                    DATA VIEW FUNCTION
    """

    # small vars
    counter = 0
    count = 0

    def today_exp_inc(self):
        if DT.today_total(DT()):
            exp_temp, inc_temp = DT.today_total(DT())
            self.td_exp = '{:,}'.format(int(exp_temp))
            self.td_inc = '{:,}'.format(int(inc_temp))

    def add_item(self):
        self.symbol_calc()
        main = DT.load_today(DT())
        if main:
            self.today_exp_inc()
            for i, y in main.items():
                if self.counter < 9:
                    self.root.ids.customers.data.append(
                        {
                            "viewclass": "RowCard",
                            "icon": y["icon"],
                            "name": y["name"],
                            "cate": y["category"],
                            "date": y["date"],
                            "price": RowCard.price_symb(RowCard(), y["category"], y["amount"]),
                            "id": i
                        }
                    )
                else:
                    if self.count == 0:
                        self.root.ids.customers.data.append(
                            {
                                "viewclass": "More",
                                "icon": "dots-horizontal"
                            }
                        )
                        self.count = + 1
                self.counter = self.counter + 1
        else:
            img = self.root.ids.nodata
            img.source = "components/icons/file-plus.jpg"

    data_count = 0

    def update_items(self):
        datas = self.root.ids.customers.data
        datas_size = len(datas)
        if datas_size >= 9:
            print("fuck you")
            if self.data_count == 0:
                self.root.ids.customers.data.append(
                    {
                        "viewclass": "More",
                        "icon": "dots-horizontal"
                    }
                )
                self.data_count = + 1
        else:
            try:
                self.update_item()
            except:
                pass

    def update_item(self):
        self.root.ids.customers.data.append(
            {
                "viewclass": "RowCard",
                "icon": self.data_icon,
                "name": self.data_name,
                "cate": self.category,
                "price": RowCard.price_symb(RowCard(), self.category, self.amount)
            }
        )

    """
                    END OF DATA VIEW FUNCTION
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
        print(self.data_name, self.amount, self.category, self.data_icon)
        if self.data_name != "Chagua Aina!" and self.amount != "0" and self.category != "" and self.data_icon != "exclamation":
            self.data_container(self.data_name, self.amount, self.category, self.data_icon)
            self.screen_leave()
            img = self.root.ids.nodata
            img.source = ""
        else:
            toast("Please dont fuck around!")

    def data_container(self, name, amount, cate, icon):
        DT.data_input(DT(), name, amount, cate, icon)
        self.update_items()
        self.refresh()

    def spin_dialog(self):
        if not self.wallet_inpt:
            self.wallet_inpt = MDDialog(
                type="custom",
                auto_dismiss=False,
                size_hint=(.6, None),
                content_cls=WalletsInputs(),
            )
        self.wallet_inpt.open()

    # WALLETS VARIABLES SPECIAL
    wallet_name = StringProperty("")
    wallet_color = ListProperty([])
    w_amount = StringProperty("")

    def phone_verfy_dialog(self):
        self.wallet_inpt = Wallet(
            title=f"Enter {self.wallet_name} amount",
            name=f"{self.wallet_name} Amount",
            color=self.wallet_color,
            buttons=[
                MDFlatButton(
                    text="Cancel", theme_text_color="Custom", text_color=self.wallet_color,
                    on_release=lambda x: self.wallet_inpt.dismiss()
                ),
                MDRaisedButton(
                    text="Submit", md_bg_color=self.wallet_color,
                    on_release=lambda x: self.update_wallet_amount(self.w_amount)
                ),
            ],
        )

        self.wallet_inpt.open()

    def update_wallet_amount(self, amount):
        self.wallet_inpt.dismiss()
        if self.wallet_name == "Mpesa":
            DT.update_wallet(DT(), "voda", amount)
            self.wallets_amount()
        if self.wallet_name == "Tigopesa":
            DT.update_wallet(DT(), "tigo", amount)
            self.wallets_amount()
        if self.wallet_name == "Halotel":
            DT.update_wallet(DT(), "halotel", amount)
            self.wallets_amount()
        if self.wallet_name == "Airtel":
            DT.update_wallet(DT(), "airtel", amount)
            self.wallets_amount()

    """
        End of Data Inputs Functions
    """

    """
        WEAK FUNCTIONS
    
    """

    def toasting(self):
        toast("chagua matumizi au kipato!")

    def wallets_amount(self):
        self.wallets = [DQ.mobile_wallets(DQ())]
        self.airtel = str(self.wallets[0][0])
        self.mpesa = self.wallets[0][1]
        self.tigo = self.wallets[0][2]
        self.halotel = self.wallets[0][3]

    def symbol_calc(self):
        inc = self.income.replace(",", "")
        exp = self.expenses.replace(",", "")
        acc = int(inc) - int(exp)
        self.perc_update()
        self.wallets_amount()
        if acc > 0:
            self.dummy_account_amount = f"+{self.account_amount}/="
        elif acc < 0:
            self.dummy_account_amount = f"-{self.account_amount}/="
        else:
            self.dummy_account_amount = f"{self.account_amount}/="

    def refresh(self):
        self.perc_update()
        self.account_amount = DQ.account_info(DQ())[0]
        self.income = DQ.account_info(DQ())[1]
        self.expenses = DQ.account_info(DQ())[2]
        self.today_exp_inc()
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
