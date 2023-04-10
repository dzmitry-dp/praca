from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.core.window import Window

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBody, IRightBodyTouch
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.card import MDCard

import dev

class AddHoursActions:
    def __init__(self, widget, hours_progress, main_screen) -> None:
        self.widget = widget
        self.hours_progress = hours_progress
        self.main_screen = main_screen

    def add_8_godzin(self, value = 8):
        dev.logger.info('screens_helper.py: class AddHoursActions() add_8_godzin()')
        self.widget.ids.hours_line_data.value = 8
        self.widget.ids.current_hours_value.text = str(int(value))

    def add_10_godzin(self, value = 10):
        dev.logger.info('screens_helper.py: class AddHoursActions() add_10_godzin()')
        self.widget.ids.hours_line_data.value = 10
        self.widget.ids.current_hours_value.text = str(int(value))

    def add_12_godzin(self, value = 12):
        dev.logger.info('screens_helper.py: class AddHoursActions() add_12_godzin()')
        self.widget.ids.hours_line_data.value = 12
        self.widget.ids.current_hours_value.text = str(int(value))

    def add_0_godzin(self, value = 0):
        dev.logger.info('screens_helper.py: class AddHoursActions() add_0_godzin()')
        self.widget.ids.hours_line_data.value = 0
        self.widget.ids.current_hours_value.text = str(int(value))

    def add_24_godziny(self, value = 24):
        dev.logger.info('screens_helper.py: class AddHoursActions() add_24_godziny()')
        self.widget.ids.hours_line_data.value = 24
        self.widget.ids.current_hours_value.text = str(int(value))

    def press_ok(self):
        dev.logger.info('screens_helper.py: class AddHoursActions() press_ok()')
        self.main_screen.ids.godziny.icon = ''
        self.main_screen.ids.godziny.text = str(int(self.hours_progress))

    def set_current_value(self, value):
        dev.logger.info('screens_helper.py: class AddHoursActions() set_current_value()')
        self.widget.ids.current_hours_value.text = str(int(value))

class ObjectsActions:
    def __init__(self, widget, main_screen) -> None:
        self.widget = widget
        self.main_screen = main_screen

    def _change_obj_btn(self, value):
        dev.logger.info('screens_helper.py: class ObjectsActions() _change_obj_btn()')
        if value != '':
            self.main_screen.ids.obiekt.icon = ''
            self.main_screen.ids.obiekt.text = value       
    
    def reaction_on_renoma(self):
        dev.logger.info('screens_helper.py: class ObjectsActions() reaction_on_renoma()')
        self.widget.ids.current_object_value.text = 'Renoma'

    def reaction_on_zarow(self):
        dev.logger.info('screens_helper.py: class ObjectsActions() reaction_on_zarow()')
        self.widget.ids.current_object_value.text = 'Żarów'

    def reaction_on_redzin(self):
        dev.logger.info('screens_helper.py: class ObjectsActions() reaction_on_redzin()')
        self.widget.ids.current_object_value.text = 'Rędzin'
    
    def press_ok(self):
        print(self.widget.ids.current_object_value.text)
        self._change_obj_btn(self.widget.ids.current_object_value.text)


class WorkObjects(MDBoxLayout):
    widget_height = NumericProperty()
    widget_width = NumericProperty()

    def __init__(self, main_screen, main_screen_logic, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.main_screen = main_screen
        self.main_screen_logic = main_screen_logic
        self._objects = None

        self.widget_height = Window.size[0]
        self.widget_width = Window.size[1]

    @property
    def objects(self):
        self._objects = ObjectsActions(
            widget = self,
            main_screen = self.main_screen,
        )
        return self._objects


class AddHoursWidget(MDBoxLayout):
    progress_hours_line = NumericProperty() # количество часов от 0 до 24
    widget_height = NumericProperty()
    widget_width = NumericProperty()

    def __init__(self, main_screen, main_screen_logic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_screen = main_screen
        self.main_screen_logic = main_screen_logic
        self._add_hour_reaction = None
        
        self.widget_height = Window.size[0]
        self.widget_width = Window.size[1]

    @property
    def add_hour(self):
        self._add_hour_reaction = AddHoursActions(
            widget = self,
            hours_progress = self.progress_hours_line,
            main_screen = self.main_screen,
        )

        return self._add_hour_reaction

# главная таблица
class TabelItem(OneLineAvatarIconListItem):
    '''Custom list item.'''
    pass


class LeftLabel(ILeftBody, MDLabel):
    '''Custom left container.'''
    pass


class RightButton(IRightBodyTouch, MDTextButton):
    '''Custom right container.'''
    pass


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class DateButton(MDCard, CommonElevationBehavior, ToggleButtonBehavior):
    text_color = ListProperty([1, 1, 1, 1])
    text = StringProperty("")

    def on_state(self, widget, value):
        if value == 'down':
            self.md_bg_color = self.theme_cls.primary_color
            self.text_color = [1, 1, 1, 1]
        else:
            self.md_bg_color = [0.12941176470588237, 0.12941176470588237, 0.12941176470588237, 1.0]
            self.text_color = [1, 1, 1, 1]
