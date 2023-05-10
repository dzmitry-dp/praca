import threading
import json
import time
import os

from kivy.clock import mainthread

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog

import dev.action as action
import dev.config as config
import dev.db.memory as memory
import dev.db.queries_struct as queries
from dev.view.helpers import AddHoursWidget, WorkObjects
from dev.client import Client
from dev.action.hash import hash_to_user_name
from dev.action.purpose import options
from dev.view.helpers import TabelItem

class VerificationData:
    def __init__(self) -> None:
        action.logger.info('logic.py: class VerificationData __init__()')

    def get_permission(self, login, password, user_hash) -> bool:
        """
        Наличие файла базы данных авторизирует пользователя
        Если есть файл, то ты авторизирован системе
        Для авторизации нужно добавит хотябы один рабочий день
        """
        action.logger.info('logic.py: class VerificationData get_permission()')

        if os.path.exists(config.PATH_TO_USER_DB + f'/{user_hash}.db'):
            action.logger.info(f'DEBUG: Have {user_hash}.db file')
            return True
        else:
            action.logger.info(f'DEBUG: Have NOT {user_hash}.db file')
            return False


class AutorizationLogic(VerificationData):
    """Вся логика авторизации пользователя
    """
    def __init__(self, screen_constructor, screen_manager, authorization_obj: MDScreen) -> None:
        super().__init__()
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) __init__()')

        self._login = None
        self._password = None
        self.user_hash = None

        self.screen_constructor = screen_constructor # ScreensConstructor()
        self.screen_manager = screen_manager # ScreenManager()
        self.authorization_obj = authorization_obj # Autorization(MDScreen)

        self.search_user_thread = None # поток поиска пользовательских данных
        self.display_main_screen_thread = None # поток отображения главного экрана
        self.handshake_thread = None # поток связи с сервером
        
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
    def _seach_user_in_base(self, remember_me: bool):
        """# Проверка пользователя в базе данных
        - Если пользователь в базе данных, то вывести его данные
        - Если нельзя найти совпадений по login и password, то заводим нового пользователя
        """
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) seach_user_in_base()')
        def remove_remember_me_file():
            "Если есть файл, то удаляю"
            action.logger.info('logic.py: _seach_user_in_base() remove_remember_me_file()')
            path_to_json = config.PATH_TO_REMEMBER_ME + f'/{self.user_hash}.json'
            if os.path.isfile(path_to_json):
                os.remove(path_to_json)
        
        def write_remember_me_file():
            self.screen_constructor.path_to_freeze_file = config.PATH_TO_REMEMBER_ME + f'/{self.user_hash}.json'
            with open(self.screen_constructor.path_to_freeze_file, 'w') as file:
                json.dump(options['remember_me'](self.login, self.password), file)

        def get_data_from_db():
            "Нахожу данные пользователя"
            query_to_user_base = memory.Query(
                    db_path = config.PATH_TO_USER_DB + f'/{self.user_hash}.db',
                    )
            self.screen_constructor.user_data_from_db: list = query_to_user_base.show_data_from_table(table_name = config.FIRST_TABLE)
            
        if self.get_permission(self.login, self.password, self.user_hash): # проверяю пароль
            # прошли авторизацию - есть база данных
            self.authorization_obj.user_authorized = True

            if remember_me:
                # если есть файл с базой данных
                # и если стоит галочка "запомнить меня"
                action.logger.info(f'logic.py: _seach_user_in_base() have DB and checkbox')
                get_data_from_db()
                # запомнить стартовые данные пользователя
                write_remember_me_file()
            else:
                # если есть файл с базой данных
                # но нет галочки "запомнить меня"
                action.logger.info(f'logic.py: _seach_user_in_base() have DB and NOT checkbox')
                get_data_from_db()
                remove_remember_me_file()
        else:
            # не зарегистрированный пользователь
            self.authorization_obj.user_authorized = False
            # как вариант можно показать рекламу
            if remember_me:
                # если нет файла, но
                # стоит галочка "запомнить меня"
                action.logger.info(f'logic.py: _seach_user_in_base() have NOT DB and have checkbox')
                write_remember_me_file()
            else:
                # если нет файла базы данных
                # и не стоит галочка
                action.logger.info(f'logic.py: _seach_user_in_base() have NOT DB and have NOT checkbox')
                remove_remember_me_file()
    
        action.logger.info(f'DEBUG: remember_me = {remember_me}, user_authorized = {self.authorization_obj.user_authorized}')
    
    @mainthread
    def _display_main_screen(self, search_user_thread: threading.Thread):
        """Создаю главный экран после авторизации пользователя, если экран еще не создан
        
        self.screen_constructor.popup_screen - подвижная вкладка
        """
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) _display_main_screen()')
        if self.screen_manager.has_screen(name='main_screen'):
            action.logger.info(f"DEBUG: Have 'main_screen'")
            self.screen_manager.get_screen('main_screen').user_name = self._login
            self.screen_manager.get_screen('main_screen').user_surname = self._password
            
        else:
            action.logger.info(f"DEBUG: Don't have 'main_screen'")
            self.screen_constructor.add_main_screen_obj(
                user_name = self._login,
                user_surname = self._password,
                search_user_thread = search_user_thread,
                )

        self.screen_constructor.main_screen.ids.backdrop.title = f'{self.screen_constructor.main_screen.user_name} {self.screen_constructor.main_screen.user_surname}'
        self.screen_constructor.popup_screen = self.screen_constructor.main_screen.children[0].ids['_front_layer'].children[0].children[0].children[0]
        self.screen_manager.current = 'main_screen' 

    def _start_logic_logowania(self, remember_me: bool):
        "Логика того, что происходит после нажатия кнопки Logowanie"
        ### Отдельным потоком отправляемся искать данные о пользователе
        self.search_user_thread = threading.Thread(
            target=self._seach_user_in_base, 
            daemon=True,
            name='search_user_thread',
            args=[remember_me, ],
            )
        self.search_user_thread.start()
        ###
        ### Отдельным потоком переходим на главный экран
        self.display_main_screen_thread = threading.Thread(
            target=self._display_main_screen,
            daemon=True,
            name='display_main_screen_thread',
            args=[self.search_user_thread, ],
        )
        self.display_main_screen_thread.start()
        ###
        self.search_user_thread.join()
        # if self.authorization_obj.user_authorized:
        ### Отдельным потоком проверяю связь с сервером
        self.handshake_thread = threading.Thread(
            target=Client.start_client_server_dialog,
            daemon=True,
            name='handshake_thread',
            kwargs={
                'user_name': self.login,
                'user_surname': self.password,
                'remember_me': remember_me,
                'msg_purpose': 'handshake', # цель обращения - рукопожатие / проверка связи с сервером / получение сертификата для передачи данных
                }
        )
        self.handshake_thread.start()
        ###

    @mainthread    
    def check_user(self, remember_me: bool, login: str = None, password: str = None) -> None:
        """Вызов этой функции происходит по нажатию кнопки авторизации.
        Исходя из того, что написано в полях ввода,
        составляю представление о пользователе"""
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) check_user()')

        if login is None and password is None:
            login = self.authorization_obj.user_name.text.replace(' ', '')
            password = self.authorization_obj.user_surname.text.replace(' ', '')

        if login != '' and password != '':
            action.logger.info(f"DEBUG: Have Login and Password: '{login}' '{password}'")
            
            self.login = login
            self.password = password
            self.user_hash = hash_to_user_name(f'{login}{password}', config.PORT)

            self._start_logic_logowania(remember_me)
            self.display_main_screen_thread.join()
            self.handshake_thread.join()

        else:
            action.logger.warning(f"DEBUG: Have NOT Login and Password: '{login}' '{password}'")

        ### Через секунду остановить спинеры
        threading.Thread(target=self.spinners_off, daemon=True).start()
        ###
    
    @mainthread
    def spinners_off(self):
        time.sleep(1)
        # выключаю спинеры
        self.screen_constructor.authorization_screen.ids.spinner.active = False
        self.screen_constructor.main_screen.ids.spinner.active = False
            

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

    def _transforming_data_from_database(self, user_data_from_db: list[tuple,]) -> json:
        if user_data_from_db == []:
            return None
        keys = queries.user_table['column_data'].keys()
        return [dict(zip(keys, values)) for values in user_data_from_db]

    @mainthread
    def make_data_table(self, user_data_from_db):
        action.logger.info('logic.py: class MainScreenLogic make_data_table()')

        user_data: list[tuple,] = self._transforming_data_from_database(user_data_from_db)

        if user_data is None:
            action.logger.info(f'DEBUG: Have NOT user_data = {user_data}')
        else:
            action.logger.info(f'DEBUG: Have user_data = {user_data}')
            for row in user_data:
                item = TabelItem(
                    text=row['building'],
                    on_release=self.on_click_table_row,
                )
                self.main_screen.sum_godziny += row['hour']
                item.ids.left_label.text = str(row['hour'])
                item.ids.right_button.text = row['date'].strftime('%d.%m')
                item.ids.right_button.on_release = lambda widget=item.ids.right_button: self.on_click_table_right_button(widget)
                
                self.main_screen.ids.scroll.add_widget(item)
            self.main_screen.ids.summa.text = f'Masz {self.main_screen.sum_godziny} godzin'

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

    def create_user_data_base(self, path, user_name, user_surname, date, build_object, hour):
        "Создаю базу данных для пользователя, если файл еще не создан"
        query_to_user_base = memory.Query(
            db_path = path,
            )
        query_to_user_base.create_table(data = queries.user_table)
        query_to_user_base.write_values(
            data = queries.generate_first_data(user_name, user_surname, date, build_object, hour),
            )
        
    def add_to_user_data_base(self, path, user_name, user_surname, date, build_object, hour):
        "Добавляю данные в пользовательскую базу данных"
        query_to_user_base = memory.Query(
            db_path = path,
            )
        query_to_user_base.write_values(
            data = queries.generate_first_data(user_name, user_surname, date, build_object, hour),
            )
        print(query_to_user_base.show_data_from_table(table_name = config.FIRST_TABLE))