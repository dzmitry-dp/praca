import os, sys
from dirsync import sync


# жестко прописанные пути
source_path = 'C:\\Users\\dp\\OneDrive\\Personal\\Projects\\Praca'
target_path = '\\\\wsl.localhost\\Ubuntu\\home\\dp\\Personal\\Projects\\Praca\\dev'

if os.path.exists(target_path):
    # удаляем __pycache__
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'pyclean .')
    # синхронизируем
    args = {
    'exclude':[
        '.*\.git',
        '.*\.venv',
        '^.*\.csv$',
        '^.*\.log$',
        '^.*\.md$',
        '^.*\.txt$',
        '^.*\.apk$',
        'Praca.code-workspace',
        'sync.py',
        '.ssh',
        'scripts',
        'dev/static/android_app',
        'dev/static/logs',
        'dev/static/doc',
        'dev/static/wallpapers',
        ],
    }

    sync(source_path, target_path, 'sync', purge=True, verbose=True, **args)
else:
    print('[x] Error! Have not target path')
    sys.exit()

###
os.system(f'move {target_path}\\buildozer.spec {target_path[:-4]}\\buildozer.spec')
os.system(f'move {target_path}\\scripts\\create_app.py {target_path[:-4]}\\create_app.py')
