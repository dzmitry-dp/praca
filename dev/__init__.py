import os

from kivy.logger import Logger as logger
from kivy.config import Config

from kivy.utils import platform

if platform == 'android':
    from android.permissions import Permission, request_permissions
    from jnius import autoclass

    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.SEND_SMS,
        ])

    # Отправляю СМС
    SmsManager = autoclass('android.telephony.SmsManager')

Config.set('kivy', 'log_dir', os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath('static/logs')))

### Пример использования logger
# logger.info('title: ++++++++++++++.')

# try:
#     raise Exception('Ошибка')
# except Exception:
#     logger.exception('!!!!!!!!!!!!!!!!!!')



