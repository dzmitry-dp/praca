from os.path import abspath

PATH_TO_KV_FILE = abspath('./dev/view/praca.kv')
PATH_TO_USER_DB = abspath('./dev/db/user.db')

# PHONE_NUMBER = '48663215343' # Жека
PHONE_NUMBER = '48577655470'

from kivy.core.window import Window

Window.top = 75
Window.left = 75
Window.size = (405, 810)

from kivy.config import Config
import os

Config.set('kivy', 'log_dir', os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath('static/logs')))