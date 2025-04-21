import os
import shutil

def copy_content(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for object in os.listdir(src):
        filepath = os.path.join(src, object)
        dst_filepath = os.path.join(dst, object)
        if os.path.isfile(filepath):
            shutil.copy(filepath, dst_filepath)
        else:
            copy_content(filepath, dst_filepath)