from datetime import date

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp

from kivymd.toast.kivytoast import kivytoast
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBody, IRightBodyTouch
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

import dev
from dev import config
from dev.view.logic import AutorizationLogic, MainScreenLogic
from dev.view.calendar import DatePicker


class Autorization(MDScreen):
    """
    Виджет авторизации на котором просят ввести Имя и Фимилию.
    Если пользователь не зарегистрирован,
    то заводим пользователя с новыми данными

    self.name = 'authorization_screen'
    self.user_name.text - текст который был введен пользователем в строку Imie
    self.user_surname.text - Nazwisko
    self.user_authorized: bool - пользователь авторизирован (True/False)

    self.logic = AutorizationLogic()
    self.logic.seach_user_in_base() - логика принятия решений при нажатии кнопки 'Logowanie'

    """

    user_name = ObjectProperty()
    user_surname = ObjectProperty()
    user_authorized: bool = False # set in seach_user_in_base()

    def __init__(self, screen_constructor, screen_manager, **kw):
        super().__init__(**kw)
        dev.logger.info("screens.py: class Autorization(MDScreen) __init__() name = 'authorization_screen'")

        self.screen_constructor = screen_constructor # class ScreensConstructor
        self.screen_manager = screen_manager # class ScreenManager

        self.logic = AutorizationLogic(
                screen_constructor = self.screen_constructor,
                screen_manager=self.screen_manager,
                authorization_obj = self,
                )

    def set_user(self) -> None:
        """Вызов этой функции из интерфейса пользователя.
        Исходя из того, что написано в полях ввода,
        составляю представление о пользователе"""
        dev.logger.info('screens.py: class Autorization(MDScreen) set_user()')

        _login = self.user_name.text.replace(' ', '')
        _password = self.user_surname.text.replace(' ', '')

        if _login != '' and _password != '':
            dev.logger.info(f"DEBUG: Have Login and Password: '{_login}' '{_password}'")
            self.logic.login = _login
            self.logic.password = _password
            self.logic.seach_user_in_base()
        else:
            dev.logger.warning(f"DEBUG: Have NOT Login and Password: '{_login}' '{_password}'")
            pass

class MyItemList(OneLineAvatarIconListItem):
    '''Custom list item.'''
    pass

class LeftLabel(ILeftBody, MDLabel):
    '''Custom left container.'''
    pass

class RightButton(IRightBodyTouch, MDTextButton):
    '''Custom right container.'''
    pass

class Main(MDScreen):
    '''Главный экран данных на котором расположен интерфейс пользователя.
    Через этот интерфейс можно управлять приложением
    '''
    user = StringProperty()
    today = StringProperty()
    dialog = None

    def __init__(
            self,
            user_name: str,
            user_surname: str,
            screen_constructor, # class ScreensConstructor
            screen_manager: ScreenManager,
            **kw):
        dev.logger.info("screens.py: class Main(MDScreen) __init__() name = 'main_screen'")
        super().__init__(**kw)

        self.user = f'{user_name} {user_surname}'

        self.today = date.today().strftime("%d.%m.%Y")
        self.year = date.today().year # int
        self.month = date.today().month # int
        self.day = date.today().day # int

        self.screen_constructor = screen_constructor
        self.screen_manager = screen_manager

        self.logic = MainScreenLogic(
            main_screen=self,
            screen_manager=self.screen_manager,
            screen_constructor=self.screen_constructor,
        )

        self.obiekt_menu = None

    def btn_wyloguj(self):
        "Возвращает на экран логирования"
        dev.logger.info('screens.py: class Main(MDScreen) btn_wyloguj()')
        self.logic.remove_main_screen()

    def make_data_table(self):
        dev.logger.info('screens.py: class Main(MDScreen) make_data_table()')

        import random
        for i, obj in enumerate(['Renoma', 'Żarów', 'Rędzin', 'Renoma', 'Żarów', 'Rędzin',\
                  'Renoma', 'Żarów', 'Rędzin', 'Renoma', 'Żarów', 'Rędzin',\
                    'Renoma', 'Żarów', 'Rędzin', 'Renoma', 'Żarów', 'Rędzin',\
                        'Renoma', 'Żarów', 'Rędzin', 'Renoma', 'Żarów', 'Rędzin',\
                            'Renoma', 'Żarów', 'Rędzin', 'Renoma', 'Żarów', 'Rędzin',]):
            item = MyItemList(text=obj, on_release=self.on_click_table_row)
            
            h = ['8', '10', '12']
            item.ids.left_label.text = random.choice(h)
            item.ids.right_button.text = str(31 - i) + '.04'
            item.ids.right_button.on_release = lambda widget=item.ids.right_button:self.on_click_right_button(widget)
            
            self.ids.scroll.add_widget(item)

    def on_click_table_row(self, widget):
        "Функция отрабатывает по клику на строку таблицы"
        print('--- on_click_item ---')
        print('wdiget.text:', widget.text, 'left_label.text:',  widget.ids.left_label.text, 'right_button.text:',  widget.ids.right_button.text)

    def on_click_table_right_button(self, widget):
        "Функция отрабатывает по клику на дату"
        print('--- on_click_right_button ---')
        print('wdiget.text:',  widget.text)
        print('widget.parent.parent:', widget.parent.parent)
        print('widget.parent.parent.text:', widget.parent.parent.text)
    
    def show_date_picker(self):
        self.screen_constructor.show_calendar()
        self.screen_manager.current = 'calendar_screen'

    def on_save_calendar(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        if value.day <= 9:
            day = f'0{value.day}'
        else:
            day = value.day

        if value.month <= 9:
            month = f'0{value.month}'
        else:
            month = value.month

        self.ids.date_input.text = f"{day}.{month}"

    def on_cancel_calendar(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        print(instance, value)

    def open_obiekt_menu(self):
        def reaction_on_renoma():
            print('Renoma')
            self.obiekt_menu.dismiss()

        def reaction_on_zarow():
            print('Żarów')
            self.obiekt_menu.dismiss()

        def reaction_on_redzin():
            print('Rędzin')
            self.obiekt_menu.dismiss()

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "icon": "git",
                "text": f"Renoma",
                "height": dp(56),
                "on_release": lambda x=f"Renoma": reaction_on_renoma(),
            },
            {
                "viewclass": "OneLineListItem",
                "icon": "git",
                "text": f"Żarów",
                "height": dp(56),
                "on_release": lambda x=f"Żarów": reaction_on_zarow(),
            },
            {
                "viewclass": "OneLineListItem",
                "icon": "git",
                "text": f"Rędzin",
                "height": dp(56),
                "on_release": lambda x=f"Rędzin": reaction_on_redzin(),
            },
        ]

        self.obiekt_menu = MDDropdownMenu(
            caller=self.ids.obiekt,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.obiekt_menu.bind()
        self.obiekt_menu.open()

    def select_godziny(self):
        if not self.dialog:
            self.widgets = Widgets(self)
            self.dialog = MDDialog(
                type = "custom",
                content_cls = self.widgets
            )
        self.dialog.open()

class IconListItem(OneLineIconListItem):
    icon = StringProperty()


    # def send_sms(phone_number, message):
    #     sms = dev.SmsManager.getDefault()
    #     sms.sendTextMessage(phone_number, None, message, None, None)

    # def btn_tak_call(self, obj):
    #     "Пользователь нажал Да"
    #     send_sms(config.PHONE_NUMBER, 'Hello from Praca App!')
    #     kivytoast.toast('Już wysłano SMS na numer +48 577 655 470')
    #     self.screen_constructor.dilog_screen.dismiss()
    #     self.children[0].open() # MDBackdrop.open()
    #     dev.logger.info('Tak: button')

    # def btn_nie_call(self, obj):
    #     "Пользователь нажал Нет"
    #     self.screen_constructor.dilog_screen.dismiss()
    #     self.children[0].open() # MDBackdrop.open()
    #     dev.logger.info('Nie: button')

class Calendar(MDScreen):
    def __init__(self, name, screen_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.screen_manager = screen_manager

class Widgets(MDBoxLayout):
    progress = NumericProperty()

    def __init__(self, main_screen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_screen = main_screen
