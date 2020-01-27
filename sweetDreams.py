#!/usr/bin/python3
import sys

if len(sys.argv) != 3:
    sys.stderr.write("Argument error : ./sweetDreams.py <target> <output_file.xml>\n")
    exit(1)

target = sys.argv[1]
file_o = open(sys.argv[2], "w")
# file_o.write("Coucou\n")
file_o.close