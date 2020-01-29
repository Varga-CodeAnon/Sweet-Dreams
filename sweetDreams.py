#!/usr/bin/python3
import os
import subprocess
import sys
import time
import datetime


def error_display(code):
    """Displays the error message corresponding to the code passed as a parameter"""
    if code == 1:
        sys.stderr.write("[!] SweetDreams: Argument error: sudo ./sweetDreams.py <target> <output_file.xml>\n")
    elif code == 2:
        sys.stderr.write("[!] SweetDreams:nmap error: You must have nmap installed and run this script with root privileges\n")
    elif code == 3:
        sys.stderr.write("[!] SweetDreams: Target error: nmap doesn't recognize the ip adress or the hostname\n")
    exit(code)


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
    try:
        subprocess.run(["nmap","--top-ports=10","-sS",target,"-oG", temp, "-oX", file_name], stdout=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        error_display(2)

    try:
        services = service_catcher(temp)
    except UnboundLocalError:  # this happens if the target is incorrect
        error_display(3)
    subprocess.run(["rm",temp])  # comment if you want to keep the grepable output file from nmap
    return services


def animated_loading():
    """A useless loading animation"""
    for i in range(10):
        sys.stdout.write("\r[*] Let's start the information gathering [|]")
        time.sleep(0.1)
        sys.stdout.write("\r[*] Let's start the information gathering [/]")
        time.sleep(0.1)
        sys.stdout.write("\r[*] Let's start the information gathering [-]")
        time.sleep(0.1)
        sys.stdout.write("\r[*] Let's start the information gathering [\\]")
        time.sleep(0.1)
    sys.stdout.write("\r[*] Let's start the information gathering\n")
# =========================== MAIN ===========================
if len(sys.argv) != 3:
    error_display(1)
with open("ascii.txt", 'r') as ascii:  # for the banner
    print(ascii.read())
# file_o = open(file_name, "w")
print("[*] Start time: ",datetime.datetime.now().time())
start_time = time.time()

animated_loading()
print(nmap_init(sys.argv[1],sys.argv[2]))

end_time = time.time()
# file_o.write("Coucou\n")
# file_o.close
print("[*] Done, ", end_time-start_time," elapsed !")
