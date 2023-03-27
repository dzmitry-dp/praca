from datetime import date

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager

from kivymd.toast.kivytoast import kivytoast
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.bottomsheet import MDGridBottomSheet

import dev
from dev import send_sms
from dev import config
from dev.view.logic import AutorizationLogic, MainScreenLogic


class Autorization(MDScreen):
    """
    Виджет на котором просят ввести Имя и Фимилию.
    Если пользователь не зарегистрирован,
    то заводим пользователя с новыми данными

    self.user_name.text - текст который был введен пользователем в строку Imie
    self.user_surname.text - Nazwisko

    logic = AutorizationLogic()
    logic.seach_user_in_base() - логика принятия решений при нажатии кнопки 'Logowanie do Pracy'

    """

    user_name = ObjectProperty()
    user_surname = ObjectProperty()
    user_authorized: bool = False # set in seach_user_in_base()

    def __init__(self, screen_constructor, screen_manager, **kw):
        super().__init__(**kw)
        dev.logger.info("class Autorization(MDScreen): __init__() name = 'screen_zero'")

        self.screen_constructor = screen_constructor # class ScreensConstructor
        self.screen_manager = screen_manager # class ScreenManager

        self.logic = AutorizationLogic(
                screen_constructor = self.screen_constructor,
                screen_manager=self.screen_manager,
                authorization_obj = self,
                )


    def set_user(self) -> None:
        """Вызов функции из интерфейса пользователя. 
        Исходя из того, что написано в полях ввода, 
        составляю представление о пользователе"""
        dev.logger.info('class Autorization(MDScreen): set_user()')

        _login = self.user_name.text.replace(' ', '')
        _password = self.user_surname.text.replace(' ', '')

        if _login != '' and _password != '':
            dev.logger.info(f'Have Login and Password: {_login} {_password}')
            self.logic.login = _login
            self.logic.password = _password
            self.logic.seach_user_in_base()
        else:
            dev.logger.info(f"Login and Password: '{_login}' '{_password}'")
            pass


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
        dev.logger.info("class Main(MDScreen): __init__() name = 'screen_one'")
        super().__init__(**kw)

        self.user = f'{user_name} {user_surname}'
        self.today = date.today().strftime("%d.%m.%Y")
        self.screen_constructor = screen_constructor
        self.screen_manager = screen_manager

        self.logic = MainScreenLogic(
            main_screen=self,
            screen_manager=self.screen_manager,
            screen_constructor=self.screen_constructor,
        )
        

    def btn_wyloguj(self):
        "Возвращает на экран логирования"
        dev.logger.info('< Wyloguj: button')
        self.screen_constructor.remove_screen_one()

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

    def show_menu_btn_sheet(self):
        pass


class AddHours(MDScreen):
    pass
