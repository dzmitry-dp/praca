import threading

import dev
from dev.view.screens import Autorization, Main, Calendar


class ScreensConstructor:
    """
    # Сборщик/Утилизатор рабочих экранов для пользователей

    - self.screen_manager
    - self.authorization_screen
    - self.main_screen

    def add_authorization_screen_obj()
    def add_main_screen_obj()
    def remove_main_screen()
    """
    def __init__(self, screen_manager) -> None:
        dev.logger.info('build.py: class ScreensConstructor __init__()')
        # Управление
        self.screen_manager = screen_manager # ScreenManager()
        # Мои экраны
        self.authorization_screen = None # authorization_screen
        self.main_screen = None # main_screen
        self.popup_screen = None # подвижная вкладка MDBackdropFrontLayer
        self.calendar = None # calendar_screen

    def start_building(self):
        "Первый запуск системы"
        dev.logger.info('build.py: class ScreensConstructor start_building()')
        self.add_authorization_screen_obj()
        self.add_calendar_screen_obj()

    def add_authorization_screen_obj(self):
        "Создаю и добавляю экран авторизации"
        dev.logger.info('build.py: class ScreensConstructor add_authorization_screen_obj()')
        self.authorization_screen = Autorization(
                name='authorization_screen',
                screen_constructor = self,
                screen_manager=self.screen_manager
            )
        self.screen_manager.add_widget(self.authorization_screen)

    def add_main_screen_obj( # main_screen
            self,
            user_name,
            user_surname,
            screen_constructor,
            search_user_thread, # поток в котором получаем все данные о пользователе
            ):
        "Создаю и добавляю главный экран приложения"
        dev.logger.info('build.py: class ScreensConstructor add_main_screen_obj()')
        self.main_screen = Main(
                name = 'main_screen',
                user_name = user_name,
                user_surname = user_surname,
                screen_constructor = screen_constructor,
                screen_manager = self.screen_manager
            )
        
        ### Отдельным потоком создаем таблицу данных
        make_table_thread = threading.Thread(
            target=self.main_screen.logic.make_data_table,
            daemon=True,
            name='make_table_thread',
            args = [search_user_thread,]
        )
        make_table_thread.start()
        ###
        self.screen_manager.add_widget(self.main_screen)

    def remove_main_screen(self) -> None:
        dev.logger.info('build.py: class ScreensConstructor remove_main_screen()')
        self.screen_manager.remove_widget(self.main_screen)
        self.main_screen = None

    def add_calendar_screen_obj(self): # calendar_screen
        self.calendar = Calendar(
            name = 'calendar_screen',
            screen_manager = self.screen_manager,
            screen_constructor = self,
        )
        self.screen_manager.add_widget(self.calendar)
        # self.screen_manager.transition.direction = 'left'
        # self.screen_manager.current = 'calendar_screen'

    def remove_calendar_screen(self):
        dev.logger.info('build.py: class ScreensConstructor remove_calendar_screen()')
        self.screen_manager.remove_widget(self.calendar)
        self.calendar = None