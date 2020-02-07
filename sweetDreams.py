#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import itertools
import os
import os.path
import subprocess
import sys
import time
from modules.cherrytree import *
from modules.ssh import *
from modules.http import *


def error_display(code):
    """Displays the error message corresponding to the code passed as a parameter"""
    if code == 1:
        sys.stderr.write("[!] SweetDreams: Argument error: sudo ./sweetDreams.py <target> <output_file.ctd>\n")
    elif code == 2:
        sys.stderr.write("[!] SweetDreams:nmap error: You must have nmap installed and run this script with root privileges\n")
    elif code == 3:
        sys.stderr.write("[!] SweetDreams: Target error: nmap doesn't recognize the ip adress or the hostname\n")
    exit(code)


def service_catcher(file_name):
    """Catch from a nmap grepable output file the list of actives services"""
    scan_f = open(file_name,"r")
    ports = []
    for line in scan_f:  # read the file line by line
        if "Ports:" in line:
            # ports part
            fields = line.split(' ')[3:]  # split the output and only keep the ports fields
            for field in fields:
                ports.append(field.split('/')[:1][0])

            # services name part
            services = line.split('//')[1:-1]  # split the output and only keep the ports fields
            del services[1::2]  # only keep the name of the service by deleting the odd fields

    scan_f.close
    results = dict(zip(ports, services))

    return results


def version_catcher(file_name):
    """Catch from a nmap grepable output file the version of actives services"""
    scan_f = open(file_name,"r")
    version = []
    for line in scan_f:  # read the file line by line
        if "Ports:" in line:
            fields = line.split('Ports: ')[1]  # split the output and only keep the ports fields
            fields = fields.split('Index: ')[0]
            fields = fields.split(',')
            i=0
            for field in fields:
                field = field.split('/')
                if field[6] == '':
                    field[6] = "Not found..."
                version.append(field[6])
                i+=1
    scan_f.close
    return version


def nmap_init(target,file_name):
    """Start the nmap scan and begin the information gathering"""
    animated_loading("Nmap -sS scan")
    temp = file_name + ".temp"
    file_name += ".txt"
    try:
        subprocess.run(["nmap","-p-","-sS",target,"-oG", temp, "-oN", file_name], stdout=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        error_display(2)

    try:
        services = service_catcher(temp)
    except UnboundLocalError:  # this happens if the target is incorrect
        error_display(3)
    subprocess.run(["rm",temp])  # comment if you want to keep the grepable output file from nmap
    return services


def nmap_sv(dicto,target,file_name):
    """Execute the nmap version scan (sV) and save the output in a temporary file"""
    animated_loading("Nmap -sV scan")
    file_name += ".txt"
    ports = "-p"
    for port in dicto:
        ports += port + ","
    ports = ports[:-1]
    subprocess.run(["nmap",ports,"-sV",target,"--append-output","-oG","sV_temp","-oN",file_name,"-O"], stdout=subprocess.DEVNULL)
    results = version_catcher("sV_temp")
    
    return results


def animated_loading(text):
    """A useless loading animation"""
    sys.stdout.write("\r[*] "+text+" in progress...\n")
    # for char in itertools.cycle(['|', '/', '-', '\\']):
    #     sys.stdout.write("\r[*] "+text+" in progress ["+char+"]")
    #     sys.stdout.flush()
    #     time.sleep(0.1)
    # sys.stdout.write("\r[*] "+text+" Done!\n")


def os_guess(sv_file):
    """Pick up the OS version from the nmap sV scan output file"""
    scan_f = open(sv_file,"r")
    os_version = ""
    
    line = scan_f.readline()
    while line and os_version == "":
        if "OS details:" in line:
            os_version = line[12:].split(',')[0]  # split the output and only keep the os version
        elif "OS guesses:" in line:
            os_version = "Just guessing... " + line[23:].split(',')[0]  # split the output and only keep the os version
        line = scan_f.readline()
    scan_f.close
    if os_version == "":
        os_version = "Not found..."
    
    return os_version


# =========================== MAIN ===========================
if len(sys.argv) != 3:
    error_display(1)
with open(".local/ascii.txt", 'r') as ascii:  # for the banner
    print(ascii.read())

file_name = sys.argv[2]
target = sys.argv[1]

print("[*] Start time:",time.strftime("%H:%M:%S"))
start_time = time.time()
port_serv = nmap_init(sys.argv[1],sys.argv[2])  # initialization
versions = nmap_sv(port_serv,target,sys.argv[2])  # grepable output in the file sV_temp

# //////////// WORK AREA //////////////
# --- HEAD ---
os = os_guess(file_name + ".txt")
file_o = open(file_name, "a")
cherry_header(file_o,target,os)
cherry_table(file_o, port_serv, versions)
# --- BODY ---
for i,(port,serv) in enumerate(port_serv.items()):
    function_name = serv + ".py"
    if os.path.isfile("modules/" + function_name):
        exec(function_name)
# --- TAIL ---
cherry_tail(file_o)
# /////////////////////////////////////

end_time = time.time()
hours, rem = divmod(end_time-start_time, 3600)
minutes, seconds = divmod(rem, 60)
print("[*] Done, {:0>2}:{:0>2}:{:05.2f} elapsed !".format(int(hours),int(minutes),seconds))
file_o.close
