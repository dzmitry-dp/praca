import threading
import json
import time
import os
from datetime import datetime

from kivy.clock import mainthread

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog

import dev.action as action
import dev.config as config
import dev.db.memory as memory
import dev.db.queries_struct as queries
from dev.view.helpers import AddHoursWidget, WorkObjects
from dev.client import start_client_server_dialog
from dev.action.hash import hash_to_user_name
from dev.action.purpose import options
from dev.view.helpers import TabelItem

class VerificationData:
    def __init__(self) -> None:
        action.logger.info('logic.py: class VerificationData __init__()')
        self.user_authorized: bool = None

    def get_permission(self, user_hash) -> bool:
        """
        Наличие файла базы данных авторизирует пользователя

        Если есть файл базы дынных, то ты авторизирован в системе

        Для создания базы данных нужно добавит хотябы один рабочий день
        """
        action.logger.info('logic.py: class VerificationData get_permission()')

        if os.path.exists(config.PATH_TO_USER_DB + f'/{user_hash}.db'):
            action.logger.info(f'DEBUG: Have {user_hash}.db file')
            self.user_authorized = True
        else:
            action.logger.info(f'DEBUG: Have NOT {user_hash}.db file')
            self.user_authorized = False
        
        return self.user_authorized


class AutorizationLogic(VerificationData):
    """Вся логика авторизации пользователя
    """
    def __init__(self, screen_constructor, screen_manager, authorization_obj: MDScreen) -> None:
        super().__init__()
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) __init__()')

        self._login = None
        self._password = None
        self._user_hash = None

        self._screen_constructor = screen_constructor # ScreensConstructor()
        self._screen_manager = screen_manager # ScreenManager()

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

    @property
    def user_hash(self):
        if self._user_hash is None:
            pass
        return self._user_hash

    @user_hash.setter
    def user_hash(self, value):
        self._user_hash = value

    @property
    def screen_constructor(self):
        return self._screen_constructor
    
    @screen_constructor.setter
    def screen_constructor(self, value):
        self._screen_constructor = value

    @property
    def screen_manager(self):
        return self._screen_manager
    
    @screen_manager.setter
    def screen_manager(self, value):
        self._screen_manager = value

    def _seach_user_in_base(self, remember_me: bool):
        """
        # Проверка пользователя в базе данных
        - Если пользователь в базе данных, то вывести его данные
        - Если нельзя найти совпадений по login и password, то заводим нового пользователя
        """
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) seach_user_in_base()')
        
        def _write_remember_me_file():
            self.screen_constructor.data_from_memory.path_to_freeze_file = config.PATH_TO_REMEMBER_ME + f'/{self.user_hash}.json'
            with open(self.screen_constructor.data_from_memory.path_to_freeze_file, 'w') as file:
                json.dump(options['remember_me'](self.login, self.password), file)

        def _get_data_from_db():
            "Нахожу данные пользователя"
            query_to_user_base = memory.QueryToSQLite3(db_path = config.PATH_TO_USER_DB + f'/{self.user_hash}.db',)
            self.screen_constructor.data_from_memory.user_data_from_db: list[tuple,] = query_to_user_base.show_data_from_table(table_name = config.FIRST_TABLE)
            
        if self.get_permission(self.user_hash): # если есть файл с базой данных
            if remember_me: # и если стоит галочка "запомнить меня"
                action.logger.info(f'logic.py: _seach_user_in_base() have DB and checkbox')
                _get_data_from_db()
                _write_remember_me_file() # сохраняем данные пользователя
            else:
                action.logger.info(f'logic.py: _seach_user_in_base() have DB and NOT checkbox')
                _get_data_from_db()
        else: # если нет файла базы данных
            if remember_me:
                action.logger.info(f'logic.py: _seach_user_in_base() have NOT DB and have checkbox')
                _write_remember_me_file()
            else:
                action.logger.info(f'logic.py: _seach_user_in_base() have NOT DB and have NOT checkbox')
    
        action.logger.info(f'DEBUG: remember_me = {remember_me}, user_authorized = {self.user_authorized}')
    
    @mainthread
    def _display_main_screen(self, search_user_thread: threading.Thread):
        """
        Создаю главный экран после авторизации пользователя, если экран еще не создан
        """
        action.logger.info('logic.py: class AutorizationLogic(VerificationData) _display_main_screen()')
        if self.screen_manager.has_screen(name='main_screen'):
            action.logger.info(f"DEBUG: Have 'main_screen'")
            self.screen_manager.get_screen('main_screen').user_name = self.login
            self.screen_manager.get_screen('main_screen').user_surname = self.password
            
        else:
            action.logger.info(f"DEBUG: Don't have 'main_screen'")
            self.screen_constructor.add_main_screen_obj(
                user_name = self.login,
                user_surname = self.password,
                search_user_thread = search_user_thread,
                )

        self.screen_constructor.main_screen.ids.backdrop.title = f'{self.screen_constructor.main_screen.user_name} {self.screen_constructor.main_screen.user_surname}'
        self.screen_manager.current = 'main_screen' 

    def _start_logic_logowania(self, remember_me: bool):
        "Логика того, что происходит после нажатия кнопки Logowanie"
        ### Отдельным потоком отправляемся искать данные о пользователе
        self.search_user_thread = threading.Thread(
            target = self._seach_user_in_base, 
            daemon = True,
            name = 'search_user_thread',
            args = [remember_me, ],
            )
        self.search_user_thread.start()
        ###
        ### Отдельным потоком переходим на главный экран
        self.display_main_screen_thread = threading.Thread(
            target = self._display_main_screen,
            daemon = True,
            name = 'display_main_screen_thread',
            args = [self.search_user_thread, ],
            )
        self.display_main_screen_thread.start()
        ###
        ### Отдельным потоком проверяю связь с сервером
        self.handshake_thread = threading.Thread(
            target = start_client_server_dialog,
            daemon = True,
            name = 'handshake_thread',
            kwargs = {
                'user_name': self.login,
                'user_surname': self.password,
                'remember_me': remember_me,
                'msg_purpose': 'handshake', # цель обращения - рукопожатие / проверка связи с сервером / получение сертификата для передачи данных
                }
            )
        self.handshake_thread.start()
        ###
        
        if not self.screen_manager.has_screen(name = 'calendar_screen'):
            self.screen_constructor.add_calendar_screen_obj()

    @mainthread    
    def check_user(self, remember_me: bool, login: str = None, password: str = None) -> None:
        """
        Вызов этой функции происходит по нажатию кнопки авторизации или после запуска приложения с данными из файла freeze.
        Исходя из того, что написано в полях ввода, составляю представление о пользователе
        """

        action.logger.info('logic.py: class AutorizationLogic(VerificationData) check_user()')

        def _spinners_off():
            action.logger.info('logic.py: class AutorizationLogic(VerificationData) _spinners_off()')
            time.sleep(2)
            self.display_main_screen_thread.join() # убедиться что экран main создан
            # выключаю спинеры
            self.screen_constructor.authorization_screen.ids.spinner.active = False
            self.screen_constructor.main_screen.ids.spinner.active = False

        if login is None and password is None: # btn_logowanie()
            self.login = self.authorization_obj.user_name.text.replace(' ', '')
            self.password = self.authorization_obj.user_surname.text.replace(' ', '')

            action.logger.info(f"DEBUG: Have Login and Password: '{login}' '{password}'")
            
            if login == '' or password == '':
                action.logger.warning(f"DEBUG: Have NOT Login and Password: '{login}' '{password}'")
                self.login = None
                self.password = None
                return None
                
        else: # start_with_user_data() from freeze_file
            self.login = login
            self.password = password

        self.user_hash = hash_to_user_name(f'{self.login}{self.password}', config.PORT)
        self._start_logic_logowania(remember_me)

        ### Через секунду остановить спинеры
        threading.Thread(target = _spinners_off, daemon = True).start()
        ###
    

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

        self.add_hour_widget: AddHoursWidget = None
        self.dialog_screen_to_set_godziny: MDDialog = None

    def select_godziny(self):
        action.logger.info('logic.py: class MainScreenLogic select_godziny()')
        if not self.dialog_screen_to_set_godziny:
            self.add_hour_widget = AddHoursWidget(
                main_screen = self.main_screen,
                main_screen_logic = self,
                )
            self.dialog_screen_to_set_godziny = MDDialog(
                type = "custom",
                content_cls = self.add_hour_widget
            )
        self.dialog_screen_to_set_godziny.open()

    def _transforming_data_from_database(self, user_data_from_db: list[tuple,]) -> json:
        if user_data_from_db == [] or user_data_from_db == None:
            return None
        keys = queries.user_table['column_data'].keys()
        return [dict(zip(keys, values)) for values in user_data_from_db]

    @mainthread
    def make_data_table(self, user_authorized: bool, user_data_from_db: list[tuple,]):
        action.logger.info('logic.py: class MainScreenLogic make_data_table()')
        if user_authorized:
            user_data: list[tuple,] = self._transforming_data_from_database(user_data_from_db)
        else:
            user_data = None

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
        date: str = widget.text
        date_string = f"{datetime.now().year}-{date[-2:]}-{date[:2]}"
        datetime_obj = datetime.strptime(date_string, "%Y-%m-%d")
        building_object = widget.parent.parent.text
        self.main_screen.ids.scroll.remove_widget(widget.parent.parent)
        self._remove_from_user_data_base(datetime_obj, building_object)
        # вычисляю часы
        hours = int(widget.parent.parent.ids.left_label.text)
        self.main_screen.sum_godziny -= hours
        self.main_screen.ids.summa.text = f'Masz {self.main_screen.sum_godziny} godzin'

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
            self.add_hour_widget = WorkObjects(
                main_screen = self.main_screen,
                main_screen_logic = self,
                )
            self.dialog_screen_to_set_object = MDDialog(
                type = "custom",
                content_cls = self.add_hour_widget
            )
        self.dialog_screen_to_set_object.open()

    def create_user_data_base(self, path, user_name, user_surname, date, build_object, hour):
        "Создаю базу данных для пользователя, если файл еще не создан"
        query_to_user_base = memory.QueryToSQLite3(
            db_path = path,
            )
        query_to_user_base.create_table(data = queries.user_table)
        query_to_user_base.write_values(
            data = queries.generate_data(user_name, user_surname, date, build_object, hour),
            )
        
    def add_to_user_data_base(self, path, user_name, user_surname, date, build_object, hour):
        "Добавляю данные в пользовательскую базу данных"
        query_to_user_base = memory.QueryToSQLite3(
            db_path = path,
            )
        query_to_user_base.write_values(
            data = queries.generate_data(user_name, user_surname, date, build_object, hour),
            )

    def _remove_from_user_data_base(self, datetime_obj, building_object):
        path = config.PATH_TO_USER_DB + f'/{self.main_screen.user_hash}.db'
        query_to_user_base = memory.QueryToSQLite3(
            db_path = path,
            )
        query_to_user_base.remove_row(
            data = queries.get_date_to_remove(datetime_obj=datetime_obj, building_object=building_object)
        )