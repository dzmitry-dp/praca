import os
from os.path import abspath

from kivy.core.window import Window
from kivy.config import Config
from kivy.utils import platform

if platform != 'android':
    Window.top = 75
    Window.left = 75
    Window.size = (405, 810)

Config.set('graphics', 'maxfps', '120')
# Config.set('kivy', 'log_dir', os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath('./dev/static/logs')))

payment_day = 15 # день зарплаты

PATH_TO_KV_FILE = abspath('./dev/view/praca.kv')

PATH_TO_REMEMBER_ME = abspath('./dev/db/freeze')
if not os.path.exists(PATH_TO_REMEMBER_ME):
    os.makedirs(PATH_TO_REMEMBER_ME)

PATH_TO_USER_DB = abspath('./dev/db/user')
if not os.path.exists(PATH_TO_USER_DB):
    os.makedirs(PATH_TO_USER_DB)

PATH_TO_EMPLOYER_DB = abspath('./dev/db/employer') # только скачиваем с сервера
if not os.path.exists(PATH_TO_EMPLOYER_DB):
    os.makedirs(PATH_TO_EMPLOYER_DB)

# PHONE_NUMBER = '48663215343' # Жека
PHONE_NUMBER = '48577655470'

# user.db
FIRST_TABLE = 'godziny'

# employer.db
WORKER_TABLE = 'worker' # список работников фирмы
PROJECT_TABLE = 'project' # список объектов для работников


SERVER = "64.226.119.172"
PORT = 1489 # порт к серверу, который принимает шифрованные сообщения

if not os.path.exists(abspath('./dev/static/.ssl')):
    os.makedirs(abspath('./dev/static/.ssl'))

CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        abspath("./dev/static/.ssl/public.crt")))