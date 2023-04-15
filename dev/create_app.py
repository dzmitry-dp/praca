import os
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
os.system(f'buildozer android debug && mv /home/dp/Personal/Projects/Praca/bin/TEST-0.4-arm64-v8a_armeabi-v7a-debug.apk /mnt/c/Users/dp/OneDrive/Personal/Projects/Praca/dev/static/android_app/TestPraca_{date_time}.apk')
