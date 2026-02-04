import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

root = os.path.dirname(os.path.dirname(__file__))

dir_path_static = os.path.join(root, "static")
dir_path_public = os.path.join(root, "docs")
dir_path_content = os.path.join(root, "content")
template_path = os.path.join(root, "template.html")

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/" 

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        basepath,
    )

if __name__ == "__main__":
    main()
