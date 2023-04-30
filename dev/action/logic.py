import threading
import json

from kivy.clock import mainthread

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog

import dev.action as action
import dev.config as config
import dev.db.memory as memory
# import dev.db.queries_struct as queries
from dev.action.exceptions import DBConnectionErr
from dev.view.helpers import AddHoursWidget, WorkObjects
from dev.client import Client


class VerificationData:
    def __init__(self) -> None:
        action.logger.info('logic.py: class VerificationData __init__()')

        self.query_to_user_base = memory.Query(
            db_path=config.PATH_TO_USER_DB,
            )
        self.query_to_employer_base = memory.Query(
            db_path=config.PATH_TO_EMPLOYER_DB,
        )

    def get_permission(self, login, password) -> bool:
        action.logger.info('logic.py: class VerificationData get_permission()')

        try:
            # Проверка на то, что пользователь в базе данных
            action.logger.info(f'DEBUG: try connect to DB')
            print(self.query_to_employer_base.show_data_from_table(
                table_name = config.WORKER_TABLE,
                ))
            
            # all_data_from_db = query_to_user_base.query_select_user(
            #     table_name=queries.FIRST_TABLE,
            #     name=login,
            #     surname=password,
            #     )

            # action.logger.info(f'DEBUG: DB answer {all_data_from_db}')

            # if len(all_data_from_db) == 0:
            #     # если ответ из базы -> []
            #     query_to_user_base.write_values(data=queries.generate_first_data(self._login, self._password))
            #     all_data_from_db = query_to_user_base.query_select_user(
            #         table_name=queries.FIRST_TABLE,
            #         name=self._login,
            #         surname=self._password,
            #         ) # запрашиваем данные у которых логин и пароль\
            #             # совпадают с данными которые ввел пользователь

        except DBConnectionErr:
            # Если таблица еще не создана
            action.logger.error('logic.py: class VerificationData get_permission() "DB have NOT table"')
            # query_to_user_base.create_table(data=queries.user_table)
            # query_to_user_base.write_values(data=queries.generate_first_data(self._login, self._password))
            # all_data_from_db = query_to_user_base.query_select_user(
            #     table_name=queries.FIRST_TABLE,
            #     name=self._login,
            #     surname=self._password,
            #     ) # запрашиваем данные у которых логин и пароль\
            #     # совпадают с данными которые ввел пользователь
            return False
        
        # all_data_from_db = ['Что-то из DB',]
        # if len(all_data_from_db) != 0:
        #     action.logger.info('DEBUG: class VerificationData get_permission() "Have user data"')
        #     # если длина сообщения из базы не равна 0
        #     # составленный запрос нашел данные в базе
        #     return True
        # else:
        #     # если собщение из базы -> []
        #     action.logger.info('DEBUG: class VerificationData get_permission() "New user"')
        #     return False
        return True


class AutorizationLogic(VerificationData):
    """Вся логика авторизации пользователя
    """
    def __init__(self, screen_constructor, screen_manager, authorization_obj: MDScreen) -> None:
        super().__init__()
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) __init__()')

        self._login = None
        self._password = None

        self._remember_me = False # checkbox active

        self.screen_constructor = screen_constructor # ScreensConstructor()
        self.screen_manager = screen_manager # ScreenManager()
        self.authorization_obj = authorization_obj # Autorization(MDScreen)

        self.search_user_thread = None # поток поиска пользовательских данных
        self.display_main_screen_thread = None # поток отображения главного экрана
        self.handshake_thread = None # поток связи с сервером
        self.download_thread = None # поток загрузки данных с сервера
        
    @property
    def login(self):
        if self._login is None:
            pass
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def password(self):
        if self._password is None:
            pass
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def _no_password_reaction(login: str, password: str):
        """Реакция на то, что логин и пароль не находится в базе данных"""
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) _no_password_reaction()')

    # функция выполняется в отдельном потоке
    def _seach_user_in_base(self):
        """# Проверка пользователя в базе данных
        - Если пользователь в базе данных, то вывести его данные
        - Если нельзя найти совпадений по login и password, то заводим нового пользователя
        """
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) seach_user_in_base()')

        if self.get_permission(self.login, self.password): # проверяю пароль
            # прошли авторизацию
            self.authorization_obj.user_authorized = True
        else:
            # не зарегистрированный пользователь
            self.authorization_obj.user_authorized = False
            # как вариант можно показать рекламу
            ### Отдельным потоком скачиваем актуальные данные
            msg_purpose = 1 # putpose.download_employer_database() # загрузка свежей базы данных
            self.download_thread = threading.Thread(
                target=Client.start_client_server_dialog, 
                daemon=True,
                name='download_thread',
                kwargs={
                    'user_name': self.login,
                    'user_surname': self.password,
                    'thread': self.handshake_thread,
                    'msg_purpose': msg_purpose,
                }
            )
            self.download_thread.start()
            ###
        
        action.logger.debug(f'-: user_authorized = {self.authorization_obj.user_authorized}')
    
    @mainthread
    def _display_main_screen(self, search_user_thread = None):
        """Создаю главный экран после авторизации пользователя, если экран еще не создан
        
        self.screen_constructor.popup_screen - подвижная вкладка
        """
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) _display_main_screen()')

        if self.screen_manager.has_screen(name='main_screen'):
            self.screen_constructor.main_screen.user_name = self._login
            self.screen_constructor.main_screen.user_surname = self._password
            self.screen_manager.get_screen('main_screen').ids.backdrop.title = f'{self.screen_constructor.main_screen.user_name} {self.screen_constructor.main_screen.user_surname}'
            self.screen_constructor.popup_screen = self.screen_manager.get_screen('main_screen').children[0].ids['_front_layer'].children[0].children[0].children[0]

            self.screen_manager.current = 'main_screen'
        else:
            action.logger.error("logic.py: _create_main_screen() Don't have 'main_screen'")
            self.screen_constructor.add_main_screen_obj(
                user_name = self._login,
                user_surname = self._password,
                screen_constructor = self.screen_constructor,
                search_user_thread = search_user_thread,
                )
            self.screen_manager.get_screen('main_screen').ids.backdrop.title = f'{self.screen_constructor.main_screen.user_name} {self.screen_constructor.main_screen.user_surname}'
            self.screen_constructor.popup_screen = self.screen_manager.get_screen('main_screen').children[0].ids['_front_layer'].children[0].children[0].children[0]

            self.screen_manager.current = 'main_screen'

    def _start_logic_logowania(self):
        "Логика того, что происходит после нажатия кнопки Logowanie"
        ### Отдельным потоком отправляемся искать данные о пользователе
        self.search_user_thread = threading.Thread(
            target=self._seach_user_in_base, 
            daemon=True,
            name='search_user_thread')
        self.search_user_thread.start()
        ###
        ### Отдельным потоком создаем главный экран
        self.display_main_screen_thread = threading.Thread(
            target=self._display_main_screen, 
            daemon=True,
            name='display_main_screen_thread',
            args=[self.search_user_thread,],
        )
        self.display_main_screen_thread.start()
        ###
        ### Отдельным потоком создаем главный экран
        self.handshake_thread = threading.Thread(
            target=Client.start_client_server_dialog, 
            daemon=True,
            name='handshake_thread',
            kwargs={
                'user_name': self.login,
                'user_surname': self.password,
                'thread': self.display_main_screen_thread,
            },
        )
        self.handshake_thread.start()
        
        self.screen_constructor.authorization_screen.ids.spinner.active = False
        self.screen_constructor.main_screen.ids.spinner.active = False

    def check_user_in_database(self) -> None:
        """Вызов этой функции происходит по нажатию кнопки авторизации.
        Исходя из того, что написано в полях ввода,
        составляю представление о пользователе"""
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) set_user()')

        _login = self.authorization_obj.user_name.text.replace(' ', '')
        _password = self.authorization_obj.user_surname.text.replace(' ', '')


        if _login != '' and _password != '':
            action.logger.info(f"DEBUG: Have Login and Password: '{_login}' '{_password}'")
            
            self.login = _login
            self.password = _password

            self._start_logic_logowania()
            
        else:
            action.logger.warning(f"DEBUG: Have NOT Login and Password: '{_login}' '{_password}'")
            
        self.screen_constructor.authorization_screen.ids.spinner.active = False

    def on_checkbox_active(self, checkbox, value):
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) on_checkbox_active()')
        if value:
            # print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
            self._remember_me = True
        else:
            # print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')
            self._remember_me = False
        
        action.logger.info(f'DEBUG: self._remember_me = {self._remember_me}')


class MainScreenLogic:
    """Логика главного экрана"""

    dialog_screen_to_set_godziny = None
    dialog_screen_to_set_object = None

    def __init__(self,
                 screen_constructor,
                 screen_manager,
                 main_screen: MDScreen,
                 ) -> None:
        action.logger.info('logic.py: class MainScreenLogic __init__()')
        self.screen_manager = screen_manager
        self.screen_constructor = screen_constructor # ScreensConstructor()
        
        self.main_screen = main_screen # class Main(MDScreen)

        self.widgets: AddHoursWidget = None
        self.dialog_screen_to_set_godziny: MDDialog = None

    def select_godziny(self):
        action.logger.info('logic.py: class MainScreenLogic select_godziny()')
        if not self.dialog_screen_to_set_godziny:
            self.widgets = AddHoursWidget(
                main_screen = self.main_screen,
                main_screen_logic = self,
                )
            self.dialog_screen_to_set_godziny = MDDialog(
                type = "custom",
                content_cls = self.widgets
            )
        self.dialog_screen_to_set_godziny.open()

    def _read_user_data_from_json(self) -> json:
        #
        return json.dumps({
            'user_name': 'User',
            'user_surname': 'Surname',
        })

    def make_data_table(self, search_user_thread = None):
        action.logger.info('logic.py: class MainScreenLogic make_data_table()')

        if search_user_thread is not None:
            search_user_thread.join() # дождался когда закончится сборка данных для конкретного пользователя
        
        user_data = self._read_user_data_from_json()

        if user_data is None:
            action.logger.info(f'DEBUG: Have NOT user_data = {user_data}')
        else:
            action.logger.info(f'DEBUG: Have user_data = {user_data}')

    def on_click_table_row(self, widget):
        "Функция отрабатывает по клику на строку таблицы"
        action.logger.info('logic.py: class MainScreenLogic on_click_table_row()')
        action.logger.info(f'DEBUG: wdiget.text: {widget.text} left_label.text: {widget.ids.left_label.text} right_button.text: {widget.ids.right_button.text}')

    def on_click_table_right_button(self, widget):
        "Функция отрабатывает по клику на дату"
        action.logger.info('logic.py: class MainScreenLogic on_click_table_right_button()')
        action.logger.info(f'DEBUG: wdiget.text: {widget.text} widget.parent.parent: {widget.parent.parent} widget.parent.parent.text: {widget.parent.parent.text}')

    def on_save_calendar(self, value):
        action.logger.info('logic.py: class MainScreenLogic on_save_calendar()')
        if value.day <= 9:
            day = f'0{value.day}'
        else:
            day = value.day

        if value.month <= 9:
            month = f'0{value.month}'
        else:
            month = value.month

        self.main_screen.ids.date.text = f"{day}.{month}"

    def open_objects_menu_list(self):
        action.logger.info('logic.py: class MainScreenLogic open_objects_menu_list()')

        if not self.dialog_screen_to_set_object:
            self.widgets = WorkObjects(
                main_screen = self.main_screen,
                main_screen_logic = self,
                )
            self.dialog_screen_to_set_object = MDDialog(
                type = "custom",
                content_cls = self.widgets
            )
        self.dialog_screen_to_set_object.open()
