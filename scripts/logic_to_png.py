import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
os.system(
    f'code2flow . --language py --output {cur_dir[:-8]}\dev\static\logic.png'
    )

os.remove(f'{cur_dir[:-8]}\\dev\\static\\logic.gv')