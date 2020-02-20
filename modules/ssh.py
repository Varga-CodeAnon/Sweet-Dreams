"""Collect informations from the SSH protocol"""
import subprocess
import time  # for the sleep command
from modules.cherrytree import *


def description(file_ctd):
    """Displays a methodology to enumerate the port 22 (source :)"""
    file_ctd.write(
"""\n			<rich_text style="italic" weight="heavy">CheckList:</rich_text>
			<rich_text>

• Fingerprint server </rich_text>
			<rich_text foreground="#2a30ffff0000">(done)</rich_text>
			<rich_text>
   ◇ telnet ip_address 22 (banner grab) 
   ◇ </rich_text>
			<rich_text link="webs http://www.monkey.org/%7Eprovos/scanssh/">scanssh</rich_text>
			<rich_text>
      ▪ scanssh -p -r -e excludes random(no.)/Network_ID/Subnet_Mask 
• Password guessing
   ◇ ssh root@ip_address 
   ◇ </rich_text>
			<rich_text link="webs http://packetstormsecurity.org/groups/teso/guess-who-0.44.tgz">guess-who</rich_text>
			<rich_text>
      ▪ ./b -l username -h ip_address -p 22 -2 &lt; password_file_location 
   ◇ </rich_text>
			<rich_text link="webs http://freeworld.thc.org/">Hydra brute force </rich_text>
			<rich_text>
   ◇ </rich_text>
			<rich_text link="webs http://www.edge-security.com/edge-soft.php">brutessh</rich_text>
			<rich_text>
   ◇ </rich_text>
			<rich_text link="webs http://www.darkc0de.com/c0de/ruby/sshbrute.txt">Ruby SSH Bruteforcer </rich_text>
			<rich_text>                                                                
• Examine configuration files 
   ◇ ssh_config 
   ◇ sshd_config 
   ◇ authorized_keys 
   ◇ ssh_known_hosts 
   ◇ .shosts 
• SSH Client programs
   ◇ </rich_text>
			<rich_text link="webs http://www.bitvise.com/">tunnelier </rich_text>
			<rich_text>
   ◇ </rich_text>
			<rich_text link="webs http://www.bitvise.com/winsshd">winsshd </rich_text>
			<rich_text>
   ◇ </rich_text>
			<rich_text link="webs http://www.chiark.greenend.org.uk/%7Esgtatham/putty/">putty </rich_text>
			<rich_text>
   ◇ </rich_text>
			<rich_text link="webs http://winscp.net/eng/index.php">winscp </rich_text>
			<rich_text>

</rich_text>"""
    )


def main_ssh(file_ctd, file_name, target_victim):
    """Execute the information gathering"""
    begin_node(file_ctd,"ssh",'2')
    print("[*] SSH enum in progress...")
    description(file_ctd)

    # cve
    begin_node(file_ctd,"cve",'3')

    file_temp = open("temp", "w")
    cmd = ['cat','/home/adam/Git/Sweet-Dreams/ssh_results']
    subprocess.call(cmd, stdout=file_temp) # , stdout=subprocess.DEVNULL
    file_temp.close()
    file_temp = open("temp", "r")
    file_ctd.write("<rich_text>")
    for line in file_temp:
        file_ctd.write(line)
    file_ctd.write("</rich_text>")

    end_node(file_ctd)
    # /cve

    # fingerprint
    begin_node(file_ctd,"fingerprint",'4')
    begin_code(file_ctd)
    file_ctd.write("""Okay !""")
    end_code(file_ctd)
    end_node(file_ctd)
    # /fingerprint
    end_node(file_ctd)
    print("[*] SSH enum done!")
