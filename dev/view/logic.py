from kivy.clock import Clock
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog

import dev
import dev.db.memory as memory
import dev.config as config
import dev.db.queries_struct as queries
from dev.exceptions import DBConnectionErr
from dev.view.screens_helper import AddHoursWidget, WorkObjects


class VerificationData:
    def __init__(self) -> None:
        dev.logger.info('logic.py: class VerificationData __init__()')

    def get_permission(self, login, password) -> bool:
        dev.logger.info('logic.py: class VerificationData get_permission()')
        query_obj = memory.Query(
            db_path=config.PATH_TO_USER_DB,
            )

        try:
            # Проверка на то, что пользователь в базе данных
            
            all_data_from_db = query_obj.query_select_user(
                table_name=queries.USER_BASE,
                name=login,
                surname=password,
                )

            dev.logger.info(f'DEBUG: DB answer {all_data_from_db}')

            if len(all_data_from_db) == 0:
                # если ответ из базы -> []
                query_obj.write_values(data=queries.generate_first_data(self._login, self._password))
                all_data_from_db = query_obj.query_select_user(
                    table_name=queries.USER_BASE,
                    name=self._login,
                    surname=self._password,
                    ) # запрашиваем данные у которых логин и пароль\
                # совпадают с данными которые ввел пльзователь

        except DBConnectionErr:
            # Если таблица еще не создана
            dev.logger.error('logic.py: class VerificationData get_permission() "DB have NOT table"')
            query_obj.create_table(data=queries.user_table)
            query_obj.write_values(data=queries.generate_first_data(self._login, self._password))
            all_data_from_db = query_obj.query_select_user(
                table_name=queries.USER_BASE,
                name=self._login,
                surname=self._password,
                ) # запрашиваем данные у которых логин и пароль\
                # совпадают с данными которые ввел пользователь

        if len(all_data_from_db) != 0:
            # если длина сообщения из базы не равна 0
            # составленный запрос нашел данные в базе
            return True
        else:
            # если собщение из базы -> []
            dev.logger.info('logic.py: class VerificationData get_permission() "New user"')
            return False


class AutorizationLogic(VerificationData):
    """Вся логика авторизации пользователя
    """
    def __init__(self, screen_constructor, screen_manager, authorization_obj: MDScreen) -> None:
        super().__init__()
        dev.logger.info('logic.py: class AutorizationLogic __init__()')

        self._login = None
        self._password = None

        self.screen_constructor = screen_constructor # ScreensConstructor()
        self.screen_manager = screen_manager # ScreenManager()
        self.authorization_obj = authorization_obj # Autorization(MDScreen)
        
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
        dev.logger.info('logic.py: class AutorizationLogic _no_password_reaction()')

    def _create_main_screen(self):
        """Создаю главный экран после авторизации пользователя, если экран не создан
        self.screen_constructor.popup_screen - подвижная вкладка
        """
        dev.logger.info('logic.py: class AutorizationLogic _create_main_screen()')

        if self.screen_manager.has_screen(name='main_screen'):
            self.screen_constructor.popup_screen = self.screen_manager.get_screen('main_screen').children[0].ids['_front_layer'].children[0].children[0].children[0]
        else:
            self.screen_constructor.add_main_screen_obj(
                user_name = self.authorization_obj.user_name.text,
                user_surname = self.authorization_obj.user_surname.text,
                screen_constructor = self.screen_constructor,
            )
            self.screen_constructor.popup_screen = self.screen_manager.get_screen('main_screen').children[0].ids['_front_layer'].children[0].children[0].children[0]

    def seach_user_in_base(self):
        """# Проверка пользователя в базе данных
        - Если пользователь в базе данных, то вывести его данные
        - Если нельзя найти совпадений по login и password, то заводим нового пользователя
        """
        dev.logger.info('logic.py: class AutorizationLogic seach_user_in_base()')

        if self.get_permission(self.login, self.password): # проверяю пароль
            # прошли авторизацию
            self.authorization_obj.user_authorized = True
            self._create_main_screen()
        else:
            # не зарегистрированный пользователь
            self.authorization_obj.user_authorized = False
            pass # ничего не делаю если пользователь не авторизирован
        
        dev.logger.debug(f'-: user_authorized = {self.authorization_obj.user_authorized}')
 
    def set_user(self) -> None:
        """Вызов этой функции из интерфейса пользователя.
        Исходя из того, что написано в полях ввода,
        составляю представление о пользователе"""
        dev.logger.info('screens.py: class Autorization(MDScreen) set_user()')

        _login = self.authorization_obj.user_name.text.replace(' ', '')
        _password = self.authorization_obj.user_surname.text.replace(' ', '')

        if _login != '' and _password != '':
            dev.logger.info(f"DEBUG: Have Login and Password: '{_login}' '{_password}'")
            self.login = _login
            self.password = _password
            self.seach_user_in_base()
        else:
            dev.logger.warning(f"DEBUG: Have NOT Login and Password: '{_login}' '{_password}'")
            pass

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')


class MainScreenLogic:
    """Логика главного экрана"""

    dialog_screen_to_set_godziny = None
    dialog_screen_to_set_object = None

    def __init__(self,
                 screen_constructor,
                 screen_manager,
                 main_screen: MDScreen,
                 ) -> None:
        self.screen_manager = screen_manager
        self.screen_constructor = screen_constructor # ScreensConstructor()
        
        self.main_screen = main_screen # class Main(MDScreen)

        self.widgets: AddHoursWidget = None

    # def process_of_view_table(self):
    #     "Добавление таблицы во вкладку главного экрана"
    #     def spiner_screen():
    #         return MDSpinner(
    #             size_hint = (None, None),
    #             size = (46, 46),
    #             pos_hint = {'center_x': .5, 'center_y': .5},
    #             active = True,
    #         )

    #     spiner = spiner_screen()
    #     self.popup_screen.add_widget(spiner) # add to FloatLayout
    #     Clock.schedule_once(create_table, 1.6)

    def select_godziny(self):
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

    def make_data_table(self):
        dev.logger.info('screens.py: class Main(MDScreen) make_data_table()')

        user_data = None
        if user_data:
            print('Есть данные')
        else:
            print('Нет данных о пользователе')

    def on_click_table_row(self, widget):
        "Функция отрабатывает по клику на строку таблицы"
        print('--- on_click_item ---')
        print('wdiget.text:', widget.text, 'left_label.text:',  widget.ids.left_label.text, 'right_button.text:',  widget.ids.right_button.text)

    def on_click_table_right_button(self, widget):
        "Функция отрабатывает по клику на дату"
        print('--- on_click_right_button ---')
        print('wdiget.text:',  widget.text)
        print('widget.parent.parent:', widget.parent.parent)
        print('widget.parent.parent.text:', widget.parent.parent.text)

    def on_save_calendar(self, value):
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
        #         "text": f"Renoma",
        #         "text": f"Żarów",
        #         "text": f"Rędzin",
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

