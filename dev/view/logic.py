from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.datatables import MDDataTable

import dev
import dev.db.memory as memory
import dev.config as config
import dev.db.queries_struct as queries
from dev.exceptions import DBConnectionErr


class VerificationData:

    def get_permission(self, login, password) -> bool:
        query_obj = memory.Query(
            db_path=config.PATH_TO_USER_DB,
            )

        try:
            # Проверка на то, что пользователь в базе данных
            dev.logger.info('DB request: SELECT * FROM table_name WHERE name = login AND surname = surname;')
            
            all_data_from_db = query_obj.query_select_user(
                table_name=queries.USER_BASE,
                name=login,
                surname=password,
                )

            dev.logger.info(f'DB answer:{all_data_from_db}')

            if len(all_data_from_db) == 0:
                # если ответ из базы -> []
                query_obj.write_values(data=queries.generate_first_data(self._login, self._password))
                dev.logger.info('class VerificationData: update user data')
                all_data_from_db = query_obj.query_select_user(
                    table_name=queries.USER_BASE,
                    name=self._login,
                    surname=self._password,
                    ) # запрашиваем данные у которых логин и пароль\
                # совпадают с данными которые ввел пльзователь

        except DBConnectionErr:
            # Если таблица еще не создана

            dev.logger.info('Create new table:')
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
            return False


class AutorizationLogic(VerificationData):
    """Вся логика авторизации пользователя
    """
    def __init__(self, screen_constructor, screen_manager, authorization_obj: MDScreen) -> None:
        super().__init__()
        self._login = None
        self._password = None

        self.screen_constructor = screen_constructor # ScreensConstructor()
        self.screen_manager = screen_manager # ScreenManager()
        self.authorization_obj = authorization_obj # Autorization(MDScreen)
        
        dev.logger.info('class AutorizationLogic: __init__()')

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
        dev.logger.info('class AutorizationLogic(VerificationData): _no_password_reaction()')

    def _create_main_screen(self):
        """Создаю главный экран после авторизации пользователя, если экран не создан
        self.screen_constructor.popup_screen - подвижная вкладка
        """
        dev.logger.info('class AutorizationLogic(VerificationData): _create_main_screen()')

        if self.screen_manager.has_screen(name='screen_one'):
            self.screen_constructor.popup_screen = self.screen_manager.get_screen('screen_one').children[0].ids['_front_layer'].children[0].children[0].children[0]
        else:
            self.screen_constructor.add_main_screen_obj(
                user_name = self.authorization_obj.user_name.text,
                user_surname = self.authorization_obj.user_surname.text,
                screen_constructor = self.screen_constructor,
            )
            self.screen_constructor.popup_screen = self.screen_manager.get_screen('screen_one').children[0].ids['_front_layer'].children[0].children[0].children[0]

    def seach_user_in_base(self):
        """# Проверка пользователя в базе данных
        - Если пользователь в базе данных, то вывести его данные
        - Если нельзя найти совпадений по login и password, то заводим нового пользователя
        """
        dev.logger.info('class AutorizationLogic(VerificationData): seach_user_in_base()')

        if self.get_permission(self.login, self.password): # проверяю пароль
            # прошли авторизацию
            dev.logger.info(f'class Autorization(Screen): user_authorized = True')
            self.authorization_obj.user_authorized = True
            self._create_main_screen()
        else:
            # не зарегистрированный пользователь
            dev.logger.info(f'class Autorization(Sceen): user_authorized = False')
            self.authorization_obj.user_authorized = False
            pass # ничего не делаю если пользователь не авторизирован
 

class MainScreenLogic:
    """Логика главного экрана"""
    def __init__(self,
                 main_screen: MDScreen,
                 screen_manager,
                 screen_constructor,
                 ) -> None:
        self.screen_manager = screen_manager
        self.screen_constructor = screen_constructor # ScreensConstructor()
        
        self.main_screen = main_screen # class Main(MDScreen)

        # self.table: MDDataTable = None # таблица часов
        # self.add_hour_ui = None # интерфейс для добавления часов в базу данных

    # def process_of_view_table(self):
    #     "Добавление таблицы во вкладку главного экрана"
    #     def spiner_screen():
    #         return MDSpinner(
    #             size_hint = (None, None),
    #             size = (46, 46),
    #             pos_hint = {'center_x': .5, 'center_y': .5},
    #             active = True,
    #         )

    #     def create_table(dt):
    #         if self.table != None:
    #             self.popup_screen.remove_widget(self.table)
    #         self.popup_screen.remove_widget(spiner)

    #         self.table = MDDataTable(
    #             column_data=[
    #                 ("No.", 28),
    #                 ("Data", 76),
    #                 ("Godziny", 46),
    #                 ("Budowa", 46),
    #                 ("Godziny jazdy", 132),
    #                 ("Samochód służbowy", 132),
    #                 ("Start, km", 60),
    #                 ("Stop, km", 60),
    #                 ("Cała droga, km", 132),
    #             ],
    #             row_data=[
    #                 (
    #                     "1",
    #                     "1.01.2023",
    #                     "8",
    #                     "Renoma",
    #                     "0",
    #                     "Nie",
    #                     "",
    #                     "",
    #                     "",
    #                 ),
    #                 (
    #                     "2",
    #                     "2.01.2023",
    #                     "10",
    #                     "Żarów",
    #                     "2",
    #                     "Tak",
    #                     "283415",
    #                     "283515",
    #                     "100",
    #                 ),
    #                 (
    #                     "3",
    #                     "3.01.2023",
    #                     "12",
    #                     "Renoma",
    #                     "0",
    #                     "Nie",
    #                     "",
    #                     "",
    #                     "",
    #                 ),
    #                 (
    #                     "4",
    #                     "4.01.2023",
    #                     "8",
    #                     "Jaz Rędzin",
    #                     "2",
    #                     "Tak",
    #                     "283415",
    #                     "283515",
    #                     "100",
    #                 ),
    #                 (
    #                     "5",
    #                     "5.01.2023",
    #                     "12",
    #                     "Jaz Rędzin",
    #                     "2",
    #                     "Tak",
    #                     "283415",
    #                     "283515",
    #                     "100",
    #                 ),
    #             ],
    #         )
    #         self.popup_screen.add_widget(self.table) # add to FloatLayout
        
    #     spiner = spiner_screen()
    #     self.popup_screen.add_widget(spiner) # add to FloatLayout
    #     Clock.schedule_once(create_table, 1.6)

    # def process_of_add_hour(self, add_hours_ui_obj):
    #     "Вкладка с интерфейсом которыйдобавляет часы в базу данных"
        
    #     self.add_hour_ui = add_hours_ui_obj() # сборка AddHours()
    #     self.popup_screen.add_widget(self.add_hour_ui)

    def process_of_view_btn_menu(self):
        # self.screen_constructor.btn_sheet_menu = MyButtonSheet(
        #     screen_constructor=self.screen_constructor,
        #     screen_manager=self.screen_manager,
        # )
        # self.screen_constructor.btn_sheet_menu.open()
        dev.logger.info('class MainScreenLogic: process_of_vuew_btn_menu() -> None')