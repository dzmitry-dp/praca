from kivy.properties import NumericProperty, StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBody, IRightBodyTouch
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.list import OneLineIconListItem


class Widgets(MDBoxLayout):
    progress = NumericProperty()

    def __init__(self, main_screen_logic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_screen_logic = main_screen_logic


# главная таблица
class MyItemList(OneLineAvatarIconListItem):
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

