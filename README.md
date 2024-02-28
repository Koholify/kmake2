# kmake2
CLI tool for compiling and building C projects

Successor to the original *kmake* https://github.com/Koholify/Kmake

usage: kmake [-h] [-r] [-i] [-c] [-C] [-I] [-n NAME] [-o]

Compile project with KMakeFile.txt

options:\
*Tabspace*  -h, --help            show this help message and exit\
*Tabspace*  -i, --init            create initial directory structure\
*Tabspace**		-n NAME, --name NAME  set name with init command\
*Tabspace**		-o, --override        overwrite existing KMakeFile during initialization\
*Tabspace*  -r, --run             run compiled program\
*Tabspace*  -c, --clean           remove all compiled objects and executables\
*Tabspace*  -C, --command         remake compile_commands.json database\
*Tabspace*  -I, --install         install executable into location from KMakeFile\
