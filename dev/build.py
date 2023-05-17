import threading

import dev.action as action
import dev.config as config
from dev.view.screens import Autorization, Main, Calendar
from dev.db.memory import MemoryDataContainer


class MyScreensObjects:
    """
    # Экраны для пользователя

    self.authorization_screen: экран авторизации пользователя
    
    self.main_screen: главный экран где пользователь добавляет часы

    self.calendar_screen: экран календаря

    """

    def __init__(self) -> None:
        action.logger.info('build.py: class MyScreensObjects __init__()')
        self.authorization_screen = None # authorization_screen
        self.main_screen = None # main_screen
        self.calendar_screen = None # calendar_screen


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
        super().__init__()
        action.logger.info('build.py: class ScreensConstructor __init__()')
        self.screen_manager = screen_manager # ScreenManager() управление экранами и памятью
        self.data_from_memory = MemoryDataContainer()
        self.start_building()

    def start_building(self) -> None:
        """
        # Первый запуск системы
        Последовательность создания экранов так же важена.
        Вначале создается экран который и будет отображаться, а уже под ним создаются остальные
        """
        action.logger.info('build.py: class ScreensConstructor start_building()')

        def _start_with_user_data():
            self.authorization_screen.user_name.text = freeze_file_data['name']
            self.authorization_screen.user_surname.text = freeze_file_data['surname']
            self.authorization_screen.ids.spinner.active = True
            ### Отдельным потоком отправляемся искать данные о пользователе
            check_user_thread = threading.Thread(
                target=self.authorization_screen.logic.check_user,
                daemon=True,
                name='check_user_thread',
                args=[self.authorization_screen.remember_me, freeze_file_data['name'], freeze_file_data['surname']],
                )
            check_user_thread.start()

        self.add_authorization_screen_obj()
        self.add_calendar_screen_obj()
        freeze_file_data = self.data_from_memory.get_freeze_member()

        if freeze_file_data is not None: # если в каталоге /db/freeze всего один json файл
            _start_with_user_data()
        else:
            self.add_main_screen_obj(user_name = '', user_surname = '', search_user_thread = None)

    def add_authorization_screen_obj(self) -> None:
        "Создаю и добавляю экран авторизации"
        action.logger.info('build.py: class ScreensConstructor add_authorization_screen_obj()')
        self.authorization_screen = Autorization(
                name='authorization_screen',
                screen_constructor = self,
                screen_manager=self.screen_manager
            )
        self.authorization_screen.refresh_internal_logic_object()
        self.screen_manager.add_widget(self.authorization_screen)

    def add_main_screen_obj(self, user_name, user_surname, search_user_thread = None,) -> None: # main_screen
        "Создаю и добавляю главный экран приложения"
        action.logger.info('build.py: class ScreensConstructor add_main_screen_obj()')
        self.main_screen = Main(
                name = 'main_screen',
                user_name = user_name,
                user_surname = user_surname,
                screen_constructor = self,
                screen_manager = self.screen_manager,
            )
        # запускаю виджет символизирующий ожидание
        self.main_screen.ids.spinner.active = True
        self.screen_manager.add_widget(self.main_screen)
        
        if search_user_thread is not None:
            search_user_thread.join()
            ### Отдельным потоком создаем таблицу данных
            make_table_thread = threading.Thread(
                target = self.main_screen.logic.make_data_table,
                daemon = True,
                name = 'make_table_thread',
                args = [
                    self.authorization_screen.user_authorized,
                    self.data_from_memory.user_data_from_db,
                    ]
            )
            make_table_thread.start()
            ###

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
