from datetime import date

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager

from kivymd.toast.kivytoast import kivytoast
from kivymd.uix.screen import MDScreen


import dev
from dev.view.logic import AutorizationLogic, MainScreenLogic
from dev.view.screens_helper import TabelItem
from dev.view.screens_calendar import CalendarLogic


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


class Main(MDScreen):
    '''Главный экран данных на котором расположен интерфейс пользователя.
    Через этот интерфейс можно управлять приложением
    '''
    user = StringProperty()
    today = StringProperty()

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
            screen_constructor=self.screen_constructor,
            screen_manager=self.screen_manager,
            main_screen=self,
        )

    def btn_wyloguj(self):
        "Возвращает на экран логирования"
        dev.logger.info('screens.py: class Main(MDScreen) btn_wyloguj()')
        self.screen_manager.transition.direction = 'right'
        self.screen_constructor.remove_main_screen()

    def btn_menu_dodac(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_menu_dodac()')
        pass

    def btn_menu_wyslij(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_menu_wyslij()')
        pass

    def btn_memu_tabela(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_memu_tabela()')
        pass

    def btn_menu_pytac(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_menu_pytac()')
        pass

    def btn_menu_zadania(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_menu_zadania()')
        pass

    def btn_dodac(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_dodac()')

        if self.ids.godziny.text != 'Godziny' and \
            self.ids.obiekt.text != 'Obiekt' and \
                self.ids.date.text != 'Data':

            item = TabelItem(
                text=self.ids.obiekt.text,
                on_release=self.logic.on_click_table_row,
                )
                
            item.ids.left_label.text = self.ids.godziny.text
            item.ids.right_button.text = self.ids.date.text
            item.ids.right_button.on_release = lambda widget=item.ids.right_button: self.logic.on_click_table_right_button(widget)
                
            self.ids.scroll.add_widget(item)
            self._refresh_buttons()
        else:
            pass

    def btn_godziny(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_godziny()')
        self.logic.select_godziny()

    def btn_obiekt(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_obiekt()')
        self.logic.open_objects_menu_list()

    def btn_show_calendar(self):
        dev.logger.info('screens.py: class Main(MDScreen) btn_show_calendar()')
        self.screen_constructor.add_calendar_screen_obj()

    def _refresh_buttons(self):
        # self.ids.godziny.text = 'Godziny'
        # self.ids.godziny.icon = 'hours-24'

        # self.ids.obiekt.text = 'Obiekt'
        # self.ids.obiekt.icon = 'home-lightning-bolt'

        self.ids.date.text = 'Data'
        self.ids.date.icon = 'calendar-range'


class Calendar(MDScreen):
    def __init__(self, name, screen_manager, screen_constructor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.screen_manager = screen_manager
        self.screen_constructor = screen_constructor

        self.logic = CalendarLogic(
            screen_manager = screen_manager,
            screen_constructor = screen_constructor
        )



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