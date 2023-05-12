from kivy.core.window import Window

# Window.top = 75
# Window.left = 75
# Window.size = (405, 810)

from kivy.config import Config
import os

Config.set('kivy', 'log_dir', os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath('./dev/static/logs')))

from os.path import abspath

PATH_TO_KV_FILE = abspath('./dev/view/praca.kv')
PATH_TO_REMEMBER_ME = abspath('./dev/db/freeze')
PATH_TO_USER_DB = abspath('./dev/db/user')
PATH_TO_EMPLOYER_DB = abspath('./dev/db/employer/rockbit.db') # только скачиваем с сервера

# PHONE_NUMBER = '48663215343' # Жека
PHONE_NUMBER = '48577655470'

# user.db
FIRST_TABLE = 'godziny'

# employer.db
WORKER_TABLE = 'worker' # список работников фирмы
PROJECT_TABLE = 'project' # список объектов для работников


SERVER = "64.226.119.172"
PORT = 1489 # порт к серверу, который принимает шифрованные сообщения
CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "./static/.ssl/public.crt"))