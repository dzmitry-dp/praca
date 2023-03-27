import dev
from dev.view.screens import Autorization, Main


class ScreensConstructor:
    """Сборщик рабочих экранов для пользователей"""
    def __init__(self, screen_manager) -> None:
        dev.logger.info('class ScreensConstructor: __init__()')
        # Управление
        self.screen_manager = screen_manager # ScreenManager()
        # Мои экраны
        self.authorization_screen = None # screen_zero
        self.main_screen = None # screen_one
        # Дополнительные элементы
        self.popup_screen = None # попап MDBackdropFrontLayer
        # self.btn_sheet_menu = None # виджет на экране 'screen_one'
        # self.dilog_screen = None # всплывающее окно в вопросом к пользователю


    def add_authorization_screen_obj(self):
        dev.logger.info('class ScreensConstructor: add_authorization_screen_obj()')
        "Создаю и добавляю экран авторизации"
        self.authorization_screen = Autorization(
                name='screen_zero',
                screen_constructor = self,
                screen_manager=self.screen_manager
            )
        self.screen_manager.add_widget(self.authorization_screen)
    
    def add_main_screen_obj( # screen_one
            self,
            user_name,
            user_surname,
            screen_constructor,
            ):
        "Создаю и добавляю главный экран приложения"
        dev.logger.info('class ScreensConstructor: add_main_screen_obj()')
        self.main_screen = Main(
                name = 'screen_one',
                user_name = user_name,
                user_surname = user_surname,
                screen_constructor = screen_constructor,
                screen_manager = self.screen_manager
            )
        self.screen_manager.add_widget(self.main_screen)

    def remove_screen_one(self) -> None:
        dev.logger.info('class ScreensConstructor: remove_screen_one()')
        self.screen_manager.remove_widget(self.main_screen)
        self.main_screen = None


    # def build_some_question_obj(self, obj) -> MDDialog:
    #     return MDDialog(
    #         text="Czy chcecie wysłać SMS ?",
    #         radius=[10, 10, 10, 10],
    #         buttons=[
    #             MDRectangleFlatButton(
    #                 text="Tak",
    #                 on_release=obj.btn_tak_call,
    #                 padding=10,
    #             ),
    #             MDRectangleFlatButton(
    #                 text="Nie",
    #                 on_release=obj.btn_nie_call,
    #                 padding=10,
    #             ),
    #         ],
    #     )

    # def load_error(self, msg: str) -> None:
    #     "Выводит на экран ошибку"
    #     kivytoast.toast(msg)

    # def create_btn_menu(self):
    #     # self.btn_sheet_menu = MDGridBottomSheet()
    #     # self.btn_sheet_menu = self.ids.grid_botton # MDGridBottomSheet id: grid_botton
    #     if self.btn_sheet_menu is None:
    #         self.btn_sheet_menu = MyButtonSheet( # widget on screen_one
    #             screen_constructor = self,
    #             screen_manager = self.screen_manager,
    #         )
    #         data = {
    #             "Dodać": "timer-plus-outline",
    #             "SMS": "message-processing",
    #             "Edytuj": "table-edit",
    #             "Tabela": "table-arrow-up",
    #             "Pytać": "frequently-asked-questions",
    #             "Zadania": "format-list-checks",
    #         }

    #         for item in data.items():
    #             self.btn_sheet_menu.add_item(
    #                 item[0],
    #                 lambda x, y=item[0]: self._callback_for_menu_items(y),
    #                 icon_src=item[1],
    #             )
        
    #     return self.btn_sheet_menu

    # def _callback_for_menu_items(self, *args):
    #     def _check_view():
    #         """Проверяю что сейчас отражено в попапе.
    #         Если таблица, то обновляю данные"""

    #         if self.main_screen_logic.table == None:
    #             pass
    #         else: # если отображена таблица
    #             self.popup_screen.remove_widget(self.main_screen_logic.table)
            
    #         if self.main_screen_logic.add_hour_ui == None:
    #             pass
    #         else: # если отображен пользовательский интерфейс для добавления рабочих часов
    #             self.popup_screen.remove_widget(self.main_screen_logic.add_hour_ui)

    #     def add_hour():
    #         "Выполняется по нажатию на кнопку Dodać"
    #         _check_view() # поведение в зависимости от объектов которые отражены в popup
    #         self.main_screen_logic.process_of_add_hour(add_hours_ui_obj = AddHours)
    #         self.main_screen.children[0].open() # MDBackdrop.open()
    #         dev.logger.info('class Main(MDScreen): add_hour()')

    #     def sms_btn():
    #         "По нажатию кнопки формируется СМС и отправляется на единый номер"
    #         dev.logger.info('class Main(MDScreen): send_sms()')
    #         self.dilog_screen = self.build_some_question_obj(self)
    #         self.dilog_screen.open()

    #     def edit_data():
    #         "Предоставляет доступ к данным"
    #         dev.logger.info('class Main(MDScreen): edit_data()')

    #     def show_table():
    #         "Закрывает меню и показывает таблицу на MDBackdropFrontLayer"
    #         dev.logger.info('MDBackdrop open()')
    #         _check_view() # поведение в зависимости от объектов которые отражены в popup
    #         self.main_screen_logic.process_of_view_table()
    #         self.main_screen.children[0].open() # MDBackdrop.open()

    #     def add_question():
    #         dev.logger.info('add_question()')

    #     def view_tasks():
    #         dev.logger.info('view_tasks()')

    #     if args[0] == 'Dodać':
    #         add_hour()
    #     elif args[0] == 'SMS':
    #         sms_btn()
    #     elif args[0] == 'Edytuj':
    #         edit_data()
    #     elif args[0] == 'Tabela':
    #         show_table()

