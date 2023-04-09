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

    def add_8_godzin(self):
        dev.logger.info('screens_helper.py: class AddHoursActions() add_8_godzin()')
        self.widget.ids.hours_line_data.value = 8

    def add_10_godzin(self):
        dev.logger.info('screens_helper.py: class AddHoursActions() add_10_godzin()')
        self.widget.ids.hours_line_data.value = 10

    def add_12_godzin(self):
        dev.logger.info('screens_helper.py: class AddHoursActions() add_12_godzin()')
        self.widget.ids.hours_line_data.value = 12

    def press_ok(self):
        dev.logger.info('screens_helper.py: class AddHoursActions() press_ok()')
        self.main_screen.ids.godziny.icon = ''
        self.main_screen.ids.godziny.text = str(int(self.hours_progress))


class ObjectsActions:
    def __init__(self, main_screen) -> None:
        self.main_screen = main_screen

    def _change_obj_btn(self, value):
        dev.logger.info('screens_helper.py: class ObjectsActions() _change_obj_btn()')
        self.main_screen.ids.obiekt.icon = ''
        self.main_screen.ids.obiekt.text = value       
    
    def reaction_on_renoma(self):
        dev.logger.info('screens_helper.py: class ObjectsActions() reaction_on_renoma()')
        self._change_obj_btn('Renoma')

    def reaction_on_zarow(self):
        dev.logger.info('screens_helper.py: class ObjectsActions() reaction_on_zarow()')
        self._change_obj_btn('Żarów')
        print('Żarów')

    def reaction_on_redzin(self):
        dev.logger.info('screens_helper.py: class ObjectsActions() reaction_on_redzin()')
        self._change_obj_btn('Rędzin')
        print('Rędzin')


class WorkObjects(MDBoxLayout):
    widget_height = NumericProperty()
    widget_width = NumericProperty()

    def __init__(self, main_screen, main_screen_logic, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.main_screen = main_screen
        self.main_screen_logic = main_screen_logic
        self._objects_reaction = None

        self.widget_height = Window.size[0]*0.7
        self.widget_width = Window.size[1]*0.5

    @property
    def objects(self):
        self._objects_reaction = ObjectsActions(
            main_screen = self.main_screen,
        )
        return self._objects_reaction


class AddHoursWidget(MDBoxLayout):
    progress_hours_line = NumericProperty() # количество часов от 0 до 24
    widget_height = NumericProperty()
    widget_width = NumericProperty()

    def __init__(self, main_screen, main_screen_logic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_screen = main_screen
        self.main_screen_logic = main_screen_logic
        self._add_hour_reaction = None
        
        self.widget_height = Window.size[0]*0.7
        self.widget_width = Window.size[1]*0.5

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
