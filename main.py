from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp

import dev.action as action
import dev.config as config
from dev.build import ScreensConstructor

Builder.load_file(config.PATH_TO_KV_FILE)

class PracaApp(MDApp):
    """
    self.screen_root = kivy.uix.screenmanager.ScreenManager()

    self.screen_constructor = dev.view.build.ScreenConstrucrot()
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager: ScreenManager = None
        self.screen_constructor: ScreensConstructor = None

    def build(self) -> ScreenManager:
        self.theme_cls.theme_style = "Dark"

        action.logger.info('Start: ------------ PracaApp.build() ------------')
        self.screen_manager = ScreenManager()
        self.screen_constructor = ScreensConstructor(self.screen_manager)
        action.logger.info('End: ------------ PracaApp.build() ------------')

        return self.screen_manager

if __name__ == "__main__":
    app = PracaApp()
    app.run()
