import json

from kivy.properties import NumericProperty, StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBody, IRightBodyTouch, IconLeftWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.button import MDRectangleFlatButton

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

    def press_left(self):
        hours_value = int(self.widget.ids.current_hours_value.text)
        if hours_value > 0 and hours_value <= 24:
            _ = hours_value - 1
            self.widget.ids.hours_line_data.value = _
            self.widget.ids.current_hours_value.text = str(_)

    def press_right(self):
        hours_value = int(self.widget.ids.current_hours_value.text)
        if hours_value >= 0 and hours_value < 24:
            _ = hours_value + 1
            self.widget.ids.hours_line_data.value = _
            self.widget.ids.current_hours_value.text = str(_)


class ObjectsActions:
    def __init__(self, widget, main_screen, screen_constructor) -> None:
        action.logger.info('my_widgets.py: class ObjectsActions __init__()')
        self.widget = widget
        self.main_screen = main_screen
        self.screen_constructor = screen_constructor

    def _write_freeze_file(self):
        action.logger.info(f"my_widgets.py: class ObjectsActions _add_objects_in_list() _write_freeze_file()")
        with open(self.screen_constructor.data_from_memory.path_to_freeze_file, 'w') as file:
            json.dump(self.screen_constructor.data_from_memory.freeze_file_data, file)
    
    def remove_obj_from_list(self, value = None):
        for item in self.widget.ids.objects_list.children:
            if item.children[0].text == value.text:
                self.widget.ids.objects_list.remove_widget(item)

                self.screen_constructor.data_from_memory.freeze_file_data['work_places'].remove(value.text)
                self._write_freeze_file()

    def select_worker_object(self, value = None):
        obj_name = value.text
        self.widget.ids.current_object_value.hint_text = obj_name
        self.widget.ids.current_object_value.text = ''
    
    def _add_objects_in_list(self, obj_name):
        action.logger.info('my_widgets.py: class ObjectsActions _add_objects_in_list()')
        
        if self.screen_constructor.data_from_memory.freeze_file_data is not None:
            if obj_name not in self.screen_constructor.data_from_memory.freeze_file_data['work_places']:
                item = OneLineAvatarIconListItem(
                            MDRectangleFlatButton(
                                text = obj_name,
                                halign = 'center',
                                font_size = '16sp',
                                pos_hint = {'center_x': .65, 'center_y': .5},
                                size_hint_x = 0.9,
                                on_release = self.select_worker_object,
                                )
                            )
                item.add_widget(
                    IconLeftWidget(
                        icon = "close",
                        text = obj_name,
                        on_release = self.remove_obj_from_list,
                        )
                    )
                self.widget.ids.objects_list.add_widget(item)
                self.screen_constructor.data_from_memory.freeze_file_data['work_places'].append(obj_name)
                self._write_freeze_file()

    def _change_obj_btn(self, obj_name):
        action.logger.info('my_widgets.py: class ObjectsActions _change_obj_btn()')
        self.main_screen.ids.obiekt.icon = ''  
        self._add_objects_in_list(obj_name)

        if len(obj_name) > 6:
            obj_name = obj_name[:5] + '...'

        self.main_screen.ids.obiekt.text = obj_name

    def press_ok(self):
        action.logger.info('my_widgets.py: class ObjectsActions press_ok()')
        if self.widget.ids.current_object_value.text == '':
            obj_name = self.widget.ids.current_object_value.hint_text
            if obj_name == 'Miejsce pracy':
                return None
        else:
            obj_name = self.widget.ids.current_object_value.text
            self.widget.ids.current_object_value.hint_text = obj_name
            self.widget.ids.current_object_value.text = ''

        self._change_obj_btn(obj_name)


class WorkObjects(MDBoxLayout):
    widget_height = NumericProperty()
    widget_width = NumericProperty()

    def __init__(self, screen_constructor, main_screen, main_screen_logic, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        action.logger.info('my_widgets.py: class WorkObjects __init__()')
        self.screen_constructor = screen_constructor
        self.main_screen = main_screen
        self.main_screen_logic = main_screen_logic
        self._objects = None

        self.widget_height = Window.size[0]
        self.widget_width = Window.size[1]

    @property
    def objects(self):
        if self._objects is None:
            self._objects = ObjectsActions(
                widget = self,
                main_screen = self.main_screen,
                screen_constructor = self.screen_constructor,
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
