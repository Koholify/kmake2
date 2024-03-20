#! /bin/env python3

from argparse import ArgumentParser
import os
from os import abort, path
import shutil
import sys

CONFIG_FILE_NAME = "KMakeFile.txt"
VERSION_NUMBER = "1.0.0"

class Config:
    def __init__(self) -> None:
        self.name = ""
        self.d_src = ""
        self.d_build = ""
        self.d_install = ""
        self.d_parent = ""
        self.cc = ""
        self.cflags = ""
        self.lflags = ""
        self.includes = ""
        self.type = ""
        self.extension = ""
        self.compile_commands = False

    def __repr__(self) -> str:
        d = dict()
        d["name"] = self.name
        d["d_build"] = self.d_build
        d["d_src"] = self.d_src
        d["d_install"] = self.d_install
        d["d_parent"] = self.d_parent
        d["cc"] = self.cc
        d["cflags"] = self.cflags
        d["lflags"] = self.lflags
        d["includes"] = self.includes
        d["type"] = self.type
        d["compile_commands"] = self.compile_commands
        d["extension"] = self.extension
        return f"(Config){str(d)}"

    def fill(self, path="KMakeFile.txt"):
        filevars = {}
        with open(path, "r") as file:
            for line in file.readlines():
                line = line.strip()
                p = line.split("=", maxsplit=1)
                if len(p) < 2: continue
                filevars[p[0]] = p[1]

        self.extension = filevars["EXT"]
        self.d_parent = filevars["DIR"]
        self.cc = filevars["CC"]
        self.d_src = filevars["SRC"]
        self.d_build = filevars["BUILD"]
        self.name = filevars["PROJECTNAME"]
        self.type = filevars["TYPE"]
        self.cflags = filevars["CFLAGS"]
        self.lflags = filevars["LFLAGS"]
        self.includes = filevars["INCLUDES"]
        self.d_install = filevars["INSTALL_LOC"]
        self.compile_commands = not filevars["COMPILE_COMMANDS"] == '0'

        return self

makeTemplate = """
CC=clang
SRC=src/
BUILD=.build/

PROJECTNAME=_NAME_
EXT=.c
TYPE=exe
CFLAGS=-std=c17 -Werror -Wall -pedantic
LFLAGS=
INCLUDES=

INSTALL_LOC=/usr/local/bin/
COMPILE_COMMANDS=0
"""

gitignoreTemplate = """
.build
.vs
.vscode
"""

helloWorldTemplate = """
#include <stdio.h>

int main(int argc, char** argv) {
	printf(\"Hello World!\\n\");
}
"""

def create_compile_command(cfg: Config, s_file: str) -> str:
    o_file = path.join(cfg.d_build, "obj", s_file + ".o")
    s = path.join(cfg.d_src, s_file)
    return f"{cfg.cc} {cfg.cflags} {cfg.includes} -I{cfg.d_src} -c {s} -o {o_file}"

def get_target_name(cfg: Config) -> str:
    target = cfg.name
    if cfg.type == "exe":
        if sys.platform == "win32":
            target = target + ".exe"
    if cfg.type == "static":
        if sys.platform == "win32":
            target = target + ".lib"
        else:
            target = target + ".a"
    return target

def get_exe_path(cfg: Config) -> str:
    target = get_target_name(cfg)
    exe_path = path.join(cfg.d_build, target)
    if sys.platform == "win32":
        exe_path = exe_path.replace("/", "\\")
    return exe_path

def fill_config() -> Config:
    try:
        return Config().fill()
    except FileNotFoundError:
        print(f"{CONFIG_FILE_NAME} not found")
        abort()

def init_dir(name="app", override=False):
    src_path = path.join(".", "src")
    obj_path = path.join(".", ".build", "obj")

    print("Creating:", src_path, obj_path)
    try:
        os.makedirs(src_path, exist_ok=True)
        os.makedirs(obj_path, exist_ok=True)
    except:
        print("Error creating directories")

    cwd = os.getcwd()
    if override or not os.access(CONFIG_FILE_NAME, mode=os.O_RDONLY):
        print(f"Creating: {CONFIG_FILE_NAME}")
        with open(CONFIG_FILE_NAME, mode="w") as file:
            template = makeTemplate.replace("_NAME_", name)
            file.write("DIR=" + cwd + "/\n")
            file.write(template)

    if not os.access(".gitignore", mode=os.O_RDONLY):
        print("Creating: .gitignore")
        with open(".gitignore", mode="w") as file:
            file.write(gitignoreTemplate)

    main_path = path.join(src_path, "main.c")
    if not os.access(main_path, mode=os.O_RDONLY):
        print("Creating:", main_path)
        with open(main_path, mode="w") as file:
            file.write(helloWorldTemplate)


def clean_dir():
    cfg = fill_config()
    obj_path = path.join(cfg.d_build, "obj")
    obj_files = os.listdir(obj_path)
    for file in obj_files:
        os.remove(path.join(obj_path, file))

    target = get_target_name(cfg)
    exe_path = path.join(cfg.d_build, target)
    try:
        os.remove(exe_path)
    except FileNotFoundError:
        print(f"unable to find {exe_path} to remove")

commandTemplate = """{{
  "directory": "{d_parent}",
  "command": "{cmd}",
  "file": "{file}"
}}"""
def compile_commands():
    cfg = fill_config()
    with open("compile_commands.json", mode="w") as cFile:
        cFile.write("[\n")
        files = os.listdir(cfg.d_src)
        for (i, file) in enumerate(files):
            command = create_compile_command(cfg, file)
            entry = commandTemplate.format(d_parent=cfg.d_parent, cmd=command, file=path.join(cfg.d_src, file))
            cFile.write(entry)

            if i < len(files) - 1:
                cFile.write(",\n")
            else:
                cFile.write("\n")

        cFile.write("]\n")

def run_exe():
    cfg = fill_config()
    exe_path = get_exe_path(cfg)
    print(exe_path)
    res = os.system(exe_path)
    print(f"Exit Code: {res}")

def install_exe():
    cfg = fill_config()
    exe_path = get_exe_path(cfg)
    install_path = cfg.d_install
    try:
        shutil.copy(exe_path, install_path)
    except PermissionError:
        print(f"PermissionError: install failed: '{install_path}'")

def compile():
    cfg = fill_config()
    source_path = cfg.d_src
    files = os.listdir(source_path)
    source_files = list(filter(lambda f: f.endswith(cfg.extension), files))
    header_files = list(map(lambda f: path.join(source_path, f), filter(lambda f: f.endswith(".h"), files)))
    target_objs = list(map(lambda f: path.join(cfg.d_build, "obj", (f + ".o")), source_files))

    if len(source_files) < 1:
        print("No source files found")
        abort()

    header_mtime = 0
    if len(header_files) > 0:
        header_mtime = max(list(map(lambda f: path.getmtime(f), header_files)))

    errors = False
    for (s_file, o_file) in zip(source_files, target_objs):
        s_mtime = path.getmtime(path.join(source_path, s_file))
        o_mtime = 0.0

        try:
            o_mtime = path.getmtime(o_file)
        except FileNotFoundError:
            pass

        if s_mtime > o_mtime or header_mtime > o_mtime:
            command = create_compile_command(cfg, s_file)
            print(command)
            res = os.system(command)
            if not res == 0:
                print(f"Error Compiling {s_file}")
                errors = True

    if not errors:
        target = get_target_name(cfg)
        exe_path = path.join(cfg.d_build, target)
        command = f"{cfg.cc} {' '.join(target_objs)} -o {exe_path} {cfg.lflags}"
        print(command)
        res = os.system(command)
        if not res == 0:
            print(f"Error linking {cfg.name}")

    if cfg.compile_commands:
        compile_commands()


def run():
    parser = ArgumentParser(description=f"Compile project with {CONFIG_FILE_NAME}")
    parser.add_argument("--version", action="store_true",
                        help="print version number")
    parser.add_argument("-r", "--run", action="store_true",
                        help="run compiled program")
    parser.add_argument("-i", "--init", action="store_true",
                        help="create initial directory structure")
    parser.add_argument("-c", "--clean", action="store_true",
                        help="remove all compiled objects and executables")
    parser.add_argument("-C", "--command", action="store_true",
                        help="remake compile_commands.json database")
    parser.add_argument("-I", "--install", action="store_true",
                        help="install executable into location from KMakeFile")
    parser.add_argument("-n", "--name", help="set name with init command", default="app")
    parser.add_argument("-o", "--override", action="store_true",
                        help="overwrite existing KMakeFile during initialization")
    args = parser.parse_args()

    if args.version:
        print(f"KMake2 version {VERSION_NUMBER}")
    elif args.run:
        run_exe()
    elif args.init:
        init_dir(args.name, args.override)
    elif args.clean:
        clean_dir()
    elif args.command:
        compile_commands()
    elif args.install:
        install_exe()
    else:
        compile()

if __name__ == "__main__":
    run()
