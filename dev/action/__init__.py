from kivy.logger import Logger as logger

from kivy.utils import platform

if platform == 'android':
    from android.permissions import Permission, request_permissions
    from jnius import autoclass

    request_permissions([
        Permission.INTERNET,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.SEND_SMS,
        ])

    # Отправляю СМС
    # SmsManager = autoclass('android.telephony.SmsManager')
