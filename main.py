### from book
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp

import dev
from dev import config
from dev.view.build import ScreensConstructor

Builder.load_file(config.PATH_TO_KV_FILE)

class PracaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        dev.logger.info('Start: ------------ PracaApp.build() ------------')
        self.screen_manager = ScreenManager()
        self.screen_constructor = ScreensConstructor(self.screen_manager)
        self.screen_constructor.add_authorization_screen_obj()
        dev.logger.info('End: ------------ PracaApp.build() ------------')

        return self.screen_manager

if __name__ == "__main__":
    app = PracaApp()
    app.run()
