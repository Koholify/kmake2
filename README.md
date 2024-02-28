# kmake2
CLI tool for compiling and building C projects

Successor to the original *kmake* https://github.com/Koholify/Kmake

usage: kmake [-h] [-r] [-i] [-c] [-C] [-I] [-n NAME] [-o]

Compile project with KMakeFile.txt

options:\
  -h, --help            show this help message and exit\
  -i, --init            create initial directory structure\
		-n NAME, --name NAME  set name with init command\
		-o, --override        overwrite existing KMakeFile during initialization\
  -r, --run             run compiled program\
  -c, --clean           remove all compiled objects and executables\
  -C, --command         remake compile_commands.json database\
  -I, --install         install executable into location from KMakeFile\
