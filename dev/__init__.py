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

    # PythonActivity = autoclass('org.kivy.android.PythonActivity')
    SmsManager = autoclass('android.telephony.SmsManager')

import os

from kivy.logger import Logger as logger
from kivy.config import Config

Config.set('kivy', 'log_dir', os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath('static/logs')))

### Пример использования logger
# logger.info('title: ++++++++++++++.')

# try:
#     raise Exception('Ошибка')
# except Exception:
#     logger.exception('!!!!!!!!!!!!!!!!!!')


def send_sms(phone_number, message):
    sms = SmsManager.getDefault()
    sms.sendTextMessage(phone_number, None, message, None, None)
