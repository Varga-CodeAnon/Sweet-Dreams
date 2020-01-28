#!/usr/bin/python3
import time
import sys
import subprocess

if len(sys.argv) != 3:
    sys.stderr.write("Argument error : ./sweetDreams.py <target> <output_file.xml>\n")
    exit(1)

target = sys.argv[1]
file_o = open(sys.argv[2], "w")
start_time = time.time()

# Let start the first scan
# [...]

# Protocols list
scan_f = open("scan.txt","r")
for line in scan_f:
    if "Ports:" in line:
        protocols = line.split('//')[1:-1] # Split the output and only keep the ports fields
        del protocols[1::2] # Only keep the protocol name
# print(protocols)
scan_f.close
# --------------

end_time = time.time()
# file_o.write("Coucou\n")
file_o.close
print("[*] Done, ", end_time-start_time," elapsed !")

