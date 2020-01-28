#!/usr/bin/python3
import os
import subprocess
import sys
import time

def service_catcher(file_name):
    """Catch from a nmap grepable output file the list of actives services"""
    scan_f = open(file_name,"r")
    for line in scan_f:  # read the file line by line
        if "Ports:" in line:
            services = line.split('//')[1:-1]  # split the output and only keep the ports fields
            del services[1::2]  # only keep the service name
    scan_f.close
    return services

def nmap_init(target,file_name):
    """Start the nmap scan and begin the information gathering"""
    temp = file_name + ".temp"
    subprocess.run(["nmap","--top-ports=10","-sS",target,"-oG", temp, "-oX", file_name], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)    
    try:
        services = service_catcher(temp)
    except UnboundLocalError:  # this happens if the target is incorrect
        sys.stderr.write("[!] Target error : nmap doesn't recognize the ip adress or the hostname\n")
        exit(2)
    subprocess.run(["rm",temp])  # comment if you want to keep the grepable output file from nmap
    return services

if len(sys.argv) != 3:
    sys.stderr.write("[!] Argument error : ./sweetDreams.py <target> <output_file.xml>\n")
    exit(1)

# file_o = open(file_name, "w")
start_time = time.time()

print(nmap_init(sys.argv[1],sys.argv[2]))

end_time = time.time()
# file_o.write("Coucou\n")
# file_o.close
print("[*] Done, ", end_time-start_time," elapsed !")
