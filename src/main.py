from textnode import *
from os import path, listdir, mkdir
from shutil import copy, rmtree


def main():
    print("hello world")
    example = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(str(example))
    copy_static("static/", "public/")

def copy_static(source_dir, dest_dir):
    print(source_dir)
    if not path.exists(source_dir):
        raise FileNotFoundError("Source directory could not be found")
    
    if path.exists(dest_dir):
        rmtree(dest_dir)
    mkdir(dest_dir)

    for file in listdir(source_dir):
        current_file = f"{source_dir}{file}"
        if path.isfile(current_file):
            copy(current_file, dest_dir)
        else:
            copy_static(current_file+"/",f"{dest_dir}{file}/")

main()        
