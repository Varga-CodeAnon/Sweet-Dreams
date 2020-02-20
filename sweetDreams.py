#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
import subprocess
import sys
import time
from modules.cherrytree import *
from modules.ssh import *
from modules.http import *
from modules.postgresql import *


class Target:
    """Define a target which has :
        - an IP address
        - an OS
        - opened ports
        - services versions detected"""
    
    def __init__(self, ip_addr, os_target, ports_dict, versions_list):
        """Constructeur de notre classe"""
        self.ip = ip_addr
        self.os = os_target
        self.ports = ports_dict
        self.versions = versions_list
        

def error_display(code):
    """Display the error message corresponding to the code passed as a parameter"""
    if code == 1:
        sys.stderr.write("[!] SweetDreams: Argument error: sudo ./sweetDreams.py <target> <output_file>\n")
    elif code == 2:
        sys.stderr.write(
            "[!] SweetDreams: nmap error: You must have nmap installed and run this script with root privileges\n")
    elif code == 3:
        sys.stderr.write("[!] SweetDreams: Target error: nmap doesn't recognize the IP address or the hostname\n")
    exit(code)


def animated_loading(text):
    """A useless loading animation"""
    sys.stdout.write("\r[*] " + text + " in progress...\n")
    # for char in itertools.cycle(['|', '/', '-', '\\']):
    #     sys.stdout.write("\r[*] "+text+" in progress ["+char+"]")
    #     sys.stdout.flush()
    #     time.sleep(0.1)
    # sys.stdout.write("\r[*] "+text+" Done!\n")


def service_catcher(file_nm):
    """Catch from a nmap grepable output file the list of actives services"""
    scan_f = open(file_nm, "r")
    services = ''
    ports = []
    for line in scan_f:  # read the file line by line
        if "Ports:" in line:
            fields = line.split(' ')[3:]  # split the output and remove some garbage
            # Ports part
            for field in fields:
                ports.append(field.split('/')[:1][0])  # we only keep the 'ports' fields

            # Protocol name part
            services = line.split('//')[1:-1]  # split the line
            del services[1::2]  # and only keep the name of the service by deleting the odd fields

    scan_f.close()
    results = dict(zip(ports, services))
    return results


def version_catcher(file_nm):
    """Catch from a nmap grepable output file the version of actives services"""
    scan_f = open(file_nm, "r")
    version = []
    for line in scan_f:  # read the file line by line
        if "Ports:" in line:
            fields = line.split('Ports: ')[1]  # similar to the 'service_catcher' function
            fields = fields.split('Index: ')[0]
            fields = fields.split(',')
            index = 0
            for field in fields:
                field = field.split('/')
                if field[6] == '':  # if there are no known versions
                    field[6] = "Not found..."
                version.append(field[6])
                index += 1
    scan_f.close()
    return version


def nmap_init(target_ip, file_nm):
    """Start the nmap scan and begin the information gathering"""
    animated_loading("Nmap -sS scan")
    temp = file_nm + ".temp"
    file_nm += ".txt"
    services = ''
    try:
        subprocess.run(["nmap", "-p-", "-sS", target_ip, "-oG", temp, "-oN", file_nm], stdout=subprocess.DEVNULL,
                       check=True)  # modify if you want to run another type of scan
    except subprocess.CalledProcessError:
        error_display(2)  # if the privileges are insufficient
    try:
        services = service_catcher(temp)
    except UnboundLocalError:  # this happens if the target is incorrect
        error_display(3)
    subprocess.run(["rm", temp])  # comment if you want to keep the grepable output file from nmap
    return services


def nmap_sv(dicto, target_ip, file_nm):
    """Execute the nmap version scan (sV) and save the output in a temporary file"""
    animated_loading("Nmap -sV scan")
    file_nm += ".txt"
    ports = "-p"
    for prt in dicto:
        ports += prt + ","
    ports = ports[:-1]
    subprocess.run(["nmap", ports, "-sV", target_ip, "--append-output", "-oG", "sV_temp", "-oN", file_nm, "-O"],
                   stdout=subprocess.DEVNULL)  # modify if you want to run another type of scan
    results = version_catcher("sV_temp")
    return results


def os_guess(sv_file):
    """Pick up the OS version from the nmap sV scan output file"""
    scan_f = open(sv_file, "r")
    os_version = ""
    line = scan_f.readline()
    while line and os_version == "":
        if "OS details:" in line:
            os_version = line[12:].split(',')[0]
        elif "OS guesses:" in line:
            os_version = "Just guessing... " + line[23:].split(',')[0]
        line = scan_f.readline()
    scan_f.close()
    if os_version == "":
        os_version = "Not found..."
    return os_version


# ==========================[ MAIN ]===========================
if len(sys.argv) != 3:
    error_display(1)

with open(".local/ascii.txt", 'r') as ascii_file:  # for the banner
    print(ascii_file.read())

print("[*] Start time:", time.strftime("%H:%M:%S"))
start_time = time.time()
target = sys.argv[1]
file_name = sys.argv[2]
file_o = open(file_name + ".ctd", "a")
# ---[ Test OFF ]---
# port_serv = nmap_init(target, file_name)  # initialization
# versions = nmap_sv(port_serv, target, file_name)  # grepable output stored in the file sV_temp
# os_found = os_guess(file_name + ".txt")
# ------------------
# ---[ Test  ON ]---
port_serv = {
    "22":"ssh",
    "80":"http",
    "443":"ssl/http"}
versions = [
    "OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)",
    "Apache httpd 2.4.29 ((Ubuntu))",
    "Apache httpd 2.4.29 ((Ubuntu))"]
os_found = "SweetDreams OS"
# ------------------
victim = Target(target,os_found,port_serv,versions)
# -----[ HEAD ]-----
cherry_header(file_o, victim)
cherry_table(file_o, victim)
# -----[ BODY ]-----
for i, (port, serv) in enumerate(victim.ports.items()):
    if os.path.exists("modules/{}.py".format(serv)):
        fct_name = "main_" + serv + "(file_o,\"" + file_name + ".ctd\",victim)"
        exec(fct_name)
# -----[ TAIL ]-----
cherry_tail(file_o)
# ------------------
end_time = time.time()
hours, rem = divmod(end_time - start_time, 3600)
minutes, seconds = divmod(rem, 60)
print("[*] Done, {:0>2}:{:0>2}:{:05.2f} elapsed !".format(int(hours), int(minutes), seconds))
file_o.close()
# =========================== -@@- ===========================
