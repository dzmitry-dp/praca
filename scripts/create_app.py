import os
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
os.system(f'buildozer android debug && mv /home/dp/Personal/Projects/Praca/bin/Rokbit-0.6-arm64-v8a_armeabi-v7a-debug.apk /mnt/c/Users/dp/OneDrive/Personal/Projects/008_Praca/dev/static/android_app/PracaApp_Rokbit_{date_time}.apk')
