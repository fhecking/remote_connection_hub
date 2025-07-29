import os
from datetime import datetime

def get_new_output_dir(base):
    today = datetime.now().strftime("%Y%m%d")
    counter = 1
    while True:
        dir_name = f"{base}/{today}_{counter}"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            return dir_name
        counter += 1