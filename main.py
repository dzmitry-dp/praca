from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp

import dev
from dev import config
from dev.build import ScreensConstructor

Builder.load_file(config.PATH_TO_KV_FILE)

class PracaApp(MDApp):
    """
    - self.screen_root = kivy.uix.screenmanager.ScreenManager()
    - self.screen_constructor = dev.view.build.ScreenConstrucrot()

    def build() - возвращает корневой виджет приложения
    """

    def build(self):
        self.theme_cls.theme_style = "Dark"

        dev.logger.info('Start: ------------ PracaApp.build() ------------')
        self.screen_root = ScreenManager()
        self.screen_constructor = ScreensConstructor(self.screen_root)
        self.screen_constructor.start_building()
        dev.logger.info('End: ------------ PracaApp.build() ------------')

        return self.screen_root

if __name__ == "__main__":
    app = PracaApp()
    app.run()
