#!/usr/bin/python3
import time
import sys

if len(sys.argv) != 3:
    sys.stderr.write("Argument error : ./sweetDreams.py <target> <output_file.xml>\n")
    exit(1)

target = sys.argv[1]
file_o = open(sys.argv[2], "w")
start_time = time.time()
time.sleep(3)
end_time = time.time()
# file_o.write("Coucou\n")
file_o.close
print("[*] Done, ", end_time-start_time," elapsed !")