import dev
from dev.view.screens import Autorization, Main


class ScreensConstructor:
    """
    # Сборщик рабочих экранов для пользователей

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

    def start_building(self):
        "Первый запуск системы"
        dev.logger.info('build.py: class ScreensConstructor start_building()')
        self.add_authorization_screen_obj()

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
        self.screen_manager.add_widget(self.main_screen)
