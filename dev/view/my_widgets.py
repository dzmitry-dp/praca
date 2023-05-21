from kivy.properties import NumericProperty, StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBody, IRightBodyTouch
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.list import OneLineIconListItem

from dev.config import Window
import dev.action as action


class AddHoursActions:
    def __init__(self, widget, hours_progress, main_screen) -> None:
        action.logger.info('my_widgets.py: class AddHoursActions __init__()')
        self.widget = widget
        self.hours_progress = hours_progress
        self.main_screen = main_screen

    def add_8_godzin(self, value = 8):
        action.logger.info('my_widgets.py: class AddHoursActions add_8_godzin()')
        self.widget.ids.hours_line_data.value = 8
        self.widget.ids.current_hours_value.text = str(int(value))

    def add_10_godzin(self, value = 10):
        action.logger.info('my_widgets.py: class AddHoursActions add_10_godzin()')
        self.widget.ids.hours_line_data.value = 10
        self.widget.ids.current_hours_value.text = str(int(value))

    def add_12_godzin(self, value = 12):
        action.logger.info('my_widgets.py: class AddHoursActions add_12_godzin()')
        self.widget.ids.hours_line_data.value = 12
        self.widget.ids.current_hours_value.text = str(int(value))

    def add_0_godzin(self, value = 0):
        action.logger.info('my_widgets.py: class AddHoursActions add_0_godzin()')
        self.widget.ids.hours_line_data.value = 0
        self.widget.ids.current_hours_value.text = str(int(value))

    def add_24_godziny(self, value = 24):
        action.logger.info('my_widgets.py: class AddHoursActions add_24_godziny()')
        self.widget.ids.hours_line_data.value = 24
        self.widget.ids.current_hours_value.text = str(int(value))

    def press_ok(self, value):
        action.logger.info('my_widgets.py: class AddHoursActions press_ok()')
        self.main_screen.ids.godziny.icon = ''
        self.main_screen.ids.godziny.text = str(int(value))
        self.main_screen.logic.dialog_screen_to_set_godziny.dismiss()

    def set_current_value(self, value):
        action.logger.info('my_widgets.py: class AddHoursActions set_current_value()')
        self.widget.ids.current_hours_value.text = str(int(value))


class ObjectsActions:
    def __init__(self, widget, main_screen) -> None:
        action.logger.info('my_widgets.py: class ObjectsActions __init__()')
        self.widget = widget
        self.main_screen = main_screen

    def _change_obj_btn(self, value):
        action.logger.info('my_widgets.py: class ObjectsActions _change_obj_btn()')
        if value != '':
            self.main_screen.ids.obiekt.icon = ''
            if len(value) > 10:
                value = value[:10]

            self.main_screen.ids.obiekt.text = value       
    
    def reaction_on_renoma(self):
        action.logger.info('my_widgets.py: class ObjectsActions reaction_on_renoma()')
        if self.widget.ids.current_object_value.text != '':
            self.widget.ids.current_object_value.text = ''

        self.widget.ids.current_object_value.hint_text = 'Renoma'

    def reaction_on_zarow(self):
        action.logger.info('my_widgets.py: class ObjectsActions reaction_on_zarow()')
        if self.widget.ids.current_object_value.text != '':
            self.widget.ids.current_object_value.text = ''

        self.widget.ids.current_object_value.hint_text = 'Żarów'

    def reaction_on_redzin(self):
        action.logger.info('my_widgets.py: class ObjectsActions reaction_on_redzin()')
        if self.widget.ids.current_object_value.text != '':
            self.widget.ids.current_object_value.text = ''

        self.widget.ids.current_object_value.hint_text = 'Rędzin'
    
    def press_ok(self):
        action.logger.info('my_widgets.py: class ObjectsActions press_ok()')
        if self.widget.ids.current_object_value.text == '':
            obj_name = self.widget.ids.current_object_value.hint_text
        else:
            obj_name = self.widget.ids.current_object_value.text
            self.widget.ids.current_object_value.hint_text = obj_name
            self.widget.ids.current_object_value.text = ''
        
        self._change_obj_btn(obj_name)


class WorkObjects(MDBoxLayout):
    widget_height = NumericProperty()
    widget_width = NumericProperty()

    def __init__(self, main_screen, main_screen_logic, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        action.logger.info('my_widgets.py: class WorkObjects __init__()')
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
        action.logger.info('my_widgets.py: class AddHoursWidget __init__()')
        self.main_screen = main_screen
        self.main_screen_logic = main_screen_logic
        self.hour_reaction = AddHoursActions(
            widget = self,
            hours_progress = self.progress_hours_line,
            main_screen = self.main_screen,
        )
        
        self.widget_height = Window.size[0]
        self.widget_width = Window.size[1]

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
