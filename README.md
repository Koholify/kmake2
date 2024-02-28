# kmake2
CLI tool for compiling and building C projects

Executables can be found in the *[os]-dist* branch in the *dist* folder

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
