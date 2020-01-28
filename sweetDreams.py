#!/usr/bin/python3
import time
import sys
import subprocess

def service_catcher(file_name):
    """Catch from a nmap grepable output file the list of actives services"""
    scan_f = open("scan.txt","r")
    for line in scan_f:
        if "Ports:" in line:
            services = line.split('//')[1:-1] # Split the output and only keep the ports fields
            del services[1::2] # Only keep the service name
    
    scan_f.close
    return services

if len(sys.argv) != 3:
    sys.stderr.write("Argument error : ./sweetDreams.py <target> <output_file.xml>\n")
    exit(1)

target = sys.argv[1]
file_o = open(sys.argv[2], "w")
start_time = time.time()

# TODO: multiple output ? On garde le -oG pour la liste servicee, mais en même temps dans un autre fichier on met le -oX
service_l = service_catcher("scan.txt")
print(service_l)
end_time = time.time()
# file_o.write("Coucou\n")
file_o.close
print("[*] Done, ", end_time-start_time," elapsed !")

