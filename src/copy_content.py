import os
import shutil

def copy_content_to_public(src, dst):
    if dst == "public":
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir("public")
    for object in os.listdir(src):
        filepath = os.path.join(src, object)
        dst_filepath = os.path.join(dst, object)
        if os.path.isfile(filepath):
            shutil.copy(filepath, dst_filepath)
        else:
            os.mkdir(dst_filepath)
            copy_content_to_public(filepath, dst_filepath)