from asyncore import write
from distutils.file_util import write_file
import glob, os, re

final =""

os.chdir(os.path.dirname(os.path.dirname(__file__)))
for file in glob.glob("*.txt"):
    lineNumber = 0
    with open(file) as topo_file:
        for line in topo_file:
            lineNumber+=1
            if(lineNumber== 1):
                final+="\\beginsong{"+line.rstrip('\n')+"}\n"
            else:
                final+=line
        final+="\\endsong\n\n"

os.chdir(os.path.dirname(__file__))
f = open("autogenerated.tex", "w")
f.write(final)
f.close()