import threading
import time

import dev.action as action
from dev.view.screens import Autorization, Main, Calendar
from dev.db.memory import MemoryDataContainer


class MyScreensObjects:
    """
    # Экраны для пользователя

    self.authorization_screen: экран авторизации пользователя
    
    self.main_screen: главный экран где пользователь добавляет часы

    self.calendar_screen: экран календаря

    """

    def __init__(self, screen_constructor) -> None:
        action.logger.info('build.py: class MyScreensObjects __init__()')
        self.screen_constructor = screen_constructor

        self.authorization_screen = None # authorization_screen
        self._main_screen = None # main_screen
        self.calendar_screen = None # calendar_screen

    @property
    def main_screen(self):
        if self._main_screen is None:
            self.screen_constructor.add_main_screen_obj()

        return self._main_screen
    
    @main_screen.setter
    def main_screen(self, value):
        self._main_screen = value


class ScreensConstructor(MyScreensObjects):
    """
    # Сборщик/Утилизатор рабочих экранов для пользователя

    self.screen_manager: объект kivy.uix.screenmanager.ScreenManager() который контролирует экраны и память

    self.data_from_memory: контейнер для данных которые нужно помнить

    - def start_building() -> None:
    - def add_authorization_screen_obj() -> None: 
    - def add_main_screen_obj() -> None:
    - def remove_main_screen() -> None:
    - def add_calendar_screen_obj() -> None:
    - def remove_calendar_screen() -> None:
    """

    def __init__(self, screen_manager) -> None:
        super().__init__(self)
        action.logger.info('build.py: class ScreensConstructor __init__()')
        self.screen_manager = screen_manager # ScreenManager() управление экранами и памятью
        self._data_from_memory = None
        self.start_building()

        self.check_user_thread: threading = None

    @property
    def data_from_memory(self):
        if self._data_from_memory is None:
            self._data_from_memory = MemoryDataContainer()
        return self._data_from_memory

    @data_from_memory.setter
    def data_from_memory(self, value):
        self._data_from_memory = value

    def start_building(self) -> None:
        """
        # Первый запуск системы
        Последовательность создания экранов так же важена.
        Вначале создается экран который и будет отображаться, а уже под ним создаются остальные
        """
        action.logger.info('build.py: class ScreensConstructor start_building()')

        def _start_with_user_data(user_name: str, user_surname: str):
            self.authorization_screen.ids.spinner.active = True

            def _spinner_off():
                time.sleep(2)
                self.authorization_screen.ids.spinner.active = False

            _off = threading.Thread(target=_spinner_off, name='_spinner_off', daemon=True)
            _off.start()

            self.authorization_screen.user_name.text = user_name
            self.authorization_screen.logic.login = user_name
            self.authorization_screen.user_surname.text = user_surname
            self.authorization_screen.logic.password = user_surname
            ### Отдельным потоком отправляемся искать данные о пользователе
            self.check_user_thread = threading.Thread(
                target=self.authorization_screen.logic.check_user,
                daemon=True,
                name='check_user_thread',
                args=[self.authorization_screen.remember_me, user_name, user_surname,],
                )
            self.check_user_thread.start()

        self.add_authorization_screen_obj()
        self.add_main_screen_obj(search_user_thread = None)
        self.add_calendar_screen_obj()

        if self.data_from_memory.freeze_file_data is not None: # выбираю последний записанный файл 
            _start_with_user_data(
                user_name = self.data_from_memory.freeze_file_data['name'],
                user_surname = self.data_from_memory.freeze_file_data['surname'],
                )

    def add_authorization_screen_obj(self) -> None:
        "Создаю и добавляю экран авторизации"
        action.logger.info('build.py: class ScreensConstructor add_authorization_screen_obj()')
        self.authorization_screen = Autorization(
                name='authorization_screen',
                screen_constructor = self,
                screen_manager=self.screen_manager
            )
        self.screen_manager.add_widget(self.authorization_screen)

    def add_main_screen_obj(self, search_user_thread = None,) -> None: # main_screen
        "Создаю и добавляю главный экран приложения"
        action.logger.info('build.py: class ScreensConstructor add_main_screen_obj()')
        self.main_screen = Main(
                name = 'main_screen',
                screen_constructor = self,
                screen_manager = self.screen_manager,
            )
        # запускаю виджет символизирующий ожидание
        self.main_screen.ids.spinner.active = True

        def _spiner_off():
            time.sleep(3)
            self.main_screen.ids.spinner.active = False

        _off = threading.Thread(target=_spiner_off, daemon=True, name='_spinner_off')
        _off.start()
        
        if search_user_thread is not None:
            search_user_thread.join()
            ### Отдельным потоком создаем таблицу данных
            make_table_thread = threading.Thread(
                target = self.main_screen.logic.make_data_table,
                daemon = True,
                name = 'make_table_thread',
                args = [
                    self.data_from_memory.user_data_from_db,
                    ]
            )
            make_table_thread.start()
            ###

        self.screen_manager.add_widget(self.main_screen)

    def remove_main_screen(self) -> None:
        action.logger.info('build.py: class ScreensConstructor remove_main_screen()')
        self.screen_manager.remove_widget(self.main_screen)
        self.main_screen = None

    def add_calendar_screen_obj(self) -> None: # calendar_screen
        action.logger.info('build.py: class ScreensConstructor add_calendar_screen_obj()')
        self.calendar_screen = Calendar(
            name = 'calendar_screen',
            screen_manager = self.screen_manager,
            screen_constructor = self,
        )
        self.screen_manager.add_widget(self.calendar_screen)

    def remove_calendar_screen(self) -> None:
        action.logger.info('build.py: class ScreensConstructor remove_calendar_screen()')
        self.screen_manager.remove_widget(self.calendar_screen)
        self.calendar_screen = None
