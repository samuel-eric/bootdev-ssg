from copy_content import copy_content
from generate_page import generate_page_recursive
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_content(dir_path_static, dir_path_public)
    generate_page_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()