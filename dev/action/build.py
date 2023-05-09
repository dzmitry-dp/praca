import threading
import os
import json

import dev.action as action
import dev.config as config
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
        action.logger.info('build.py: class ScreensConstructor __init__()')
        # Управление
        self.screen_manager = screen_manager # ScreenManager()
        # Мои экраны
        self.authorization_screen = None # authorization_screen
        self.main_screen = None # main_screen
        self.calendar = None # calendar_screen
        # Отдельные виджеты
        self.popup_screen = None # подвижная вкладка MDBackdropFrontLayer
        # Remember me
        self.freeze_file: json = None
        self.path_to_freeze_file = None

    def _freeze_member(self) -> bool:
        action.logger.info('build.py: class ScreensConstructor _freeze_member()')
        # список всех файлов в папке
        files = os.listdir(config.PATH_TO_REMEMBER_ME)
        # фильтрация файлов по расширению
        json_files = [file for file in files if file.endswith('.json')]
        
        if len(json_files) == 0:
            action.logger.info(f'DEBUG: Have NOT json files')
            return False
        
        if len(json_files) == 1:
            action.logger.info(f'DEBUG: Have json file {json_files[0]}')
            self.path_to_freeze_file = config.PATH_TO_REMEMBER_ME + f'/{json_files[0]}'
            with open(self.path_to_freeze_file, 'r') as file:
                self.freeze_file = json.load(file)
            return True

        if len(json_files) > 1:
            action.logger.info(f'DEBUG: Have json files {json_files}')
            return False # если нет файлов или нужно выбирать

    def start_building(self):
        """
        # Первый запуск системы
        Последовательность создания экранов так же важена.
        Вначале создается экран который и будет отображаться, а уже под ним создаются остальные
        """
        action.logger.info('build.py: class ScreensConstructor start_building()')

        if self._freeze_member():
            # если пользователь хочет чтобы приложение помнило его
            # если в каталоге /db/freeze всего один файл
            self.add_authorization_screen_obj()
            self.add_calendar_screen_obj()
            self.authorization_screen.ids.spinner.active = True

            user_name = self.freeze_file['name']
            self.authorization_screen.user_name.text = user_name
            user_surname = self.freeze_file['surname']
            self.authorization_screen.user_surname.text = user_surname

            self.authorization_screen.logic.check_user(self.authorization_screen.remember_me, user_name, user_surname)
        else:
            self.add_authorization_screen_obj()
            self.add_calendar_screen_obj()
            self.add_main_screen_obj(user_name='', user_surname='', search_user_thread=None)
            self.screen_manager.current = 'authorization_screen'

    def add_authorization_screen_obj(self):
        "Создаю и добавляю экран авторизации"
        action.logger.info('build.py: class ScreensConstructor add_authorization_screen_obj()')
        self.authorization_screen = Autorization(
                name='authorization_screen',
                screen_constructor = self,
                screen_manager=self.screen_manager
            )
        self.authorization_screen.build_logic_object()
        self.screen_manager.add_widget(self.authorization_screen)

    def add_main_screen_obj( # main_screen
            self,
            user_name,
            user_surname,
            search_user_thread = None, # поток в котором получаем все данные о пользователе
            ):
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
            ### Отдельным потоком создаем таблицу данных
            make_table_thread = threading.Thread(
                target=self.main_screen.logic.make_data_table,
                daemon=True,
                name='make_table_thread',
                args = [search_user_thread,]
            )
            make_table_thread.start()
            ###

    def remove_main_screen(self) -> None:
        def remove_remember_me_file():
            "Если есть файл, то удаляю"
            action.logger.info('build.py: remove_main_screen() remove_remember_me_file()')
            if os.path.isfile(self.path_to_freeze_file):
                os.remove(self.path_to_freeze_file)

        action.logger.info('build.py: class ScreensConstructor remove_main_screen()')
        self.screen_manager.remove_widget(self.main_screen)
        self.authorization_screen.build_logic_object()
        self.main_screen = None
        remove_remember_me_file()

    def add_calendar_screen_obj(self): # calendar_screen
        action.logger.info('build.py: class ScreensConstructor add_calendar_screen_obj()')
        self.calendar = Calendar(
            name = 'calendar_screen',
            screen_manager = self.screen_manager,
            screen_constructor = self,
        )
        self.screen_manager.add_widget(self.calendar)

    def remove_calendar_screen(self):
        action.logger.info('build.py: class ScreensConstructor remove_calendar_screen()')
        self.screen_manager.remove_widget(self.calendar)
        self.calendar = None