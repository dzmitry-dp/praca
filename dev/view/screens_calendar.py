from datetime import date, timedelta

from kivy.event import EventDispatcher
from kivy.metrics import dp

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton

import dev
from dev.view.screens_helper import DateButton


class DatePicker(BoxLayout, EventDispatcher):
    def __init__(self, *args, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.register_event_type("on_select")
        self.date = date.today()
        self.days = (
            "Pon",
            "Wto",
            "Śro",
            "Сzw",
            "Pią",
            "Sob",
            "Nie"
        )
        self.orientation = "vertical"
        self.month_names = (
            'Styczeń',
            'Luty',
            'Marzec',
            'Kwiecień',
            'Maj',
            'Czerwiec',
            'Lipiec',
            'Sierpień',
            'Wrzesień',
            'Październik',
            'Listopad',
            'Grudzień'
        )
        if "month_names" in kwargs:
            self.month_names = kwargs['month_names']
        self.header = BoxLayout(orientation='horizontal',
                                size_hint=(1, 0.2))
        self.body = GridLayout(cols=7, spacing=dp(20))
        self.add_widget(self.header)
        self.add_widget(self.body)

        self.populate_body()
        self.populate_header()

    def populate_header(self, *args, **kwargs):
        self.header.clear_widgets()
        previous_month = MDRaisedButton(text="<", pos_hint={"center_y": .5}, on_release=self.move_previous_month)
        previous_month.bind()
        next_month = MDRaisedButton(text=">", on_release=self.move_next_month, pos_hint={"center_y": .5})
        month_year_text = self.month_names[self.date.month - 1] + ' ' + str(self.date.year)
        current_month = Label(text=month_year_text, size_hint=(2, 1), color=[1, 1, 1, 1])

        self.header.add_widget(previous_month)
        self.header.add_widget(current_month)
        self.header.add_widget(next_month)

    def populate_body(self, *args, **kwargs):
        self.body.clear_widgets()
        date_cursor = date(self.date.year, self.date.month, 1)
        for day in self.days:
            self.body.add_widget(Label(text=day, color=[1, 1, 1, 1]))
        for filler in range(date_cursor.isoweekday() - 1):
            self.body.add_widget(Label(text=""))
        while date_cursor.month == self.date.month:
            date_label = DateButton(text=str(date_cursor.day), group="date")
            date_label.bind(
                on_release=lambda x, _date=int(date_label.text): self.set_date(
                    day=date(self.date.year, self.date.month, _date)
                )
            )
            if self.date.day == date_cursor.day:
                date_label.state = "down"
            self.body.add_widget(date_label)
            date_cursor += timedelta(days=1)

    def set_date(self, day):
        self.date = day
        self.dispatch("on_select", day)

    def on_select(self, day):
        pass

    def move_next_month(self, *args, **kwargs):
        if self.date.month == 12:
            self.date = date(self.date.year + 1, 1, self.date.day)
        else:
            self.date = date(self.date.year, self.date.month + 1, self.date.day)
        self.populate_header()
        self.populate_body()

    def move_previous_month(self, *args, **kwargs):
        if self.date.month == 1:
            self.date = date(self.date.year - 1, 12, self.date.day)
        else:
            self.date = date(self.date.year, self.date.month - 1, self.date.day)
        self.populate_header()
        self.populate_body()


class CalendarLogic:
    def __init__(self, screen_manager, screen_constructor) -> None:
        dev.logger.info('screens_calendar.py: class CalendarLogic __init__()')
        self.screen_manager = screen_manager
        self.screen_constructor = screen_constructor

    def back_from_calendar_to_main_screen(self):
        dev.logger.info('screens_calendar.py: class CalendarLogic back_from_calendar_to_main_screen()')