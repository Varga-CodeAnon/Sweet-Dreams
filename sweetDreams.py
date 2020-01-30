#!/usr/bin/python3
import os
import subprocess
import sys
import time
import datetime


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


def nmap_init(target,file_name):
    """Start the nmap scan and begin the information gathering"""
    temp = file_name + ".temp"
    try:
        subprocess.run(["nmap","--top-ports=10","-sS",target,"-oG", temp, "-oN", file_name], stdout=subprocess.DEVNULL, check=True)
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
    i = 0
    while i < 10:
        sys.stdout.write("\r[*] Let's start the information gathering [|]")
        time.sleep(0.1)
        sys.stdout.write("\r[*] Let's start the information gathering [/]")
        time.sleep(0.1)
        sys.stdout.write("\r[*] Let's start the information gathering [-]")
        time.sleep(0.1)
        sys.stdout.write("\r[*] Let's start the information gathering [\\]")
        time.sleep(0.1)
        i+=1
    sys.stdout.write("\r[*] Let's start the information gathering\n")

# =========================== MAIN ===========================
if len(sys.argv) != 3:
    error_display(1)
with open(".local/ascii.txt", 'r') as ascii:  # for the banner
    print(ascii.read())

print("[*] Start time: ",datetime.datetime.now().time())
start_time = time.time()
# //////////// WORK AREA //////////////
file_name = sys.argv[2] + ".ctd"
target = sys.argv[1]
os = "FIXME:"
services_table = "FIXME:"
file_o = open(file_name, "w")
file_o.write(
"""<?xml version="1.0" ?>
<cherrytree>
    <node custom_icon_id="14" foreground="" is_bold="True" name="SweetDreams" prog_lang="custom-colors" readonly="False" tags="" ts_creation="0.0" ts_lastsave="0.0" unique_id="1">\
        <rich_text weight="heavy">Target:</rich_text>
        <rich_text> """ + target + """\n</rich_text>
        <rich_text weight="heavy">OS:</rich_text>
		<rich_text> """ + os + """\n</rich_text>""")

file_o.write(
"""	</node>
</cherrytree>""")

# /////////////////////////////////////
print(nmap_init(sys.argv[1],sys.argv[2]))
end_time = time.time()
# file_o.write("Coucou\n")
# file_o.close
print("[*] Done, ", end_time-start_time," elapsed !")
