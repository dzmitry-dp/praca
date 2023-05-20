from datetime import date, datetime
import threading
import os

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager

# from kivymd.toast.kivytoast import kivytoast
from kivymd.uix.screen import MDScreen

import dev.config as config
import dev.action as action
import dev.db.memory as memory
from dev.action.logic import AutorizationLogic, MainScreenLogic
# from dev.view.helpers import TabelItem
from dev.view.calendar import CalendarLogic
from dev.action.hash import hash_to_user_name


class Autorization(MDScreen):
    """
    # Виджет авторизации на котором просят ввести Имя и Фимилию.
    Если пользователь не зарегистрирован, то заводим пользователя со стандартыми начальными данными

    self.user_name.text - текст который был введен пользователем в строку Imie

    self.user_surname.text - текст который был введен пользователем в строку Nazwisko


    self.screen_constructor: объект dev.build.ScreensConstructor()для сборки и удаления экранов приложения

    self.screen_manager: объект kivy.uix.screenmanager.ScreenManager() который контролирует экраны и память

    self.logic = AutorizationLogic()
    """

    user_name = ObjectProperty()
    user_surname = ObjectProperty()

    def __init__(self, screen_constructor, screen_manager: ScreenManager, **kw):
        super().__init__(**kw)
        action.logger.info("screens.py: class Autorization(MDScreen) __init__() name = 'authorization_screen'")

        self._screen_constructor = screen_constructor # class ScreensConstructor
        self._screen_manager: ScreenManager = screen_manager # class ScreenManager
        self._logic: AutorizationLogic = None # class AutorizationLogic

        self.remember_me = True # изначально стоит галочка Remember me

    @property
    def screen_constructor(self):
        return self._screen_constructor
    
    @screen_constructor.setter
    def screen_constructor(self, value):
        self._screen_constructor = value

    @property
    def screen_manager(self) -> ScreenManager:
        return self._screen_manager
    
    @screen_manager.setter
    def screen_manager(self, value: ScreenManager):
        self._screen_manager = value
        
    @property
    def logic(self) -> AutorizationLogic:
        if self._logic is None:
            self._logic = AutorizationLogic(
                screen_constructor = self.screen_constructor,
                screen_manager=self.screen_manager,
                authorization_obj = self,
                )
        return self._logic
    
    @logic.setter
    def logic(self, value: AutorizationLogic):
        self._logic = value

    def checkbox_remember_me(self, value) -> None:
        "Галочка 'запомнить меня'"
        action.logger.info('screens.py: class Autorization(MDScreen) checkbox_remember_me()')
        self.remember_me = value
        action.logger.info(f'DEBUG: self._remember_me = {self.remember_me}')
    
    def btn_logowanie(self) -> None:
        "Кнопка 'Logowanie'"
        action.logger.info('screens.py: class Autorization(MDScreen) btn_logowanie()')
        ### Отдельным потоком отправляемся искать данные о пользователе
        set_user_thread = threading.Thread(
            name='set_user_thread',
            target=self.logic.check_user,
            args=[self.remember_me, ],
            daemon=True,
            )
        set_user_thread.start()
        ### Отдельный поток позволяет сменить экран до окончания всех расчетов


class Main(MDScreen):
    '''
    # Главный экран на котором расположен интерфейс пользователя.
    
    ## Через этот интерфейс можно управлять приложением

    user: str - имя и фамилия пользователя

    today: str - текущая дата
    '''

    user = StringProperty()
    today = StringProperty()

    def __init__(self, user_name: str, user_surname: str, screen_constructor, screen_manager: ScreenManager, **kw):
        action.logger.info("screens.py: class Main(MDScreen) __init__() name = 'main_screen'")
        super().__init__(**kw)

        self._screen_constructor = screen_constructor
        self._screen_manager = screen_manager
        self._logic: MainScreenLogic = None

        self.user_name = user_name
        self.user_surname = user_surname
        self.user_hash = hash_to_user_name(f'{self.user_name}{self.user_surname}', config.PORT)

        self.user = f'{self.user_name} {self.user_surname}'
        self.today = date.today().strftime("%d.%m.%Y")

        self.sum_godziny = 0 # Начальная сумма наработанных часов

        self.year = date.today().year # int
        self.month = date.today().month # int
        self.day = date.today().day # int


    @property
    def screen_constructor(self):
        return self._screen_constructor
    
    @screen_constructor.setter
    def screen_constructor(self, value):
        self._screen_constructor = value

    @property
    def screen_manager(self) -> ScreenManager:
        return self._screen_manager
    
    @screen_manager.setter
    def screen_manager(self, value: ScreenManager):
        self._screen_manager = value

    @property
    def logic(self) -> MainScreenLogic:
        if self._logic is None:
            self._logic = MainScreenLogic(
                screen_constructor=self.screen_constructor,
                screen_manager=self.screen_manager,
                main_screen=self,
            )
        return self._logic
    
    @logic.setter
    def logic(self, value: MainScreenLogic):
        self._logic = value

    def btn_wyloguj(self):
        "Возвращает на экран логирования"
        action.logger.info('screens.py: class Main(MDScreen) btn_wyloguj()')

        def remove_remember_me_file():
            "Если есть файл, то удаляю"
            action.logger.info('build.py: remove_main_screen() remove_remember_me_file()')
            if os.path.isfile(self.screen_constructor.data_from_memory.path_to_freeze_file):
                os.remove(self.screen_constructor.data_from_memory.path_to_freeze_file)

        self.screen_manager.transition.direction = 'right'
        self.screen_constructor.remove_main_screen()
        self.screen_constructor.remove_calendar_screen()
        self.screen_constructor.authorization_screen.logic = None # обновляю объект логики для экрана авторизации
        action.logger.info("DEBUG: Update 'logic' object in 'authorization_screen'")

        if self.screen_constructor.data_from_memory.path_to_freeze_file is not None:
            remove_remember_me_file()

    def btn_menu_dodac(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_menu_dodac()')
        pass

    def btn_menu_wyslij(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_menu_wyslij()')
        pass

    def btn_memu_tabela(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_memu_tabela()')
        pass

    def btn_menu_pytac(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_menu_pytac()')
        pass

    def btn_menu_zadania(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_menu_zadania()')
        pass

    def btn_godziny(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_godziny()')
        self.logic.select_godziny()

    def btn_obiekt(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_obiekt()')
        self.logic.open_objects_menu_list()

    def btn_show_calendar(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_show_calendar()')
        # self.screen_constructor.add_calendar_screen_obj()
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'calendar_screen'

    def btn_dodac(self):
        action.logger.info('screens.py: class Main(MDScreen) btn_dodac()')

        if self.ids.godziny.text != 'Godziny' and \
            self.ids.obiekt.text != 'Obiekt':

            self.logic.write_to_user_db()
            self.sum_godziny = 0
            query_to_user_base = memory.QueryToSQLite3(
                    db_path = config.PATH_TO_USER_DB + f'/{self.user_hash}.db',
                    )
            user_data_from_db: list[tuple,] = query_to_user_base.show_data_from_table(table_name = config.FIRST_TABLE)
            ###
            self.ids.scroll.clear_widgets()
            make_table_thread = threading.Thread(
                target = self.logic.make_data_table,
                daemon = True,
                name = 'make_table_thread',
                args = [True, user_data_from_db]
            )
            make_table_thread.start()


class Calendar(MDScreen):
    def __init__(self, name, screen_manager, screen_constructor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        action.logger.info("screens.py: class Calendar(MDScreen) __init__() name = 'calendar_screen'")
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