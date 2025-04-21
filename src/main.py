from copy_content import copy_content
from generate_page import generate_page_recursive
import os
import shutil
import sys

dir_path_static = "./static"
dir_path_public = "./docs"

def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_content(dir_path_static, dir_path_public)
    generate_page_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()