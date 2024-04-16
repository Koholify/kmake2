# kmake2
CLI tool for compiling and building C projects

Successor to the original *kmake* https://github.com/Koholify/Kmake

usage: kmake [-h] [-r] [-i] [-c] [-C] [-I] [-n NAME] [-o]

Compile project with KMakeFile.txt

options:\
&ensp;-h, --help            show this help message and exit\
&ensp;-i, --init            create initial directory structure\
&emsp; -n NAME, --name NAME  set name with init command\
&emsp; -o, --override        overwrite existing KMakeFile during initialization\
&ensp;-r, --run             run compiled program\
&ensp;-c, --clean           remove all compiled objects and executables\
&ensp;-C, --command         remake compile_commands.json database\
&ensp;-I, --install         install executable into location from KMakeFile

Installation instructions:\
Debian/Ubuntu - .deb package is provided for quick install\
&ensp;git clone https://github.com/Koholify/Kmake2.git && sudo dpkg -i ./Kmake2/kmake-1.0.deb

other - build and install kmake into an executable with pyinstaller\
&ensp;requirements - pyinstaller, recommended to create python-venv and install with `pip install pyinstaller`\
&ensp;windows - `./build.bat && ./install.bat [install location]`\
&ensp;&ensp;(default location: dest=%homepath%\tools\bin)\
&ensp;*nix and macos - `./build.sh && sudo ./install.sh`\
&ensp;&ensp;(installs to /usr/local/bin)
