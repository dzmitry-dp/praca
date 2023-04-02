import os, sys
from dirsync import sync


# жестко прописанные пути
source_path = 'C:\\Users\\dp\\OneDrive\\Personal\\Projects\\Praca'
target_path = '\\\\wsl.localhost\\Ubuntu\\home\\dp\\Personal\\Projects\\Praca\\dev_app'

if os.path.exists(target_path):
    # удаляем __pycache__
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'pyclean {cur_dir}')
    # синхронизируем
    args = {
    'exclude':[
        '.*\.git',
        '.*\.venv',
        '^.*\.csv$',
        '^.*\.log$',
        '^.*\.md$',
        '^.*\.txt$',
        'sync.py'
        ],
    }

    sync(source_path, target_path, 'sync', purge=True, verbose=True, **args)
else:
    print('[x] Error! Have not target path')
    sys.exit()
